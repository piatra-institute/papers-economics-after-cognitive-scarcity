"""What free cognition determines, and what it leaves open.

Three constructions. The first is an exact competitive equilibrium; the second
and third are properties of stated models, and no number in either is an
estimate of any real economy.

1. The allocation benchmark. Two goods, identical preferences, identical and
   universally free cognition, and physical production already automated. The
   equilibrium is solved in closed form and the entire distribution of
   consumption is shown to be a function of claims on output alone. Multiplying
   physical output by ten leaves relative housing consumption untouched.

2. The permanent remainder. Tasks have capability requirements; machine
   capability rises; a task is done by people while capability is below its
   requirement. The claim that there will always be work for people is checked
   against the claim that people will always earn a share of output, and the two
   are shown to come apart: the set of human-advantaged tasks can be nonempty
   at every date while the human income share falls to zero. What a positive
   limiting share requires is computed, and so is the rate at which new tasks
   would have to arrive to sustain one.

3. The fallback. An automated system fails; something must recover. The optimal
   fallback is computed over the plane of machine capability and failure
   independence, so that "the automation failed, therefore a human is needed"
   becomes an inequality that can be false. The confound in the deskilling
   evidence is quantified separately: automation that removes easy cases raises
   the mean human resolution time with competence held exactly fixed.

Seeded where sampling is used. A failed invariant fails the run.
"""
from __future__ import annotations

import numpy as np

SEED = 20260905


def _py(x):
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating,)):
        return round(float(x), 6)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, float):
        return round(x, 6)
    return x


# ---------------------------------------------------------------------------
# 1. The allocation benchmark
# ---------------------------------------------------------------------------
# N people, a consumption good Q and a housing service H, both in fixed net
# supply because their physical production is assumed already automated.
# Preferences are identical: log c + eta log h. Person i owns share theta_i of
# every productive asset; a fraction tau of asset income is pooled and shared
# equally. Cognition is free and identical for everyone, and enters utility only
# through an additive constant, so it cannot affect the allocation of Q and H.

N_PEOPLE = 100
TOP_GROUP = 10
TOP_SHARE = 0.90
SUPPLY_Q, SUPPLY_H = 100.0, 100.0
ETA = 1.0
POOLING = (0.0, 0.5, 1.0)
OUTPUT_MULTIPLIER = 10.0


def _shares(theta: np.ndarray, tau: float) -> np.ndarray:
    return (1.0 - tau) * theta + tau / len(theta)


def run_allocation() -> dict:
    theta = np.empty(N_PEOPLE)
    theta[:TOP_GROUP] = TOP_SHARE / TOP_GROUP
    theta[TOP_GROUP:] = (1.0 - TOP_SHARE) / (N_PEOPLE - TOP_GROUP)
    assert abs(theta.sum() - 1.0) < 1e-12

    rows = []
    for tau in POOLING:
        s = _shares(theta, tau)
        c = s * SUPPLY_Q
        h = s * SUPPLY_H
        rows.append({
            "pooling": tau,
            "consumption_top": float(c[0]),
            "consumption_rest": float(c[-1]),
            "ratio": float(c[0] / c[-1]),
            "housing_top": float(h[0]), "housing_rest": float(h[-1]),
            "shares_sum": float(s.sum()),
            "price_of_housing": ETA * SUPPLY_Q / SUPPLY_H,
        })

    # ten times the consumption good, everything else unchanged
    s = _shares(theta, 0.0)
    scaled = {
        "consumption_top": float(s[0] * SUPPLY_Q * OUTPUT_MULTIPLIER),
        "consumption_rest": float(s[-1] * SUPPLY_Q * OUTPUT_MULTIPLIER),
        "housing_top": float(s[0] * SUPPLY_H),
        "housing_rest": float(s[-1] * SUPPLY_H),
        "housing_ratio_change": 0.0,
        "price_of_housing": ETA * SUPPLY_Q * OUTPUT_MULTIPLIER / SUPPLY_H,
    }

    # any strictly positive share vector is supportable by some ownership
    rng = np.random.default_rng(SEED)
    targets = rng.dirichlet(np.ones(N_PEOPLE), 200)
    max_error = 0.0
    for target in targets:
        implied = target  # with tau = 0 the share vector is the ownership vector
        realised = _shares(implied, 0.0)
        max_error = max(max_error, float(np.abs(realised - target).max()))

    return {
        "n_people": N_PEOPLE, "top_group": TOP_GROUP, "top_share": TOP_SHARE,
        "supply_q": SUPPLY_Q, "supply_h": SUPPLY_H, "eta": ETA,
        "rows": rows,
        "ratio_no_pooling": rows[0]["ratio"],
        "ratio_half_pooling": rows[1]["ratio"],
        "ratio_full_pooling": rows[2]["ratio"],
        "scaled": scaled,
        "supportable_share_vectors_tested": len(targets),
        "max_support_error": max_error,
    }


