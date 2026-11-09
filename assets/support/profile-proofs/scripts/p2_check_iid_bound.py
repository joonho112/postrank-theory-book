#!/usr/bin/env python3
"""Bounded N01 formula checks; no posterior simulation or certificate engine."""
from decimal import Decimal as D, localcontext, ROUND_CEILING
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math


def margin(K, S, beta):
    if type(K) is not int or K < 1 or type(S) is not int or S < 1:
        raise ValueError("K and S must be positive integers")
    beta = D(beta)
    if not D(0) < beta < D(1):
        raise ValueError("beta must be in (0,1)")
    return ((D(K) / beta).ln() / (2 * S)).sqrt()


def run():
    root = Path(__file__).resolve().parents[1]
    checks = []

    def check(condition, label):
        assert condition, label
        checks.append(label)

    with localcontext() as context:
        context.prec = 80
        beta, eta = D("0.05"), D("0.02")
        table = []
        for K in [1, 9, 1000, 1000000]:
            epsilon = margin(K, 1000, beta)
            required = int(((D(K)/beta).ln()/(2*eta**2)).to_integral_value(rounding=ROUND_CEILING))
            check(margin(K, required, beta) <= eta, f"K={K}: ceiling sample size meets target")
            check(margin(K, required-1, beta) > eta, f"K={K}: preceding sample size misses target")
            residual = abs(D(K)*(-2*D(1000)*epsilon**2).exp()-beta)
            check(residual < D("1e-70"), f"K={K}: exponential formula agrees to working precision")
            floating = math.sqrt(math.log(K/float(beta))/(2*1000))
            check(abs(float(epsilon)-floating) < 1e-14, f"K={K}: independent math-library formula check")
            table.append({"K": K, "S": 1000, "beta": str(beta),
                          "margin_decimal_80_digit_working_precision": str(epsilon),
                          "margin_rounded_six_decimals": str(epsilon.quantize(D("0.000001"))),
                          "target_margin": str(eta), "sufficient_S_ceiling": required})
        check(all(margin(a,1000,beta)<margin(b,1000,beta)
                  for a,b in zip([1,9,1000],[9,1000,1000000])), "larger K increases margin")
        check(margin(9,10000,beta)<margin(9,1000,beta), "larger S decreases margin")
        check(margin(9,1000,beta)>D("0.05"), "K=9,S=1000: zero errors do not pass alpha=.05")
        check(margin(1,1000,beta)>0, "alpha=0 cannot pass a positive stochastic margin")
        large = margin(1000000,5,beta)
        check(large>1, "small S can make the formula margin exceed one")
        check(all(min(D(1),D(v)/5+large)==1 for v in range(6)), "clipped upper bound is then identically one")
        examples = []
        for v in [300,350]:
            epsilon = margin(9,10000,beta)
            estimate = D(v)/10000
            upper = min(D(1),estimate+epsilon)
            accepted = upper <= D("0.05")
            check(accepted==(v==300), f"illustrative count v={v}: margin comparison")
            examples.append({"kind":"illustrative count; no sample was generated", "K":9,
                             "S":10000,"v":v,"Jhat":str(estimate),"beta":str(beta),
                             "epsilon":str(epsilon),"U":str(upper),"alpha":"0.05",
                             "sufficient_rule_passes":accepted})
        for K,S,b in [(0,10,".05"),(1,0,".05"),(1,10,"0"),(1,10,"1")]:
            rejected = False
            try:
                margin(K,S,b)
            except ValueError:
                rejected = True
            check(rejected, f"reject invalid K,S,beta: {K},{S},{b}")
        files = ["proofs/N01-iid-uniform-bound.qmd", "contracts/mc-selection.qmd",
                 "contracts/decision-contract-v1.qmd", "contracts/profile-risk-spec.qmd",
                 "contracts/input-provenance.qmd", "scripts/p2_check_iid_bound.py"]
        result = {
            "fixture_id":"N01-iid-uniform-bound-formulas-v1",
            "timestamp_utc":datetime.now(timezone.utc).isoformat(),
            "status":"PASS", "checks_passed":len(checks), "checks":checks,
            "formula":"sqrt(log(K/beta)/(2*S))",
            "sample_size_formula":"ceil(log(K/beta)/(2*eta^2))",
            "working_precision_decimal_digits":80,
            "illustration_table":table, "count_illustrations":examples,
            "large_margin_case":{"K":1000000,"S":5,"beta":str(beta),"epsilon":str(large),"clipped_U":"1"},
            "qualification":"Numerical formula checks only; not an interval-arithmetic certificate, probability proof, simulation, coverage study or empirical data result.",
            "source_hashes":{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files}}
    destination = root / "fixtures/p2-v1/iid-uniform-bound-check.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status":result["status"],"checks_passed":result["checks_passed"],
                      "table":[{"K":row["K"],"margin":row["margin_rounded_six_decimals"],
                                "required_S":row["sufficient_S_ceiling"]} for row in table]},indent=2))


if __name__ == "__main__":
    run()
