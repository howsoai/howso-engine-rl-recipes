# Provenance Notes

## Repository & Commit
- Repo: howso-engine-rl-recipes (local workspace)
- Commit: 17682eb158b737b229e881b64d6ec0b6bfb8bb5b (HEAD during analysis)

## Environment
- OS: Linux 5.15.167.4-microsoft-standard-WSL2 (x86_64)
- Python: 3.12.7 (virtualenv `.venv`)
- Key packages: howso-engine-rl-recipes (editable), howso-engine 48.1.1, gymnasium 1.2.1, pandas 2.3.3, pdfminer.six 20250506, pdfplumber 0.11.7.

## Commands Executed
- Dependency install: `python -m venv .venv && source .venv/bin/activate && pip install -e .[dev]`
- CartPole sweeps: `python -m howso_engine_rl_recipes cartpole --iterations 5 --workers 1 --log-level WARNING` (additional single-run probes for sanity).
- WTM sweeps: `python -m howso_engine_rl_recipes wtm --iterations 20 --workers 1 --log-level WARNING`.
- Log capture: outputs saved to `rl_results_cartpole.log` and `rl_results_wtm.log`.
- Literature downloads: `curl` on Shaikh et al. (2019) project report and Bontrager et al. (2019) AAAI paper; extraction via `pdfminer.six`/`pdfplumber`.
- CI artifact review: downloaded Linux trace from run 18333159956 using GitHub CLI (`gh run download ...`).

## Artifacts Produced
- Raw per-seed CSVs: `rl_results/our_results/cartpole_runs.csv`, `rl_results/our_results/wtm_runs.csv`.
- Summaries: `rl_results/our_results/summary_cartpole.csv`, `summary_wtm.csv`, `summaries.json`.
- Literature tables & quote bank under `rl_results/literature/`.
- Final tables for paper body & appendix under `rl_results/final_tables/`.

## Caveats & TODOs
- CartPole comparators currently rely on a 2019 course project (Shaikh et al.); additional peer-reviewed baselines (e.g., PPO, DQN) should be sourced to strengthen coverage.
- WTM literature limited to Bontrager et al. (2019); seek supplementary GVGAI competition reports if available.
- No CI nightly artifacts beyond Linux trace inspected due to time; Mac/Windows traces still available for cross-check.