# ---------------------------------------------------------------------------
# 2. The permanent remainder
# ---------------------------------------------------------------------------
# Tasks have capability requirements. Machine capability rises, and a task is
# held by people while capability is below its requirement. Two propositions are
# often run together: that at every date some task is still held by people, and
# that people therefore keep a share of output. The first does not give the
# second. In the arrival model a task created above the frontier is swept up at
# rate `a`; tasks also become obsolete at rate `delta`; and the share of tasks
# held by people converges to delta / (a + delta), with no dependence on how
# fast new tasks arrive.

HORIZON_YEARS = 400
STEPS_PER_YEAR = 12
TURNOVER = (0.02, 0.05, 0.10)         # annual task-obsolescence rates
SWEEP_RATES = (0.10, 0.20, 0.50, 1.00)  # annual rate at which capability passes a new task
ARRIVAL_RATES = (1.0, 10.0, 100.0)    # new tasks per year
NONCOGNITIVE_MASS = (0.0, 0.02, 0.10)  # share of tasks needing something other than reasoning


def _remainder_path(arrival: float, sweep: float, turnover: float,
                    atom: float, steps: int) -> dict:
    """Stocks of human-held and machine-held tasks under arrivals and turnover.

    A newly created task sits above the capability frontier and is taken over
    at rate `sweep`; every task becomes obsolete at rate `turnover`; a share
    `atom` of new tasks requires something the premise has not made free, so
    capability never takes them.
    """
    dt = 1.0 / STEPS_PER_YEAR
    human, machine, permanent = 1.0, 0.0, 0.0
    path = []
    for step in range(steps):
        new = arrival * dt
        d_perm = new * atom - permanent * turnover * dt
        d_human = new * (1 - atom) - human * (sweep + turnover) * dt
        d_machine = human * sweep * dt - machine * turnover * dt
        human += d_human
        machine += d_machine
        permanent += d_perm
        total = human + machine + permanent
        path.append((human + permanent) / total if total > 0 else 0.0)
    return {"path": path, "final_share": path[-1],
            "human": human, "machine": machine, "permanent": permanent}


def run_remainder() -> dict:
    steps = HORIZON_YEARS * STEPS_PER_YEAR
    grid = []
    for turnover in TURNOVER:
        for sweep in SWEEP_RATES:
            closed = turnover / (sweep + turnover)
            sim = _remainder_path(10.0, sweep, turnover, 0.0, steps)
            grid.append({"turnover": turnover, "sweep": sweep,
                         "closed_form": closed,
                         "simulated": sim["final_share"],
                         "error": abs(closed - sim["final_share"])})

    # the arrival rate cancels: three orders of magnitude, one limit
    arrivals = []
    for arrival in ARRIVAL_RATES:
        sim = _remainder_path(arrival, 0.20, 0.05, 0.0, steps)
        arrivals.append({"arrival_rate": arrival,
                         "final_share": sim["final_share"]})
    arrival_spread = (max(a["final_share"] for a in arrivals)
                      - min(a["final_share"] for a in arrivals))

    # what a positive limit actually requires
    atoms = []
    for atom in NONCOGNITIVE_MASS:
        sim = _remainder_path(10.0, 1.00, 0.05, atom, steps)
        atoms.append({"noncognitive_share_of_new_tasks": atom,
                      "final_share": sim["final_share"]})

    # the frontier is never empty even where the share vanishes
    fast = _remainder_path(10.0, 1.00, 0.02, 0.0, steps)
    nonempty = fast["human"] > 0.0

    paths = {f"sweep_{s:g}": _remainder_path(10.0, s, 0.05, 0.0, steps)["path"]
             for s in SWEEP_RATES}
    paths["noncognitive_0.10"] = _remainder_path(10.0, 1.00, 0.05, 0.10,
                                                 steps)["path"]
    return {
        "horizon_years": HORIZON_YEARS,
        "grid": grid,
        "max_closed_form_error": max(g["error"] for g in grid),
        "arrivals": arrivals,
        "arrival_spread": arrival_spread,
        "atoms": atoms,
        "share_without_atom": atoms[0]["final_share"],
        "share_with_two_percent_atom": atoms[1]["final_share"],
        "share_with_ten_percent_atom": atoms[2]["final_share"],
        "frontier_never_empty": bool(nonempty),
        "residual_human_stock": fast["human"],
        "paths": paths,
        "share_at_turnover_5_sweep_20": next(
            g["closed_form"] for g in grid
            if g["turnover"] == 0.05 and g["sweep"] == 0.20),
        "share_at_turnover_5_sweep_100": next(
            g["closed_form"] for g in grid
            if g["turnover"] == 0.05 and g["sweep"] == 1.00),
    }


