# Comparability Notes

## CartPole
- **Environment version:** All Howso runs and literature references target Gym CartPole-v1 with state observations (cart position/velocity, pole angle/angular velocity). Our agent follows the default win rule from `howso_engine_rl_recipes/cart_pole/game.py` (average reward ≥195 across 100 consecutive episodes).
- **Observation differences:** The REINFORCE baselines in Shaikh et al. (2019) operate on the same low-dimensional state features; no pixel-based variants are reported.
- **Training horizons:** Howso simulations cap at `max_rounds=1000`; literature baselines report convergence within ≤650 episodes and average over 10 seeds.
- **Algorithm variations:** Shaikh et al. augment REINFORCE with model-generated rollouts, reducing required real episodes. They keep Gym reward structure unmodified.

## Wafer-Thin-Mints
- **Environment version:** Howso uses the GVGAI WaferThinMints level packaged with this repo (`config/latest-mt-*.yml`) and the default `max_rounds=150` baked into `wafer_thin_mint/game.py`.
- **Observation differences:** Howso basic agent consumes structured state counts, whereas Bontrager et al. (2019) train A2C directly from GVGAI pixels and planning agents via forward models. Pixel training struggled to converge on the stochastic level.
- **Solved definition:** Howso treats a "win" as meeting the average score constraint enforced by `GameResult['win']`. Bontrager et al. measure average score over ~150 plays; no explicit win threshold is defined, so comparisons rely on score magnitude (negative values imply frequent busts).
- **Variance considerations:** Our 20-run sweep yields 70% win rate with median score 6.98 (high score 9). Literature averages mix deterministic and stochastic planners; A2C remained negative (-6.21 average), while NovelTS achieved 8.75 despite the same time budget.
