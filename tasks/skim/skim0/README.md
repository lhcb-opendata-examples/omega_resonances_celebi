# Task: skim

Runs the `skim` algorithm on the raw LHCb Open Data ntuples.

## Parameters

- `raw_source`: EOS xrootd directory with the raw collision ntuples
- `max_files`: `0` = all files; set to e.g. `1` for a quick test

## Outputs

- `stageout/*.skim.root` — skimmed ntuples consumed by `skim_plots` and `sweight`
