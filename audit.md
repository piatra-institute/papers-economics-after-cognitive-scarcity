# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-05 — v1, complete

Scope: the whole paper, the three benchmarks, and the evidence base, from the
seed chat to the built PDF and the bound claim ledger.

Changes:
  - Bibliography built as CSL records in `references.yaml` with Pandoc `[@id]`
    citations; 18 entries, all resolved against Crossref. Two seed locators were
    corrected: Nilsson is the 1985 *Human Systems Management* article rather than
    a 1984 *AI Magazine* one, and Marschak resolves to the 1968 report rather
    than the 1966 title the seed gave.
  - The seed's twelve-period optimisation with synthetic coefficients was not
    used. Coefficients invented for abstract periods produce numbers with no
    interpretation; the three benchmarks kept here each have an exact solution or
    a closed-form limit that can be stated without a calibration.
  - The paper's central result is not in the seed. The seed identified the
    logical gap between "at every date there is human-advantaged work" and "there
    is permanently human-advantaged work" and left it there. Formalising it gives
    a limit, δ/(a+δ), that the simulation reproduces to 5.50e-5, and the
    cancellation of the arrival rate, which is the finding that most directly
    answers the reassurance that new work will appear.
  - The fallback plane, the containment crossing at 50 percent automation, and
    the decomposition of an observed resolution-time rise into case mix and skill
    loss are also new here. The seed argued the case-mix confound as a criticism;
    quantifying it at 71 percent turns it into a control someone can run.
  - Source review changed the manuscript. A sentence attributing a specific
    experimental finding to Endsley and Kiris was weakened to what the article's
    title and subject establish, because the full text could not be retrieved
    from the publisher, Semantic Scholar or Europe PMC. The failure and the
    resulting change are recorded in `claims.yaml` and `sources.md` rather than
    being papered over.
  - The historical complaint that nobody imagined machine-dominated production is
    explicitly declined in the text, with Simon, Marschak, Nilsson, Romer and
    Meade cited against it, because it is false and would let the substantive
    argument be dismissed on a priority claim.
  - Editorial: ten voice diagnostics were reported; four were rewritten as
    positive declaratives and six kept, with reasons in `editorial.md`. The
    abstract is 242 words.

Verification:
  - references: 18 cited IDs resolve to 18 entries — PASS
  - claims: 22 bound claims, 17 computations against JSON pointers, 3 source
    claims with verification notes, 3 assumption and interpretation claims —
    all PASS; coverage stamped against this manuscript's sha256
  - execution: `verification/benchmarks.json`, exit 0, artifact hash recorded
  - simulation: 22/22 invariants
  - build: 9 pages, no missing-character warnings, manifest hashes match
  - editorial and visual: version-bound records, all 9 pages inspected — PASS
  - `papers check --stage local` => PASS
