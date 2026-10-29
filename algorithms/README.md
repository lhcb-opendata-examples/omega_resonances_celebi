# algorithms

Reusable algorithm templates for the Omega_c resonance analysis

- `skim` — offline selection on the raw LHCb Open Data ntuples
- `skim_plots` — Xi_c+ / Omega_c0 mass histograms of the skimmed data
- `sweight` — Xi_c+ mass fit and signal sWeight computation
- `fit` — fit of the sWeighted Omega_c0 spectrum (7 excited Omega_c states)

All algorithms run in the
`registry.cern.ch/lhcb-opendata-example-omegac-resonances/omegac-analysis:v1.0.2`
container and write outputs exclusively to `stageout/`.
