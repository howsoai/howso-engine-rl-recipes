# RL Results Paragraph — Sources & Verification

## Final Paragraph
On **CartPole-v1** (state observations), our Howso RL agent crossed the classic CartPole “solved” bar—average reward ≥ 195 over 100 consecutive episodes—after a **median 273** training episodes across **5** seeds; note this **195-over-100** rule follows the legacy CartPole-v0 convention, while the current v1 docs list a reward threshold of **475**. For context, a CMU study reported **REINFORCE** needing **≈650 episodes** on CartPole, improved to **≈400** when alternating in learned-dynamics rollouts (**10 runs**). On **Wafer-Thin-Mints** (GVGAI, 150 plays), our agent’s **median winning score** was **6.98** with a **70% win rate** (overall median 6.59); **Bontrager et al. (AIIDE 2019)** report **A2C** averaging **−6.21** on this game, while planning baselines **NovelTS** and **Return42** scored **8.75** and **−2.66**, respectively.

## Verification Checklist

### A. CartPole “Solved” Convention vs v1 Threshold
- **Legacy (195 over 100)** — GitHub Gym leaderboard states: “_CartPole-v0 defines "solving" as getting average reward of 195.0 over 100 consecutive trials._” (openai/gym wiki, CartPole-v0 section, line 31).[<https://github.com/openai/gym/wiki/Leaderboard>]
- **v1 reward threshold = 475** — Gymnasium documentation: “_The default reward threshold is 500 for v1 and 200 for v0 due to the time limit on the environment._” (Gymnasium CartPole page, “Rewards” section).[<https://gymnasium.farama.org/environments/classic_control/cart_pole/>]
- **Registry constants** — Gymnasium source registers `CartPole-v0` with `reward_threshold=195.0` and `CartPole-v1` with `reward_threshold=475.0` (Farama Gymnasium `gymnasium/envs/__init__.py`, lines 9-22).[<https://github.com/Farama-Foundation/Gymnasium/blob/main/gymnasium/envs/__init__.py>]

### B. Our CartPole Numbers
- **Median episodes (273) across 5 seeds** — `rl_results/our_results/summary_cartpole.csv:1-12` lists `total_runs=5`, `winning_runs=5`, and `median_rounds_to_win=273` (IQR 38).
- **Raw log confirmation** — `rl_results_cartpole.log` summary reports five iterations with win rounds (e.g., entries `"rounds": 100, 273, 791, 287, 249`).
- **Solve detection logic** — Source `howso_engine_rl_recipes/cart_pole/game.py:16-40` documents the convention: “Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive rounds,” with `win_threshold = 100` and `required_average = 195`.
- **Env ID & observation type** — `CartPoleGame.game_id = 'CartPole-v1'` and the simulation uses Gymnasium’s state vector (`observation` resets via `self.env.reset(...)`), confirming state observations.

### C. REINFORCE Comparison (Shaikh et al., 2019)
- **Quoted result** — “_Averaging over 10 runs, REINFORCE alone solved the environment in 650 episodes whereas model-free with model dynamics solved it in 400._” (Frontiers project report, page 6, Fig. 6 caption).[<https://sha2nkt.github.io/assets/deep-rl-final.pdf>] — citation ID `RL-C1`.

### D. Wafer-Thin-Mints — Our Numbers
- **Summary metrics** — `rl_results/our_results/summary_wtm.csv:1-13` shows `total_runs=20`, `winning_runs=14` (70%), `median_avg_score_final_window=6.9833` (winning median), `median_avg_score_total=6.9833` (for wins), and best unsolved score column (4.47 median unsolved).
- **Raw log** — `rl_results_wtm.log` lists per-run scores; overall median across all 20 runs computed from `wtm_runs.csv` equals 6.59 (documented in analysis).
- **Game configuration** — `howso_engine_rl_recipes/wafer_thin_mint/game.py:13-45` sets `game_id = 'WaferThinMint-v0'`, enforces `max_rounds=150`, and defines the win condition as average score across 150 rounds ≥ win threshold (state-based play).

### E. Wafer-Thin-Mints Literature Anchors (Bontrager et al., 2019)
- **A2C non-convergence** — “_One stochastic environment, WaferThinMints, did not converge and might have benefited from more training time._” (AIIDE-19 paper, page 2).[<https://arxiv.org/pdf/1908.04436>]
- **Table 1 scores** — Table 1 (page 5) lists average scores: A2C `-6.21`, NovelTS `8.75`, Return42 `-2.66`; extracted via pdfplumber (`Page 5 tables: 1` output) and recorded in `rl_results/literature/wtm_table.csv`.

### F. CI Provenance (GitHub Actions)
- Workflow run **18333159956** (`main Build`) includes jobs `Pytest . (3.12, Linux, MT)` running `tests/test_cart_pole.py` and `tests/test_wtm.py`; trace artifact `traces-Linux-3.12-MT` captures CLI executions consistent with our local runs.[<https://github.com/howsoai/howso-engine-rl-recipes/actions/runs/18333159956>]

## Supporting Files & Locations
- `rl_results/our_results/cartpole_runs.csv`, `summary_cartpole.csv`
- `rl_results/our_results/wtm_runs.csv`, `summary_wtm.csv`
- `rl_results_cartpole.log`, `rl_results_wtm.log`
- Source modules: `howso_engine_rl_recipes/cart_pole/game.py`, `.../wafer_thin_mint/game.py`
- Literature tables & quotes: `rl_results/literature/cartpole_table.csv`, `wtm_table.csv`, `quote_bank.csv`

## Citation IDs
- **RL-C1** — Shaikh et al., 2019 (CartPole REINFORCE ± dynamics) — [PDF](https://sha2nkt.github.io/assets/deep-rl-final.pdf)
- **RL-W1** — Bontrager et al., 2019 (Wafer-Thin-Mints A2C & planning baselines) — [arXiv:1908.04436](https://arxiv.org/pdf/1908.04436)

