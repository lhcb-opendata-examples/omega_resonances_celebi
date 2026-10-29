# alg_combine

Merges the output of the parallel skim shards into a single `stageout/`
directory, so that downstream tasks see one flat set of skimmed files.

`combine.sh` copies `*.root` from each shard mount point:

```bash
cp skim0/stageout/*.root stageout
cp skim1/stageout/*.root stageout
cp skim2/stageout/*.root stageout
```

## Contract

Expects the consuming task to mount three upstream skim tasks under the
aliases `skim0`, `skim1` and `skim2` — see `tasks/skim/skim`. The alias names
are hardcoded in `combine.sh`, so adding or renaming a shard means editing
this script.

Because shard outputs are named after their input file
(`<stem>.skim.root`) and the shards process disjoint slices of the file list,
no filename collisions occur during the copy.

Input: `skim0/stageout/*.root`, `skim1/stageout/*.root`, `skim2/stageout/*.root`
Output: `stageout/*.skim.root`

Runs in `celebichrono/root-xrootd:6.32.02` with a 256Mi limit — it only moves
files, no ROOT processing.
