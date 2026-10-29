# Algorithm: sweight

Fits the Xi_c+ mass spectrum (Double Crystal Ball signal + exponential
background, extended unbinned fit with zfit) and computes signal sWeights,
which are stored together with the masses in a weighted ROOT file.

Ported from `src/sweight.py` of the omegac_resonances_snakemake project.

## Inputs

Expects an upstream `skim` task mounted with alias `skimdata`. The skimmed
files are read from `skimdata/${skim_dir}` (default `skimdata/stageout`).

## Parameters

- `skim_dir`: directory of skimmed ROOT files, relative to the `skimdata` mount
- `max_files`: limit the number of skimmed files read; `0` means all files

## Outputs

- `stageout/omegac2xicK.root` — masses plus `sweight_signal`/`sweight_background` branches
- `stageout/sweight/xic_fit.png` — Xi_c+ fit with pull distribution
- `stageout/sweight/omega_weighted.png` — sWeighted Omega_c0 spectrum
