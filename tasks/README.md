# tasks

Executable task instances of the Omega_c resonance analysis workflow:

```
skim ──┬──> skim_plots
       └──> sweight ──> fit
```

- `skim` reads the raw LHCb Open Data ntuples (`max_files=0` processes all
  files; use `max_files=1` for a quick test)
- `skim_plots` and `sweight` consume the skimmed ntuples via alias `skimdata`
- `fit` consumes the weighted ntuple via alias `sweightdata`

Submit from any task directory with `celebi-cli submit`; dependencies are
resolved automatically.
