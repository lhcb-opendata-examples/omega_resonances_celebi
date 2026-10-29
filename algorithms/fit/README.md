# Algorithm: fit

Fits the sWeighted Omega_c0 mass spectrum with seven Breit-Wigner signal
components (the excited Omega_c states near 3000, 3050, 3065, 3090, 3119,
3185 and 3327 MeV) on top of a threshold background, using iminuit.

Ported from `src/fit.py` of the omegac_resonances_snakemake project.

## Inputs

Expects an upstream `sweight` task mounted with alias `sweightdata`. The
weighted ROOT file is read from `sweightdata/${weighted_file}`
(default `sweightdata/stageout/omegac2xicK.root`).

## Parameters

- `weighted_file`: weighted ROOT file path, relative to the `sweightdata` mount

## Outputs

- `stageout/omega_fit.json` — fitted parameter values and errors
- `stageout/omega_fit.png` — fit plot with per-signal components and pulls
- `stageout/omega_fit.minuit.log` — full Minuit log
