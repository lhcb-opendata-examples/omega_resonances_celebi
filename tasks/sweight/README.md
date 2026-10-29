# Task: sweight

Runs the `sweight` algorithm on the output of the `skim` task
(input alias `skimdata`): Xi_c+ mass fit and signal sWeights.

## Parameters

- `max_files`: limit the number of skimmed files read; `0` = all

## Outputs

- `stageout/omegac2xicK.root` — weighted ntuple consumed by the `fit` task
- `stageout/sweight/xic_fit.png`, `stageout/sweight/omega_weighted.png`
