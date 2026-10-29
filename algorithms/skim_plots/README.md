# Algorithm: skim_plots

Builds the Xi_c+ and Omega_c0 mass histograms from the skimmed ntuples.

Ported from `src/skim_plots.py` of the omegac_resonances_snakemake project.

## Inputs

Expects an upstream `skim` task mounted with alias `skimdata`. The skimmed
files are read from `skimdata/${skim_dir}` (default `skimdata/stageout`).

## Parameters

- `skim_dir`: directory of skimmed ROOT files, relative to the `skimdata` mount
- `max_files`: limit the number of skimmed files read; `0` means all files

## Outputs

- `stageout/xic_mass.png` — Xi_c+ mass spectrum
- `stageout/omega_c_mass.png` — Omega_c0 mass spectrum
