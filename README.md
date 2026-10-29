# omegac

Celebi project for the search for excited Omega_c0 states in
Omega_c0 -> (Xi_c+ -> p K- pi+) K- decays using LHCb Open Data.

Migrated from the Snakemake project `omegac_resonances_snakemake`
(see `../omegac_resonances_snakemake`).

## Structure

```
omegac(project)
├── algorithms(directory)      stateless, reusable templates
│   ├── skim
│   ├── skim_plots
│   ├── sweight
│   └── fit
└── tasks(directory)           executable instances
    ├── skim(directory)
    │   ├── alg_combine        task-local algorithm: merges the shard stageouts
    │   ├── skim0 / skim1 / skim2   parallel skim shards
    │   └── skim               merge task (uses alg_combine)
    ├── skim_plots
    ├── sweight
    └── fit
```

The skim stage is sharded across three tasks that each process a slice of the
input file list, then a merge task collects their `stageout/` into a single
directory that the downstream tasks consume.

## Workflow

```
skim0 ─┐
skim1 ─┼─> skim (merge) ─┬─> skim_plots
skim2 ─┘                 └─> sweight ──> fit
```

| Task | Alias for input | What it does | Outputs (`stageout/`) |
|---|---|---|---|
| `skim0/1/2` | — | Offline selection on the raw EOS ntuples (`DecayTree/DecayTree`): vertex chi2/ndf, pT and ProbNN PID cuts, Xi_c+ mass window 2400–2520 MeV. One output file per input file. | `*.skim.root` |
| `skim` | `skim0`, `skim1`, `skim2` | Copies the three shard stageouts into one directory (54 files for the full dataset). | `*.skim.root` |
| `skim_plots` | `skimdata` | Plots the Xi_c+ and Omega_c0 mass spectra (70 bins each; 2430–2520 and 2900–3500 MeV). | `xic_mass.png`, `omega_c_mass.png` |
| `sweight` | `skimdata` | Extended unbinned zfit of M(Xi_c+) over 2430–2510 MeV (double Crystal Ball + exponential), then sWeights via the `sweights` package. | `omegac2xicK.root`, `sweight/xic_fit.png`, `sweight/omega_weighted.png` |
| `fit` | `sweightdata` | iminuit weighted extended fit of the sWeighted m(Xi_c+ K-) spectrum over 2970–3500 MeV: seven relativistic Breit-Wigners (3000, 3050, 3065, 3090, 3119, 3185, 3327 MeV) on a threshold background (threshold fixed at 2965 MeV). 26 free parameters. | `omega_fit.json`, `omega_fit.png`, `omega_fit.minuit.log` |

`omegac2xicK.root` holds a `DecayTree/DecayTree` with the branches
`Lambda_cplus_M`, `Omega_cst0_M`, `sweight_signal` and `sweight_background`.
Note that `Lambda_cplus_M` is the Xi_c+ mass — the stripping line reconstructs
both Lambda_c+ and Xi_c+, and the branch name follows the former.

## Parameters

The skim shards slice the sorted input file list with `start_file` /
`max_files` (`max_files=0` means "all remaining files"):

| Task | `start_file` | `max_files` |
|---|---|---|
| `skim0` | 0 | 20 |
| `skim1` | 20 | 20 |
| `skim2` | 40 | 0 (rest) |

All three read `raw_source =
root://eospublic.cern.ch//eos/opendata/lhcb/CollisionNtuples/OPENDATA.LHCB.MHK4.OQO3/outputs/real-production/`.

For a quick end-to-end test, set a single shard to `max_files=1` and drop the
others; `celebi-cli add-parameter max_files 1` from the task directory.

`skim_plots` and `sweight` take `max_files` (0 = all). `fit` takes
`weighted_file = stageout/omegac2xicK.root`, resolved relative to the
`sweightdata` mount point.

## Environments

| Tasks | Image | Memory |
|---|---|---|
| `skim0/1/2` | `celebichrono/root-xrootd:6.32.02` | 4Gi |
| `skim` (merge) | `celebichrono/root-xrootd:6.32.02` | 256Mi |
| `skim_plots`, `sweight`, `fit` | `celebichrono/lhcb-omegac:v0.4` | 4Gi |

The `lhcb-omegac` image carries ROOT plus zfit, sweights, iminuit and mplhep.

## Running

```bash
cd tasks/fit        # or any task; dependencies resolve automatically
celebi-cli submit   # submits the upstream chain as well
celebi-cli status
```

To change the sharding, adjust `start_file` / `max_files` on the shard tasks
with `celebi-cli add-parameter`; the tasks return to `[new]` and must be
resubmitted along with everything downstream of them.

## Notes

- The Snakemake `run_skim: false` mode (reading pre-skimmed EOS tuples) is
  covered by pointing `skim_plots` / `sweight` at an EOS directory instead of a
  task input — their file-list helper accepts xrootd directories.
- `admin_skim_and_upload.py` was not migrated: it is an admin-only EOS upload
  utility, not part of the analysis DAG.
