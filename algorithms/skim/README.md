# Algorithm: skim

Applies the offline Omega_c -> (Xi_c+ K-) selection to the raw LHCb Open Data
ntuples and writes one `*.skim.root` file per input file into `stageout/`.

Ported from `src/skim.py` of the omegac_resonances_snakemake project.

## Parameters

- `raw_source`: local directory, ROOT file, or xrootd directory with the raw ntuples
  (default: the LHCb Open Data real-production EOS directory)
- `max_files`: limit the number of input files; `0` means all files

## Outputs

- `stageout/*.skim.root` — skimmed `DecayTree/DecayTree` ntuples

Downstream tasks mount this task's output with alias `skimdata` and read the
skimmed files from `skimdata/stageout`.
