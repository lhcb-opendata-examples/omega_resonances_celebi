"""Shared helper to collect ROOT files from local or xrootd sources.

Extracted from the skim script of the omegac_resonances_snakemake project so
that downstream stages (skim_plots, sweight) can resolve skimmed inputs
without importing the skim module itself.
"""

import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def collect_files(source: str, max_files: int) -> list[str]:
    if source.startswith("root://") and source.endswith(".root") and not source.endswith("/"):
        files = [source]
    elif source.startswith("root://"):
        files = collect_xrootd_files(source)
    else:
        path = Path(source)
        if path.is_file():
            files = [str(path)]
        else:
            if not path.is_dir():
                raise NotADirectoryError(f"Input path is not a directory or ROOT file: {source}")

            files = sorted(str(p) for p in path.glob("*.root"))

    if max_files > 0:
        files = files[:max_files]

    if not files:
        raise RuntimeError(f"No ROOT files matched input: {source}")

    return files


def collect_xrootd_files(source: str) -> list[str]:
    parsed = urlparse(source)
    host = parsed.netloc
    directory = parsed.path

    if not host or not directory:
        raise ValueError(f"Invalid xrootd directory: {source}")

    if directory.startswith("//"):
        directory = directory[1:]
    elif not directory.startswith("/"):
        directory = f"/{directory}"

    if shutil.which("xrdfs") is None:
        raise RuntimeError("xrdfs is required to list files from xrootd sources")

    command = ["xrdfs", host, "ls", directory]
    result = subprocess.run(command, check=True, capture_output=True, text=True)

    files = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.endswith(".root"):
            files.append(f"root://{host}//{line.lstrip('/')}")

    return sorted(files)
