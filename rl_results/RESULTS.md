# Howso RL Results Pack — CartPole & Wafer-Thin-Mints

## 1. Our Run Summaries

**CartPole (Gym CartPole-v1, state observations)**
- Runs: 5 (basic Howso agent, default config)
- Win rate: 100%
- Median episodes to solve: **273** (IQR 38)
- Median high score: 500
- Median total cases: 26 564
- Source log: `rl_results_cartpole.log`

**Wafer-Thin-Mints (GVGAI level, structured state)**
- Runs: 20 (basic Howso agent, default max_rounds=150)
- Win rate: 70% (14/20)
- Median score across winning runs: **6.98** (high score 9)
- Non-winning best score: 9 (median average score 4.47)
- Source log: `rl_results_wtm.log`

Raw per-seed data live in `rl_results/our_results/{cartpole,wtm}_runs.csv`; summaries in `rl_results/our_results/summary_*.csv`.

## 2. Paper Body Tables

### CartPole

| Algorithm (ours) | Metric | Our Result | Literature Comparator (range/median) | Sources |
| --- | --- | --- | --- | --- |
| Howso RL (basic, state) | Episodes to reach Gym solve (median, N=5) | 273 (IQR 38; CartPole-v1) | REINFORCE baseline 650; REINFORCE + learned dynamics 400 | RL-C1 |

### Wafer-Thin-Mints

| Algorithm (ours) | Metric | Our Result | Literature Comparator (range/median) | Sources |
| --- | --- | --- | --- | --- |
| Howso RL (basic) | Avg. score @ 150 rounds (median of winning runs, N=14/20) | 6.98 (high score 9; win rate 70%) | A2C −6.21; NovelTS 8.75; Return42 −2.66 | RL-W1 |

## 3. Appendix Tables

### CartPole Literature (RL-C1)

| Algorithm (+version) | Observation type | “Solved” definition | Median episodes/steps to solve (N) | Training compute | Seeds | Year | Paper | Code | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REINFORCE (baseline) | state | Average reward ≥195 across 100 episodes (Gym) | 650 episodes (N=10) | — | 10 | 2019 | [Shaikh et al. 2019](https://sha2nkt.github.io/assets/deep-rl-final.pdf) | — | Figure 6a |
| REINFORCE + learned dynamics | state | Same as above | 400 episodes (N=10) | — | 10 | 2019 | [Shaikh et al. 2019](https://sha2nkt.github.io/assets/deep-rl-final.pdf) | — | Figure 6b alternates real & model rollouts |

### Wafer-Thin-Mints Literature (RL-W1)

| Algorithm (+version) | Observation type | “Solved” definition | Median episodes/steps to solve (N) | Training compute | Seeds | Year | Paper | Code | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A2C (OpenAI Baselines) | pixels | Mean score over ~150 GVGAI plays | Avg. score −6.21 (150 games) | ~5M frames (reported) | 5 seeds | 2019 | [Bontrager et al. 2019](https://www.aaai.org/ojs/index.php/AIIDE/article/download/5218/5074) | — | Table 1, Mints column; text notes non-convergence |
| NovelTS planning | state | Same | Avg. score 8.75 (150 games) | N/A (planning) | ~150 plays | 2019 | [Bontrager et al. 2019](https://www.aaai.org/ojs/index.php/AIIDE/article/download/5218/5074) | — | Table 1 |
| Return42 planning | state | Same | Avg. score −2.66 (150 games) | N/A (planning) | ~150 plays | 2019 | [Bontrager et al. 2019](https://www.aaai.org/ojs/index.php/AIIDE/article/download/5218/5074) | — | Table 1 |

## 4. Quote Bank (verbatim ≤2 sentences)

| Env | Algorithm | Quote | Where |
| --- | --- | --- | --- |
| CartPole | REINFORCE (baseline + dynamics) | “Averaging over 10 runs, REINFORCE alone solved the environment in 650 episodes whereas model-free with model dynamics solved it in 400.” | Shaikh et al. 2019, Sec. 4.1 (p.5) |
| Wafer-Thin-Mints | A2C | “One stochastic environment, WaferThinMints, did not converge and might have benefited from more training time.” | Bontrager et al. 2019, Sec. 3 (p.3) |
| Wafer-Thin-Mints | A2C (Table 1) | “A2C 5.0 3.79 2.0 69.6 228.86 -6.21” | Bontrager et al. 2019, Table 1 (p.5) |
| Wafer-Thin-Mints | NovelTS (Table 1) | “NovelTS 2.1 2.0 2.0 4.8 298.51 8.75” | Bontrager et al. 2019, Table 1 (p.5) |
| Wafer-Thin-Mints | Return42 (Table 1) | “Return42 5.0 2.0 2.0 190.12 329.73 -2.66” | Bontrager et al. 2019, Table 1 (p.5) |

(CSV source: `rl_results/literature/quote_bank.csv`.)

## 5. Comparability Notes

**CartPole**
- Env version: Gym CartPole-v1; state vector observations. Howso win rule matches repo default (avg reward ≥195 over 100 consecutive episodes).
- Literature baselines (Shaikh et al.) also operate on state features and report 10-seed medians.
- Training horizon: Howso default `max_rounds=1000`. Baselines converge within ≤650 episodes.

**Wafer-Thin-Mints**
- Env: GVGAI WaferThinMints level bundled here with `max_rounds=150`.
- Observation gap: Howso agent uses structured counts; Bontrager et al. train A2C from pixels, while NovelTS/Return42 rely on forward-model planning.
- No explicit “solved” threshold in literature; comparisons rest on average score across ~150 plays. Negative mean indicates busting the mint limit.

(Full text in `rl_results/literature/notes_comparability.md`.)

## 6. Provenance Snapshot

- Repo commit: 17682eb158b737b229e881b64d6ec0b6bfb8bb5b
- OS: Linux 5.15.167.4-microsoft-standard-WSL2 (x86_64)
- Python: 3.12.7 (venv `.venv`)
- Key commands:
  - `pip install -e .[dev]`
  - `python -m howso_engine_rl_recipes cartpole --iterations 5 --workers 1 --log-level WARNING`
  - `python -m howso_engine_rl_recipes wtm --iterations 20 --workers 1 --log-level WARNING`
  - Literature downloads via `curl`; parsing with `pdfminer.six` / `pdfplumber`.
- Artifacts: GitHub Actions run 18333159956 traces (Linux) inspected; macOS/Windows artifacts available but not processed yet.

See `rl_results/PROVENANCE.md` for exhaustive details and caveats (e.g., need additional CartPole baselines, potential CI artifact cross-check).

## 7. Directory Map

```
rl_results/
  our_results/
    cartpole_runs.csv
    wtm_runs.csv
    summary_cartpole.csv
    summary_wtm.csv
    summaries.json
  literature/
    cartpole_table.csv
    wtm_table.csv
    quote_bank.csv
    notes_comparability.md
  final_tables/
    body_cartpole.csv
    body_wtm.csv
    appendix_cartpole.csv
    appendix_wtm.csv
  PROVENANCE.md
  RESULTS.md  ← this file
```

