# Economics After Cognitive Scarcity

The Permanent-Remainder Assumption and What Would Have to Be True for It to Hold.
Arguments about what artificial intelligence will do to work keep one thing fixed
while everything else moves: the assumption that whatever machines cannot yet do
is a durable human province. This paper names that assumption and computes what
it would require. Under a counterfactual in which every attainable cognitive
service is free and universally available, three benchmarks are solved. An exact
two-good equilibrium gives consumption ratios of 81 to 1, 9 to 1 or 1 to 1
between the same two groups on the strength of ownership and pooling alone, so
equal intelligence does not narrow the distribution at all, and multiplying
physical output tenfold leaves housing quantities per person exactly where they
were. A task model then separates two propositions the usual argument runs
together: the set of tasks people hold can be nonempty at every date while their
share of tasks converges to a limit that does not depend on how fast new work
appears, and a positive limit requires tasks needing something other than
reasoning. And the argument that automation must leave a human fallback is
vindicated across most of the plane of machine capability and failure
independence, bounded in a computable region, and overtaken by plain containment
once half of routine incidents are automated. A separate calculation shows that
71 percent of any observed rise in human resolution time is case mix rather than
skill loss.

## Simulation

```bash
cd simulation
uv run run_all.py        # -> output/results.json + output/figures/*.png
```

Twenty-two invariant checks fail the run if broken, among them the exact
consumption ratios, the agreement between the closed-form limit and the
simulation, the cancellation of the arrival rate across a hundredfold range, the
independence a second automated system needs, and the containment crossing.
Execution is recorded in `verification/benchmarks.json` and every number quoted
in the manuscript is bound to a JSON pointer in `claims.yaml`. Nothing here is
calibrated to any real economy.

## Build

```bash
uv run build.py          # -> paper/PAPER.pdf  (vendored canonical recipe)
```

Requires `pandoc` and `xelatex` on PATH. From the workspace you can also run
`papers build economics-after-cognitive-scarcity`.

Part of [piatra-papers](https://github.com/piatra-institute). See the workspace
docs for the research and writing pipelines.