# ---------------------------------------------------------------------------
# 3. The fallback
# ---------------------------------------------------------------------------
# A primary automated system fails and something must recover. The candidates
# are a person, an independent automated system, and a safe-state procedure.
# What matters is not whether the primary failed but the conditional success
# probability of each candidate given that it did, and that depends on how much
# of the primary's failure the candidate shares.

BASE_HUMAN_SKILL = 0.72        # unconditional success of a practised responder
HUMAN_SHARED_FAILURE = 0.10    # share of primary failures a person also fails on
SAFE_STATE_SUCCESS = 0.55      # containment without diagnosis
SKILL_DECAY = 0.35             # proportional loss of readiness at full automation
CAPABILITY_GRID = np.round(np.linspace(0.50, 0.99, 50), 4)
DEPENDENCE_GRID = np.round(np.linspace(0.0, 0.95, 40), 4)
ROUTINE_SHARES = (0.0, 0.25, 0.50, 0.75, 0.90)
N_INCIDENTS = 200_000
DIFFICULTY_SHAPE = 1.6


def _conditional(success: float, shared: float) -> float:
    """Success given that the primary failed, discounted by shared failure."""
    return success * (1.0 - shared)


def run_fallback() -> dict:
    human = _conditional(BASE_HUMAN_SKILL, HUMAN_SHARED_FAILURE)
    surface = []
    for kappa in CAPABILITY_GRID:
        row = []
        for rho in DEPENDENCE_GRID:
            second = _conditional(float(kappa), float(rho))
            best = max((human, "human"), (second, "second system"),
                       (SAFE_STATE_SUCCESS, "safe state"))
            row.append(best[1])
        surface.append(row)
    human_cells = sum(r.count("human") for r in surface)
    total_cells = len(CAPABILITY_GRID) * len(DEPENDENCE_GRID)

    # at each dependence level, the capability at which the second system wins
    crossovers = []
    for rho in DEPENDENCE_GRID:
        need = human / (1.0 - rho) if rho < 1.0 else float("inf")
        crossovers.append({"dependence": float(rho),
                           "capability_needed": need,
                           "reachable": need <= 1.0})
    reachable = [c for c in crossovers if c["reachable"]]
    max_dependence = max(c["dependence"] for c in reachable)

    # what deskilling does to the same boundary
    decay = []
    for share in ROUTINE_SHARES:
        skill = BASE_HUMAN_SKILL * (1.0 - SKILL_DECAY * share)
        h = _conditional(skill, HUMAN_SHARED_FAILURE)
        need_at_half = h / (1.0 - 0.5)
        decay.append({"routine_automated": share, "human_conditional": h,
                      "capability_needed_at_half_dependence": need_at_half,
                      "human_beats_safe_state": h > SAFE_STATE_SUCCESS})
    first_loss = next((d["routine_automated"] for d in decay
                       if not d["human_beats_safe_state"]), None)

    # the confound: automation removes easy cases, competence held fixed
    rng = np.random.default_rng(SEED + 5)
    difficulty = rng.gamma(DIFFICULTY_SHAPE, 1.0, N_INCIDENTS)
    resolution = 1.0 + 2.5 * difficulty      # hours, competence fixed by construction
    baseline = float(resolution.mean())
    selection = []
    for share in ROUTINE_SHARES:
        cut = float(np.quantile(difficulty, share)) if share > 0 else -np.inf
        remaining = resolution[difficulty > cut]
        selection.append({"routine_automated": share,
                          "mean_hours": float(remaining.mean()),
                          "rise_over_baseline": float(remaining.mean() / baseline)})
    # the same cohort, competence degraded, on the unselected case mix
    degraded = []
    for share in ROUTINE_SHARES:
        slow = 1.0 / (1.0 - SKILL_DECAY * share)
        degraded.append({"routine_automated": share,
                         "mean_hours": baseline * slow,
                         "rise_over_baseline": slow})
    at_75 = next(s for s in selection if s["routine_automated"] == 0.75)
    deg_75 = next(d for d in degraded if d["routine_automated"] == 0.75)
    selection_share = ((at_75["rise_over_baseline"] - 1.0)
                       / ((at_75["rise_over_baseline"] - 1.0)
                          + (deg_75["rise_over_baseline"] - 1.0)))

    return {
        "human_conditional": human,
        "safe_state": SAFE_STATE_SUCCESS,
        "capability_grid": CAPABILITY_GRID.tolist(),
        "dependence_grid": DEPENDENCE_GRID.tolist(),
        "surface": surface,
        "human_optimal_cells": human_cells, "total_cells": total_cells,
        "human_optimal_share": human_cells / total_cells,
        "crossovers": crossovers,
        "max_dependence_a_second_system_can_carry": max_dependence,
        "capability_needed_at_half_dependence":
            next(c["capability_needed"] for c in crossovers
                 if abs(c["dependence"] - 0.4872) < 1e-3),
        "decay": decay,
        "routine_share_at_which_a_person_loses_to_containment": first_loss,
        "selection": selection, "degradation": degraded,
        "baseline_hours": baseline,
        "selection_rise_at_75": at_75["rise_over_baseline"],
        "degradation_rise_at_75": deg_75["rise_over_baseline"],
        "selection_share_of_observed_rise": selection_share,
        "n_incidents": N_INCIDENTS,
    }


