#!/usr/bin/env python3
"""Exact finite checks for an equality-neutral reporting loss.

This standalone standard-library program enumerates small ordered partitions
and evaluates constructed finite laws directly. It does not import a ranking
package, fit a model, draw random samples, or call an optimizer. Finite checks
supplement general mathematical arguments; they are not proofs for arbitrary
laws, a benchmark, or evidence about the frequency of ties in real data.

Run once with ordinary Python 3. The JSON destination defaults to the script's
name with a .json suffix. Existing output is never overwritten.
"""

from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import sys


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    return value


def digest(value):
    encoded = json.dumps(serial(value), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def reports(n):
    """Every surjection onto 1,...,G: canonical ordered partitions, not RGSs."""
    return tuple(g for g in product(range(1, n + 1), repeat=n)
                 if set(g) == set(range(1, max(g) + 1)))


def law(name, weights, states):
    result = {"name": name, "weights": tuple(weights), "states": tuple(states)}
    n, k = len(states[0][1]), len(weights)
    if sum(weights) != 1 or any(w < 0 for w in weights):
        raise ValueError("Weights must be normalized and nonnegative")
    if sum(p for p, _ in states) != 1 or any(p <= 0 for p, _ in states):
        raise ValueError("State masses must be positive and sum to one")
    if n < 2 or any(len(s) != n or any(len(row) != k for row in s)
                    for _, s in states):
        raise ValueError("Inconsistent finite-state dimensions")
    return result


def raw_risk(law_, g, tau, weak=False):
    """Read each raw state, then average its realized pair losses."""
    n, weights = len(g), law_["weights"]
    total = F(0)
    for mass, state in law_["states"]:
        realized = F(0)
        for i, j in combinations(range(n), 2):
            for k, weight in enumerate(weights):
                left, right = state[i][k], state[j][k]
                if g[i] == g[j]:
                    cost = tau if weak or left != right else F(0)
                elif g[i] < g[j]:
                    cost = F(left <= right if weak else left < right)
                else:
                    cost = F(right <= left if weak else right < left)
                realized += weight * cost
        total += mass * realized
    return total / F(n * (n - 1), 2)


def coefficients(law_):
    """Independently tabulate strict direction and equality probabilities."""
    n, weights = len(law_["states"][0][1]), law_["weights"]
    b, t, d = {}, {}, {}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for k in range(len(weights)):
                b[i, j, k] = sum(p for p, s in law_["states"]
                                 if s[i][k] < s[j][k])
                t[i, j, k] = sum(p for p, s in law_["states"]
                                 if s[i][k] == s[j][k])
                d[i, j, k] = 1 - t[i, j, k]
    c = {(i, j): sum(w * b[i, j, k] for k, w in enumerate(weights))
         for i in range(n) for j in range(n) if i != j}
    delta = {(i, j): sum(w * d[i, j, k] for k, w in enumerate(weights))
             for i, j in combinations(range(n), 2)}
    return {"b": b, "t": t, "d": d, "c": c, "delta": delta}


def summaries(coef, g):
    n = len(g)
    pairs = tuple(combinations(range(n), 2))
    wrong = sum(coef["c"][i, j] for i in range(n) for j in range(n)
                if g[i] < g[j])
    total_mass = sum(coef["delta"].values())
    disclosed_mass = sum(coef["delta"][i, j] for i, j in pairs if g[i] != g[j])
    return wrong, total_mass, disclosed_mass, sum(g[i] != g[j] for i, j in pairs)


def coefficient_risk(coef, g, tau):
    """Sum directed disclosures and tied-pair terms, separately from raw loss."""
    n = len(g)
    disclosed = sum(coef["c"][i, j] for i in range(n) for j in range(n)
                    if g[i] < g[j])
    held = sum(coef["delta"][i, j] for i, j in combinations(range(n), 2)
               if g[i] == g[j])
    return (disclosed + tau * held) / F(n * (n - 1), 2)


def raw_utility(law_, g, lam):
    total = F(0)
    for mass, state in law_["states"]:
        for i, j in combinations(range(len(g)), 2):
            if g[i] == g[j]:
                continue
            high, low = (i, j) if g[i] < g[j] else (j, i)
            for k, w in enumerate(law_["weights"]):
                difference = state[high][k] - state[low][k]
                payoff = lam if difference > 0 else (-1 if difference < 0 else 0)
                total += mass * w * payoff
    return total / F(len(g) * (len(g) - 1), 2)


def identity_pairs(law_):
    n = len(law_["states"][0][1])
    active = [k for k, w in enumerate(law_["weights"]) if w > 0]
    return tuple((i, j) for i, j in combinations(range(n), 2)
                 if all(s[i][k] == s[j][k] for _, s in law_["states"] for k in active))


def minimizers(law_, family, tau):
    values = [(g, raw_risk(law_, g, tau)) for g in family]
    best = min(v for _, v in values)
    return best, tuple(g for g, v in values if v == best)


def run_checks():
    counts = defaultdict(int)

    def require(condition, group, context=""):
        counts[group] += 1
        if not condition:
            raise AssertionError(f"{group}: {context}")

    grid = tuple(F(i, 20) for i in range(1, 11))
    families = {n: reports(n) for n in (2, 3, 4)}
    for n, expected in ((2, 3), (3, 13), (4, 75)):
        require(len(families[n]) == expected, "enumeration", str(n))
    laws = [
        law("tie_free", (F(3, 7), F(4, 7)), (
            (F(2, 5), ((3, 1), (2, 3), (1, 2))),
            (F(3, 5), ((1, 3), (3, 2), (2, 1))))),
        law("partial_equalities", (F(1, 3), F(2, 3)), (
            (F(2, 5), ((0, 0), (0, 1), (2, 0))),
            (F(3, 5), ((1, 0), (0, 0), (1, 2))))),
        law("identity_pair", (F(1, 2), F(1, 2)), (
            (F(1, 3), ((0, 2), (0, 2), (1, 1))),
            (F(2, 3), ((2, 0), (2, 0), (1, 1))))),
        law("all_identical", (F(1, 2), F(1, 2)), (
            (F(1), ((1, 2), (1, 2), (1, 2))),)),
        law("four_unit_counterexample", (F(1, 4), F(3, 4)), (
            (F(3, 5), ((0, 0), (0, 0), (2, 0), (3, 1))),
            (F(2, 5), ((0, 0), (0, 0), (2, 0), (1, 1))))),
    ]
    law_results = []
    for item in laws:
        n, weights = len(item["states"][0][1]), item["weights"]
        M, coef = F(n * (n - 1), 2), coefficients(item)
        family, ids = families[n], identity_pairs(item)
        for i, j in combinations(range(n), 2):
            for k in range(len(weights)):
                require(coef["b"][i, j, k] + coef["b"][j, i, k] == coef["d"][i, j, k],
                        "reverse_relation", item["name"])
        for g in family:
            A, T, Q, N = summaries(coef, g)
            for tau in grid:
                risk = raw_risk(item, g, tau)
                require(risk == coefficient_risk(coef, g, tau), "raw_vs_coefficients", str(g))
                require(risk == (A + tau * (T - Q)) / M, "distinct_mass_expression", str(g))
                correction = sum(w * coef["t"][i, j, k] * (tau if g[i] == g[j] else 1)
                                 for i, j in combinations(range(n), 2)
                                 for k, w in enumerate(weights)) / M
                require(raw_risk(item, g, tau, weak=True) - risk == correction,
                        "weak_minus_neutral_identity", str(g))
                if item["name"] == "tie_free":
                    require(risk == raw_risk(item, g, tau, weak=True), "zero_tie_reduction", str(g))
                lam = tau / (1 - tau)
                require(risk == tau * T / M - (1 - tau) * raw_utility(item, g, lam),
                        "payoff_affine_relation", str(g))
        # Compare each fixed at-most-G family with its fixed identity guard.
        for cap in range(1, n + 1):
            unrestricted = tuple(g for g in family if max(g) <= cap)
            guarded = tuple(g for g in unrestricted if all(g[i] == g[j] for i, j in ids))
            for tau in grid:
                require(minimizers(item, unrestricted, tau)[0] == minimizers(item, guarded, tau)[0],
                        "guard_preserves_optimum", f"{item['name']},G={cap},tau={tau}")
            # T, the action family and the guard are fixed throughout each grid.
            for fixed in (unrestricted, guarded):
                optima = [minimizers(item, fixed, tau)[1] for tau in grid]
                for left, right in zip(optima, optima[1:]):
                    max_left = max(summaries(coef, g)[2] for g in left)
                    min_right = min(summaries(coef, g)[2] for g in right)
                    require(max_left <= min_right, "fixed_family_mass_monotonicity", item["name"])
        law_results.append({"name": item["name"], "n": n, "K": len(weights),
                            "reports": len(family), "identity_pairs": ids,
                            "total_distinct_mass": sum(coef["delta"].values())})

    # Zero-cost equivalence does not force every minimizing report to obey a guard.
    identical = laws[3]
    require(len(minimizers(identical, families[3], F(1, 4))[1]) == 13,
            "guard_existence_not_all_minimizers")
    t11, tau_results = laws[4], []
    c11 = coefficients(t11)
    binary = tuple(g for g in families[4] if max(g) <= 2)
    guarded_binary = tuple(g for g in binary if g[0] == g[1])
    require(len(binary) == 15 and len(guarded_binary) == 7, "counterexample_family_counts")
    require(sum(c11["delta"].values()) == F(7, 2), "counterexample_total_mass")
    expected_actions = ((F(1, 10), (2, 2, 1, 1), F(1, 60), 4, F(5, 2)),
                        (F(3, 10), (2, 2, 2, 1), F(1, 24), 3, F(3)))
    for tau, expected_g, expected_risk, expected_N, expected_Q in expected_actions:
        minimum, optimum = minimizers(t11, guarded_binary, tau)
        require(optimum == (expected_g,), "counterexample_unique_guarded_minimum", str(tau))
        require(minimum == expected_risk, "counterexample_exact_risk", str(tau))
        A, T, Q, N = summaries(c11, expected_g)
        require(N == expected_N and Q == expected_Q, "counterexample_disclosure_counts", str(tau))
        require(minimizers(t11, binary, tau)[0] == minimum, "counterexample_unguarded_minimum", str(tau))
        tau_results.append({"tau": tau, "grade": expected_g, "risk": minimum,
                            "raw_disclosed_pairs": N, "distinct_disclosed_mass": Q})
    require(tau_results[0]["raw_disclosed_pairs"] > tau_results[1]["raw_disclosed_pairs"],
            "raw_disclosure_not_monotone")
    require(tau_results[0]["distinct_disclosed_mass"] < tau_results[1]["distinct_disclosed_mass"],
            "distinct_mass_counterexample_increases")
    require(not any(max(g) == 4 and g[0] == g[1] for g in families[4]),
            "exact_G_can_be_infeasible_with_guard")
    table = [{"grade": g, "wrong_mass": summaries(c11, g)[0],
              "withheld_distinct_mass": summaries(c11, g)[1] - summaries(c11, g)[2],
              "raw_disclosed_pairs": summaries(c11, g)[3],
              "distinct_disclosed_mass": summaries(c11, g)[2]} for g in guarded_binary]

    # The two primary targets are evaluated on one common, unchanged action family.
    criterion = law("conflicting_criteria", (F(1, 2), F(1, 2)),
                    ((F(1), ((1, -1), (0, 0))),))
    composite = law("zero_composite", (F(1),), ((F(1), ((0,), (0,))),))
    tau = F(1, 4)
    target_comparison = []
    for g in families[2]:
        target_comparison.append({"grade": g, "criterion_risk": raw_risk(criterion, g, tau),
                                  "composite_risk": raw_risk(composite, g, tau)})
    require(raw_risk(criterion, (1, 1), tau) == tau and raw_risk(composite, (1, 1), tau) == 0,
            "co_primary_withholding_does_not_cancel")
    require(raw_risk(criterion, (1, 1), tau, True) == raw_risk(composite, (1, 1), tau, True),
            "weak_comparison_withholding_does_cancel")

    # Coherent coefficient perturbations generated from two exact finite laws.
    true = law("error_true", (F(1),), ((F(1, 2), ((0,), (0,), (0,))),
                                      (F(1, 2), ((3,), (2,), (1,)))))
    estimated = law("error_approximation", (F(1),), ((F(3, 5), ((0,), (0,), (0,))),
                                                     (F(2, 5), ((3,), (2,), (1,)))))
    ct, ce = coefficients(true), coefficients(estimated)
    eps_b = max(abs(ct["c"][key] - ce["c"][key]) for key in ct["c"])
    eps_d = max(abs(ct["delta"][key] - ce["delta"][key]) for key in ct["delta"])
    for g in families[3]:
        N, M = summaries(ct, g)[3], 3
        for tau in grid:
            discrepancy = abs(raw_risk(true, g, tau) - coefficient_risk(ce, g, tau))
            radius = (N * eps_b + tau * (M - N) * eps_d) / M
            require(discrepancy <= radius, "coefficient_geometry_bound", str(g))
            require(radius <= max(eps_b, tau * eps_d) <= eps_b,
                    "coherent_uniform_bound", str(g))
    require(eps_d <= 2 * eps_b, "coherent_distinct_mass_radius")
    hold_difference = abs(raw_risk(true, (1, 1, 1), F(1, 4))
                          - coefficient_risk(ce, (1, 1, 1), F(1, 4)))
    require(hold_difference == F(1, 40), "all_withhold_nonzero_coefficient_error")
    # A second perturbation changes the selected action and gives positive regret.
    rt = law("regret_true", (F(1),), ((F(11, 20), ((1,), (0,))),
             (F(1, 4), ((0,), (1,))), (F(1, 5), ((0,), (0,)))))
    re = law("regret_approximation", (F(1),), ((F(3, 5), ((1,), (0,))),
             (F(1, 5), ((0,), (1,))), (F(1, 5), ((0,), (0,)))))
    risk_t, g_t = minimizers(rt, families[2], F(3, 10))
    _, g_e = minimizers(re, families[2], F(3, 10))
    require(g_t == ((1, 1),) and g_e == ((1, 2),), "perturbed_selection")
    regret = raw_risk(rt, g_e[0], F(3, 10)) - risk_t
    require(regret == F(1, 100) and regret <= F(1, 20), "perturbed_selection_regret_bound")

    result = {"status": "pass", "tau_grid": grid, "laws": law_results,
              "assertion_counts": dict(sorted(counts.items())), "total_assertions": sum(counts.values()),
              "four_unit_minima": tau_results, "four_unit_guarded_binary_table": table,
              "co_primary_target_comparison": target_comparison,
              "coefficient_error_example": {"Delta_b": eps_b, "Delta_d": eps_d,
                  "all_withhold_discrepancy_at_tau_1_4": hold_difference,
                  "positive_selection_regret": regret},
              "input_laws_sha256": digest(laws + [criterion, composite, true, estimated, rt, re])}
    result["exact_results_sha256"] = digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite an existing result")
    result = run_checks()
    result["execution"] = {"at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0], "script_name": Path(__file__).name,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "arithmetic": "fractions.Fraction; no floating-point risks or randomized draws",
        "execution_scope": "One evaluation of the bounded finite checks; no package or solver import",
        "limitations": ["Finite examples do not prove general propositions.",
            "Guard preservation is checked only for fixed at-most-G families without extra restrictions.",
            "Distinct-mass monotonicity holds for each fixed law, weight vector, guard and action family.",
            "The two target objectives use the same fixed family; no law-derived guard is transferred.",
            "No empirical validity, model calibration, runtime or scalability conclusion is drawn."]}
    args.output.write_text(json.dumps(serial(result), indent=2) + "\n")
    print(json.dumps({"status": result["status"], "total_assertions": result["total_assertions"],
                      "exact_results_sha256": result["exact_results_sha256"]}))


if __name__ == "__main__":
    main()
