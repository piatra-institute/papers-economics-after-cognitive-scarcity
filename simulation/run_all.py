"""Reproduce every number and both figures.

    cd simulation && uv run run_all.py
"""
from __future__ import annotations

import json
from pathlib import Path

from analyses import run

OUT = Path(__file__).parent / "output"


def main() -> None:
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    results = run()
    (OUT / "results.json").write_text(json.dumps(results, indent=2))

    from figures import plot_allocation, plot_fallback
    plot_allocation(results, str(OUT / "figures" / "allocation.png"))
    plot_fallback(results, str(OUT / "figures" / "fallback.png"))

    A, R, F = results["allocation"], results["remainder"], results["fallback"]
    print("allocation:")
    for row in A["rows"]:
        print(f"  pooling {row['pooling']:.1f}: {row['consumption_top']:.3f} against "
              f"{row['consumption_rest']:.3f}, ratio {row['ratio']:.0f}:1")
    print(f"  tenfold output: housing per person unchanged at "
          f"{A['scaled']['housing_top']:.2f} and {A['scaled']['housing_rest']:.3f}; "
          f"housing price {A['scaled']['price_of_housing']:.1f}")
    print("remainder:")
    print(f"  closed form matches simulation to {R['max_closed_form_error']:.2e}")
    print(f"  share at 5% turnover: {R['share_at_turnover_5_sweep_20']:.3f} at a "
          f"five-year sweep, {R['share_at_turnover_5_sweep_100']:.3f} at one year")
    print(f"  arrival rate spans {len(R['arrivals'])} orders of magnitude; share "
          f"spread {R['arrival_spread']:.2e}")
    print(f"  with a tenth of new tasks needing more than reasoning: "
          f"{R['share_with_ten_percent_atom']:.3f}")
    print("fallback:")
    print(f"  a person is optimal in {F['human_optimal_share']:.2%} of the plane; a "
          f"second system needs dependence at or below "
          f"{F['max_dependence_a_second_system_can_carry']:.3f}")
    print(f"  a degraded responder falls below containment at "
          f"{F['routine_share_at_which_a_person_loses_to_containment']:.0%} automation")
    print(f"  at 75% automation, case mix alone raises resolution time "
          f"{F['selection_rise_at_75']:.2f}x; that is "
          f"{F['selection_share_of_observed_rise']:.0%} of the combined rise")
    print("checks:", f"{sum(results['checks'].values())}/{len(results['checks'])}")
    print("wrote", OUT / "results.json")


if __name__ == "__main__":
    main()
