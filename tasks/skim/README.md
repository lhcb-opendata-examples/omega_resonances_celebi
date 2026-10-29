# tasks/skim

The skim stage of the omegac workflow, sharded for parallel execution.

```
skim0 ─┐
skim1 ─┼─> skim (merge)
skim2 ─┘
```

| Object | Type | Role |
|---|---|---|
| `skim0`, `skim1`, `skim2` | task | Run `algorithms/skim` on a slice of the raw EOS file list |
| `alg_combine` | algorithm | Copies the shard stageouts into a single directory |
| `skim` | task | Merge task; mounts the three shards as `skim0` / `skim1` / `skim2` |

Each shard writes one `*.skim.root` per input file into its own `stageout/`.
The merge task `skim` is what downstream tasks (`tasks/skim_plots`,
`tasks/sweight`) depend on — they mount it as `skimdata` and read
`skimdata/stageout`.

## Sharding

The shards slice the sorted input file list with `start_file` / `max_files`
(`max_files=0` means "all remaining files"):

| Task | `start_file` | `max_files` |
|---|---|---|
| `skim0` | 0 | 20 |
| `skim1` | 20 | 20 |
| `skim2` | 40 | 0 (rest) |

To add a shard, create a task, link `../../algorithms/skim`, set its
`start_file` / `max_files`, then add it as an input to `skim` and extend
`alg_combine/combine.sh` with the new alias.

`alg_combine` is deliberately task-local rather than a project-level algorithm:
its `combine.sh` hardcodes the shard aliases, so it is not reusable outside
this directory.
