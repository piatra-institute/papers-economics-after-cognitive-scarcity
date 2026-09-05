# Sources

The frozen bibliography lives in `references.yaml` as CSL records with stable
IDs; the manuscript cites them with Pandoc `[@id]` syntax. This file records
provenance. Support for particular assertions is bound in `claims.yaml`.

## Provenance

All eighteen entries were resolved against Crossref during this pass, with the
locators in the CSL records taken from those responses.

- `acemoglu2018`, `autor2015`, `ostrom2010` — Crossref, AEA journals.
- `bainbridge1983`, `endsley1995` — Crossref. See the note below on `endsley1995`.
- `growiec2023` — Crossref, DOI 10.33119/kaewps2023091. A working paper, and
  labelled as such in the bibliography.
- `lucas1976`, `myerson1983`, `romer1990`, `sen1999`, `turing1950`, `yokoo2004`
  — Crossref, journal records.
- `marschak1968` — Crossref, DOI 10.21236/ad0668496. A technical report; the
  seed cited a 1966 title, and the resolvable record is the 1968 one used here.
- `meade1993`, `tullock2001` — Crossref, book chapters. Both are reprints of
  earlier work and are cited in the form that resolves.
- `nilsson1985` — Crossref, DOI 10.3233/hsm-1985-5205. The seed's 1984 *AI
  Magazine* attribution does not resolve; the *Human Systems Management* article
  does and is what is cited.
- `simon1960` — Crossref, DOI 10.1037/13978-000, for the book.
- `trammell2026` — Crossref, *Annual Review of Economics* 18(1), 589–611.

## Unverified support

`endsley1995` is cited for the existence and subject of the out-of-the-loop
performance problem, which its title establishes. The full text and abstract
could not be retrieved: the publisher returns 403, and neither Semantic Scholar
nor Europe PMC holds an abstract. An earlier draft attributed a specific
experimental finding to it; that sentence was rewritten. The claim ledger records
the failure and the resulting change.

## Not cited

The seed referred to work by Hadfield and Koh on agent economies and to a
Brookings paper on AI public finance. Neither was resolved to a stable locator in
this pass and no claim here depends on either, so both are omitted rather than
cited unverified.
