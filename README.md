# Economics After Cognitive Scarcity

The Permanent-Remainder Assumption and What Would Have to Be True for It to Hold.

Many arguments about the effect of artificial intelligence on work assume that tasks machines cannot yet perform form a lasting human domain. We call this the permanent-remainder assumption and examine what it requires. Under a counterfactual in which every attainable cognitive service is free and universally available, we solve three benchmark models. In a two-good equilibrium with identical preferences and identical free cognition, the ratio of consumption between two groups is 81 to 1, 9 to 1 or 1 to 1 depending only on ownership and pooling, so equal access to intelligence does not by itself narrow the distribution of consumption. In a task model, the set of tasks held by people can be nonempty at every date while their share of tasks converges to $\delta/(a+\delta)$, where $\delta$ is the rate of task turnover and $a$ the rate at which capability overtakes a new task. This limit does not depend on the rate at which new tasks appear, and it is positive only if some tasks require something other than reasoning. In a model of fallback after automated incident response, a human responder is the best fallback in 84.85 percent of the plane of machine capability and failure independence, and beyond 43.2 percent automation of routine incidents an out-of-practice responder performs worse than simple containment. The models are benchmarks with no prices, investment or empirical calibration.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Twenty-two invariant checks fail the run if broken, among them the exact consumption ratios, the agreement between the closed-form limit and the simulation, the cancellation of the arrival rate across a hundredfold range, the independence a second automated system needs, and the containment crossing. Execution is recorded in `verification/benchmarks.json` and every number quoted in the manuscript is bound to a JSON pointer in `claims.yaml`. Nothing here is calibrated to any real economy.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run `papers build economics-after-cognitive-scarcity`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace docs for the research and writing pipelines.
