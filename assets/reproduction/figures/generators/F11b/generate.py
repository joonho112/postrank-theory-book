#!/usr/bin/env python3
"""F11b: exact local loss matrices with symbolic state probabilities.

Public scientific inputs only. No numerical tau or probability is selected.
Run with python -B; SVG glyphs use the frozen portable outline style.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve()
BASE = HERE.parents[2]
sys.path.insert(0, str(BASE))
import figstyle as fs
from matplotlib.patches import Rectangle

ROOT = fs.ROOT
FID = "F11b"
STEM = "f11b-equality-changes-the-loss-and-the-baseline"
DATA = ROOT / "assets/reproduction/figures/data/pair-loss-matrices.json"
RECEIPT = ROOT / "evidence/figures/builds/F11b.json"
C = fs.PALETTE


def check_fixture(data):
    checks = []
    for row, state in enumerate(data["states"]):
        i, j = state["theta_i"], state["theta_j"]
        definitions = {
            "weak_error": [(int(i <= j), 0), (0, 1), (int(j <= i), 0)],
            "equality_neutral": [(int(i < j), 0), (0, int(i != j)), (int(j < i), 0)],
        }
        for loss, values in definitions.items():
            for col, (a, b) in enumerate(values):
                cell = data[loss][row][col]
                assert (cell["constant"], cell["tau_coefficient"]) == (a, b)
                assert cell["label"] == ("tau" if b else str(a))
                checks.append({"loss": loss, "state": state["id"], "action": data["actions"][col]["id"], "definition_match": True})
    differences = []
    for row in range(3):
        for col in range(3):
            a, b = data["weak_error"][row][col], data["equality_neutral"][row][col]
            actual = (a["constant"] - b["constant"], a["tau_coefficient"] - b["tau_coefficient"])
            expected = ((1, 0) if col != 1 else (0, 1)) if row == 1 else (0, 0)
            assert actual == expected
            differences.append({"row": row, "column": col, "coefficients": list(actual), "equality_only_difference": True})
    expected = data["expected_pair_costs"]
    assert expected["weak_error"] == {"forward": "p_zero + p_minus", "hold": "tau", "reverse": "p_plus + p_zero"}
    assert expected["equality_neutral"] == {"forward": "p_minus", "hold": "tau * (p_plus + p_minus)", "reverse": "p_plus"}
    assert data["all_withhold_baseline"]["one_pair_one_criterion"] == {"weak_error": "tau", "equality_neutral": "tau * d"}
    return {"definition_cells": checks, "equality_differences": differences, "expected_cost_formulas": 6, "local_baseline_formulas": 2, "result": "PASS exact symbolic checks; no numerical probability or tau evaluated"}


def label(ax, x, y, text, size, **kwargs):
    kwargs.setdefault("color", C["ink"])
    return ax.text(x, y, text, fontsize=size, **kwargs)


def matrix(ax, data, loss, mobile):
    size = 14 if mobile else 12.5
    title = "Weak-error loss" if loss == "weak_error" else "Equality-neutral loss"
    color = C["teal"] if loss == "weak_error" else C["ochre"]
    label(ax, .025, .97, title, 15 if mobile else 14.5, va="top", weight="semibold")
    label(ax, .035, .79, "Latent state", size, va="center")
    xs = [.50, .69, .88]
    for x, title in zip(xs, [r"$i\succ j$", "Hold", r"$j\succ i$"]):
        label(ax, x, .79, title, size, ha="center", va="center")
    relations = [r"$\theta_i>\theta_j$", r"$\theta_i=\theta_j$", r"$\theta_i<\theta_j$"]
    for row, (y, relation) in enumerate(zip([.59, .40, .21], relations)):
        if row == 1:
            ax.add_patch(Rectangle((.015, y - .087), .965, .174, facecolor=C["light"], edgecolor=color, linewidth=1.35, zorder=0))
        label(ax, .035, y, relation, size + .5, va="center")
        for col, x in enumerate(xs):
            ax.add_patch(Rectangle((x - .085, y - .075), .17, .15, facecolor="none", edgecolor=C["line"], linewidth=.75, zorder=1))
            raw = data[loss][row][col]["label"]
            math = r"$\tau$" if raw == "tau" else "$" + raw + "$"
            label(ax, x, y, math, size + 2, ha="center", va="center")
    label(ax, .025, .04, "Same rows and reporting actions", 13 if mobile else 11.5, va="center", color=C["muted"])


def events(ax, mobile):
    size = 14 if mobile else 12.5
    label(ax, .01, .96, "Symbolic state masses", size, va="top", weight="semibold")
    names = [r"$p_+$" + "\nStrict forward", r"$p_0$" + "\nEquality", r"$p_-$" + "\nStrict reverse"]
    for x, text in zip([.17, .50, .83], names):
        fs.box(ax, x - .15, .29, .30, .41, text, size=size, fc=C["white"], ec=C["line"])
    label(ax, .5, .10, r"$p_+ + p_0 + p_- = 1$" + "  |  Boxes are not to scale", 12.5 if mobile else 11.5, ha="center", va="center")


def expected_costs(ax, mobile):
    size = 14 if mobile else 12.5
    label(ax, .01, .97, "Expected local costs", size, va="top", weight="semibold")
    label(ax, .53, .71, "Weak-error", size, ha="center", va="center")
    label(ax, .85, .71, "Neutral", size, ha="center", va="center")
    for y, name, weak, neutral in [(.43, r"Report $i\succ j$", r"$p_0+p_-$", r"$p_-$"), (.13, "Hold", r"$\tau$", r"$\tau(p_++p_-)$")]:
        label(ax, .01, y, name, size, va="center")
        label(ax, .53, y, weak, size + .5, ha="center", va="center")
        label(ax, .85, y, neutral, size + .5, ha="center", va="center")


def baseline(ax, mobile):
    size = 14 if mobile else 12.5
    title = "Full-report all-withhold baseline\n(if feasible)" if mobile else "Full-report all-withhold baseline (if feasible)"
    label(ax, .01, .95, title, size, va="top", weight="semibold", linespacing=1.25)
    if mobile:
        label(ax, .01, .68, r"Weak-error: $\tau$", size + .5, va="center")
        label(ax, .01, .44, r"Equality-neutral: $R_0^s=\tau T_w^s/M$", size + .5, va="center")
        note = "Zero neutral cost does not certify\nstrict superiority. Hold withholds a direction."
        label(ax, .01, .09, note, 13, va="center", linespacing=1.25, color=C["muted"])
    else:
        label(ax, .01, .58, r"Weak-error: $\tau$", size + .5, va="center")
        label(ax, .47, .58, r"Equality-neutral: $R_0^s=\tau T_w^s/M$", size + .5, va="center")
        label(ax, .01, .17, "Zero neutral cost does not certify strict superiority; hold withholds a direction.", 11.5, va="center", color=C["muted"])


def draw(data, mobile):
    fig = fs.canvas(4.8 if mobile else 10.8, 16.8 if mobile else 9.3, mobile)
    fig.text(.04, .989, "Equality changes the loss\nand the baseline" if mobile else "Equality changes the loss and the baseline", va="top", fontsize=15.5 if mobile else 16, weight="semibold")
    fig.text(.04, .945 if mobile else .928, "One pair, one criterion.\nBefore weighting and division by M." if mobile else "One pair and one criterion, before weighting and division by M.", va="top", fontsize=13.5 if mobile else 12.5, color=C["muted"], linespacing=1.25)
    rects = [(.02, .68, .96, .235), (.02, .42, .96, .235), (.04, .285, .92, .12), (.04, .16, .92, .11), (.04, .015, .92, .13)] if mobile else [(.025, .52, .46, .35), (.515, .52, .46, .35), (.05, .34, .90, .15), (.05, .19, .90, .125), (.05, .03, .90, .13)]
    axes = [fs.diagram_axis(fig, rect) for rect in rects]
    matrix(axes[0], data, "weak_error", mobile)
    matrix(axes[1], data, "equality_neutral", mobile)
    events(axes[2], mobile)
    expected_costs(axes[3], mobile)
    baseline(axes[4], mobile)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    checks = []
    for idx, ax in enumerate(axes):
        bounds = ax.get_window_extent(renderer)
        texts = [(t, t.get_window_extent(renderer)) for t in ax.texts]
        for text, bb in texts:
            inside = bool(bb.x0 >= bounds.x0 - 1 and bb.x1 <= bounds.x1 + 1 and bb.y0 >= bounds.y0 - 1 and bb.y1 <= bounds.y1 + 1)
            checks.append({"panel": idx, "label": text.get_text(), "font_pt": text.get_fontsize(), "inside_panel": inside})
        for i, (text, bb) in enumerate(texts):
            for other, ob in texts[i + 1:]:
                if bb.overlaps(ob):
                    raise RuntimeError("Text overlap: " + text.get_text() + " / " + other.get_text())
    if not all(c["inside_panel"] for c in checks):
        raise RuntimeError("Clipped text: " + str([c for c in checks if not c["inside_panel"]]))
    return fs.export(fig, STEM, mobile), {"mobile": mobile, "canvas_inches": list(fig.get_size_inches()), "text_checks": checks, "all_panel_text_inside_and_nonoverlapping": True}


def generate(overwrite=False):
    prior = json.loads(RECEIPT.read_text()) if RECEIPT.exists() else None
    targets = [ROOT / "assets/figures" / (STEM + suffix + "." + ext) for suffix in ["", "-mobile"] for ext in ["svg", "pdf", "png"]]
    if not overwrite and (RECEIPT.exists() or any(p.exists() for p in targets)):
        raise SystemExit("Refuse existing F11b output; --overwrite is reserved for a recorded repair.")
    data = json.loads(DATA.read_text())
    exact = check_fixture(data)
    outputs, geometry = [], []
    for mobile in [False, True]:
        files, checks = draw(data, mobile)
        outputs.extend(files)
        geometry.append(checks)
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    inputs = [DATA, BASE / "figstyle.py", HERE]
    record = {"id": FID, "step": "4.12", "author": 'JoonHo Lee (jlee296@ua.edu)',  "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": 'rendered', "command": "python -B assets/reproduction/figures/generators/F11b/generate.py" + (" --overwrite" if overwrite else ""), "source_refs": ["chapters/11-multicriteria-loss.qmd (controlling text; not a runtime input)"], "inputs": [{"path": str(p.relative_to(ROOT)), "sha256": h(p)} for p in inputs], "outputs": outputs, "exact_checks": exact, "geometry_checks": geometry, "actual_image_views": [], "execution": {"python": platform.python_version(), "production_invocations_total": 1 if prior is None else prior["execution"]["production_invocations_total"] + 1, "last_command_invocations": 1, "layout_exports": 2, "asset_exports": 6, "symbolic_definition_check_runs": 1, "numerical_probabilities": 0, "numerical_tau_values": 0, "posterior_samples": 0, "optimizer_runs": 0, "model_fits": 0, "canonical_edits": 0, "registry_edits": 0}, "scope": "Exact symbolic local-loss tables and event/baseline labels from public inputs. Geometry does not encode probability or numeric tau. No empirical calculation or global optimization.", "limits": [  "No PDF-pixel inspection is claimed by generation."], "repairs": [], "required_repairs_remaining": []}
    if prior:
        record["previous_export_history"] = prior.get("previous_export_history", []) + [{"outputs": prior["outputs"], "execution": prior["execution"], "views": prior.get("actual_image_views", [])}]
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"id": FID, "outputs": outputs, "geometry": "PASS", "exact_cells": 18}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overwrite", action="store_true")
    generate(parser.parse_args().overwrite)
