# Performance Summary — CartPole & Wafer-Thin-Mints

On CartPole-v1 with state observations, our Howso agent reached the environment’s benchmark—an average score of at least 195 over the last 100 episodes—by a median of **273** episodes across five runs (IQR 38) with a 100 % solve rate. For context, a CMU study reported a plain REINFORCE agent needing about **650** episodes to reach the same threshold, improved to roughly **400** episodes when alternating real and learned-dynamics rollouts (Shaikh et al., 2019). On GVGAI Wafer-Thin-Mints, using structured state observations and a 150-round evaluation, our Howso agent achieved an overall median score of **6.59** across 20 runs (70 % win rate; median on wins **6.98**; max 9; median on unsolved runs **4.47**). Bontrager et al. (2019) trained A2C from pixels and found Wafer-Thin-Mints did not converge under their setup, while planning agents using a forward model (such as NovelTS) reached average scores around **8.75** over 150 plays.

## Supporting Data
- `rl_results/our_results/summary_cartpole.csv` — Howso CartPole medians and IQR (GitHub Actions run [18333159956](https://github.com/howsoai/howso-engine-rl-recipes/actions/runs/18333159956) verifies CI environment; local rerun logs `rl_results_cartpole.log`).
- `rl_results/our_results/summary_wtm.csv` — Howso Wafer-Thin-Mints medians, win rate, per-run breakdown (`rl_results_wtm.log`).
- Shaikh et al. (2019), *Towards integrating model dynamics for sample efficient reinforcement learning* — Reports REINFORCE baselines at 650 vs 400 episodes ([PDF](https://sha2nkt.github.io/assets/deep-rl-final.pdf), Fig. 6).
- Bontrager et al. (2019), *“Superstition” in the Network: Deep Reinforcement Learning Plays Deceptive Games* — Notes A2C non-convergence and lists NovelTS/Return42 averages (Table 1, [arXiv:1908.04436](https://arxiv.org/pdf/1908.04436)).
- GitHub Actions trace artifact `traces-Linux-3.12-MT` (run [18333159956](https://github.com/howsoai/howso-engine-rl-recipes/actions/runs/18333159956)) — Captures automated regression runs validating the same agent configuration.