def run() -> dict:
    alloc = run_allocation()
    rem = run_remainder()
    fall = run_fallback()

    grid = {(g["turnover"], g["sweep"]): g for g in rem["grid"]}
    dec = {d["routine_automated"]: d for d in fall["decay"]}
    sel = {s["routine_automated"]: s for s in fall["selection"]}

    checks = {
        # 1. allocation
        "shares_sum_to_one": all(abs(r["shares_sum"] - 1.0) < 1e-9
                                 for r in alloc["rows"]),
        "eighty_one_to_one_without_pooling":
            abs(alloc["ratio_no_pooling"] - 81.0) < 1e-9,
        "nine_to_one_at_half_pooling":
            abs(alloc["ratio_half_pooling"] - 9.0) < 1e-9,
        "one_to_one_at_full_pooling":
            abs(alloc["ratio_full_pooling"] - 1.0) < 1e-9,
        "tenfold_output_leaves_housing_quantities_untouched":
            abs(alloc["scaled"]["housing_top"] - alloc["rows"][0]["housing_top"]) < 1e-9
            and abs(alloc["scaled"]["housing_rest"]
                    - alloc["rows"][0]["housing_rest"]) < 1e-9,
        "the_housing_price_takes_the_increase_instead":
            abs(alloc["scaled"]["price_of_housing"]
                - OUTPUT_MULTIPLIER * alloc["rows"][0]["price_of_housing"]) < 1e-9,
        "every_distribution_is_supportable_by_some_ownership":
            alloc["max_support_error"] < 1e-12,

        # 2. the remainder
        "closed_form_matches_the_simulation": rem["max_closed_form_error"] < 0.01,
        "the_share_falls_as_capability_sweeps_faster": all(
            grid[(0.05, SWEEP_RATES[i + 1])]["closed_form"]
            < grid[(0.05, SWEEP_RATES[i])]["closed_form"]
            for i in range(len(SWEEP_RATES) - 1)),
        "the_share_rises_with_task_turnover": all(
            grid[(TURNOVER[i + 1], 0.20)]["closed_form"]
            > grid[(TURNOVER[i], 0.20)]["closed_form"]
            for i in range(len(TURNOVER) - 1)),
        "the_arrival_rate_cancels": rem["arrival_spread"] < 1e-3,
        "the_frontier_is_never_empty": rem["frontier_never_empty"],
        "a_noncognitive_requirement_raises_the_limit":
            rem["share_with_ten_percent_atom"] > rem["share_without_atom"] * 2,
        "without_one_the_share_is_small": rem["share_without_atom"] < 0.06,

        # 3. the fallback
        "a_person_is_usually_the_right_fallback":
            fall["human_optimal_share"] > 0.80,
        "but_not_always": fall["human_optimal_share"] < 1.0,
        "a_second_system_has_to_be_independent":
            fall["max_dependence_a_second_system_can_carry"] < 0.50,
        "deskilling_crosses_containment_at_half_automation":
            fall["routine_share_at_which_a_person_loses_to_containment"] == 0.5,
        "a_degraded_responder_falls_below_containment":
            not dec[0.75]["human_beats_safe_state"]
            and dec[0.0]["human_beats_safe_state"],
        "selection_alone_raises_resolution_time":
            sel[0.75]["rise_over_baseline"] > 1.5,
        "selection_is_monotone_in_automation": all(
            sel[ROUTINE_SHARES[i + 1]]["rise_over_baseline"]
            > sel[ROUTINE_SHARES[i]]["rise_over_baseline"]
            for i in range(len(ROUTINE_SHARES) - 1)),
        "selection_dominates_degradation":
            fall["selection_share_of_observed_rise"] > 0.60,
    }
    bad = [k for k, v in checks.items() if not v]
    if bad:
        raise AssertionError("invariants failed: " + ", ".join(bad))

    return _py({"allocation": alloc, "remainder": rem, "fallback": fall,
                "checks": {k: bool(v) for k, v in checks.items()},
                "seed": SEED})
