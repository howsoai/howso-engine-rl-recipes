import logging
import os
from pathlib import Path


def pytest_configure(config):
    """Create one log file for each worker with pytest-xdist."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    log_file = config.getoption("log_file")
    if worker_id is not None and log_file:
        filepath = Path(log_file)
        logging.basicConfig(
            format=config.getoption("log_file_format") or config.getini("log_file_format"),
            filename=Path(filepath.parent, f"{worker_id}_{filepath.name}"),
            level=(config.getoption("log_file_level") or "INFO").upper(),
        )
