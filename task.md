# Howso RL Results Runner Guide — CartPole & Wafer‑Thin‑Mints

**Audience:** Research assistant / agent with no prior context.

**Purpose:** Produce a small, defensible **results pack** for the whitepaper’s RL subsection that anchors **Howso’s RL results** on **CartPole** and **Wafer‑Thin‑Mints (WTM)** against **published baselines**. You are **not** re‑running other people’s methods; you are surfacing their published numbers with citations, and computing our numbers from our own runs/nightlies.

---

## 0) Outcomes (what you must hand back)

1. **Two short tables (for the paper body)** — one for **CartPole**, one for **WTM**:

   * Columns: `Algorithm (ours) • Metric • Our Result • Literature Comparator (range/median) • Sources (IDs)`
   * Keep to 4–6 rows max per env (concise).
2. **Two detailed tables (appendix)** with **literature rows**:

   * Columns: `Algorithm (+version) • Observation type (state/pixels) • “Solved” criterion • Median episodes/steps to solve (N) • Best reachable reward if not solved • Seeds • Year • Paper DOI/URL • Code`
3. **Quote bank (CSV)** of ≤2‑sentence **verbatim quotes** per literature row with **page/fig/section numbers**.
4. **Our‑results sheet** with raw runs for CartPole and WTM, plus computed summary (median, IQR, seeds).
5. **Provenance note** (1 page): repos/commit hashes, environment, commands, config, and any caveats.

> If any field is unknown, leave it blank and add a TODO line in the Provenance note. Do **not** invent values.

---

## 1) Scope at a glance

* **Environments:** `CartPole`, `Wafer‑Thin‑Mints (WTM)`.
* **Goal:** Compare **Howso RL** sample‑efficiency/learning speed to published baselines via tables + quotes.
* **We do run:** Howso RL (our method) on both envs, if runs aren’t already available as nightlies.
* **We do not run:** External baselines (DQN, PPO, etc.). We cite their numbers from papers.

---

## 2) Definitions you’ll use

* **Solved (CartPole)**: Commonly defined as **average reward ≥ 195 over 100 consecutive episodes** in OpenAI Gym v0/v1. Some papers use slight variants (note exactly what each paper says). You must record **their definition verbatim**.
* **Solved (WTM)**: Definition varies; collect each paper’s criterion. If a paper says it could **not** solve WTM, record best achievable score and say **“not solved”**.
* **Sample efficiency**: Use what the paper reports (episodes/steps to threshold). Prefer **median** over mean; if only mean available, note it.
* **Observation type**: `state` vs `pixels` — matters for comparability.

---

## 3) Access & setup (our side)

> If access fails at any step, stop and log a TODO in **Provenance note**.

1. **Repos & artifacts**

   * `howso-internal-recipes` (for shared infra and prior examples, if applicable).
   * RL runs/nightlies repo or storage path for **Howso RL** (ask maintainer to share).
2. **Environment**

   * Python 3.10+ (or the version specified by the maintainer).
   * Package manager: `pip` or `poetry` as per repo README.
3. **Credentials**

   * Any tokens/keys needed for artifact access (nightly store / object storage).

Record: repo URLs, branch names, commit hashes, and exact commands you ran in the **Provenance note**.

---

## 4) Producing **our** results

### 4.1 If nightlies already exist

1. Locate the latest **CartPole** and **WTM** runs. Copy their raw logs/metrics.
2. Extract for each env:

   * **Solve time** (episodes/steps) if solved; else **best mean reward** and **training horizon**.
   * **Seeds** and **N** (number of runs).
3. Summarize:

   * **Median** episodes/steps to solve (plus IQR). If not solved, best reward ± sd.
   * Number of seeds and environment version.
4. Save to **Our‑results sheet** (one tab per env). Link the raw files.

### 4.2 If you need to run Howso RL

1. Use the maintainer’s script/entrypoint to run **K seeds** (target ≥5) per env.
2. Fixed configuration:

   * Same environment version across seeds (record `v0`/`v1`, action space, observation type).
   * Same training horizon and evaluation protocol across seeds.
3. Capture artifacts per run:

   * Seed, episodes/steps to solve (or `None`), per‑episode rewards, wall‑time, machine info.
4. Aggregate into **Our‑results sheet**; produce the same summary as above.

> If you changed any default, log it in **Provenance note**.

---

## 5) Literature sweep (CartPole & WTM)

> You are collecting **papers’ numbers and quotes** — no experiments.

1. Search (Scholar/arXiv): terms like `CartPole sample efficiency`, `episodes to solve CartPole`, `Wafer‑Thin‑Mints reinforcement learning`, `benchmark`, `steps to solve`, plus algorithm names (DQN, PPO, A2C, SAC, Rainbow, etc.). Include `“openai gym v1”` or env versions if stated.
2. Inclusion rules:

   * Prefer **peer‑reviewed** or well‑cited arXiv with code.
   * Extract only what’s **explicitly claimed** (episodes/steps, solved thresholds, seeds).
   * Record **env version** and **observation type**.
3. For each paper, fill a row in the **detailed table** (appendix) and add a **quote** to the **quote bank** with page/fig/section numbers.
4. If multiple strong sources disagree, keep **both** and note differences (env version, reward shaping, termination rule, sticky actions, etc.).

**Deliverable sanity:** each literature row must have **(a)** a numeric claim, **(b)** a source link/ID, **(c)** a ≤2‑sentence quote with a page/figure reference.

---

## 6) Build the final tables

### 6.1 Short table (body) — per environment

Columns:

* `Algorithm (ours)` → e.g., **Howso RL (state)**
* `Metric` → Episodes to solve (median, N) **or** Best reward @ horizon
* `Our Result` → e.g., **312 (N=5, v1)**
* `Literature Comparator (range/median)` → e.g., **PPO 450–800; DQN 1000–>2000**
* `Sources (IDs)` → paper IDs from your appendix table

### 6.2 Detailed table (appendix) — per environment

Columns:
`Algorithm (+version) • Obs type • “Solved” definition • Median episodes/steps (N) • Training compute (if stated) • Seeds • Paper (DOI/URL) • Code • Year • Notes`

> If a paper reports **not solved**, record the best reported reward and the training horizon.

---

## 7) Quote bank (strict format)

Create a CSV with columns:
`env • algorithm • exact_quote • where (page/fig/section) • DOI/URL • notes`

Rules:

* ≤2 sentences per entry; verbatim; include page/fig/section.
* Only quotes that **state the metric/claim** (episodes/steps or best reward and the threshold).

---

## 8) Comparability notes (per environment)

Create a short paragraph covering:

* **Env version** (v0/v1), observation type (state/pixels), action space.
* **Solved threshold** used by each cited work.
* **Evaluation protocol** (averaging window, episode length cap, training horizon, sticky actions if any).
* Any **reward shaping** or implementation quirks.

> Purpose: make it clear why a number from paper A may not match paper B.

---

## 9) Provenance & reproducibility (1 page)

* **Repos/paths:** all sources you touched.
* **Commits:** hashes for our code and any evaluation scripts.
* **Environment:** OS, Python, key package versions.
* **Commands:** the exact commands you ran for our RL runs.
* **Artifacts:** where raw logs live; checksums if files are large.
* **Caveats:** any unknowns or deviations from defaults.

---

## 10) File/Folder layout (suggested)

```
rl_results/
  our_results/
    cartpole_runs.csv
    wtm_runs.csv
    summary_cartpole.csv
    summary_wtm.csv
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
```

---

## 11) Quality bar & Go/No‑Go

* **Green (use in paper):** Our results summarized (median + N), at least **two** credible literature comparators per env with quotes and page refs, comparability notes present.
* **Yellow (mention only):** Our numbers OK but only **one** comparator or fuzzy thresholds → keep in text, skip detailed table.
* **Red (omit):** Missing comparators **and** unclear solve definitions.

---

## 12) FAQ

**Q: Do I need to run PPO/DQN?**
A: **No.** You only collect their published numbers with sources/quotes.

**Q: What if our runs don’t solve?**
A: Report **best reward** and horizon; still anchor against papers that also didn’t solve or took long.

**Q: What if papers disagree on CartPole’s “solved” threshold?**
A: Record each definition verbatim; our comparability notes will explain the variance.

---

## 13) Checklists

**Our results (per env)**

* [ ] Found/ran N≥5 seeds
* [ ] Recorded env version
* [ ] Computed median episodes/steps (or best reward)
* [ ] Saved per‑seed CSV
* [ ] Wrote summary CSV

**Literature**

* [ ] ≥2 strong sources per env
* [ ] Quote with page/fig/section
* [ ] Env version + solved threshold captured
* [ ] Added to appendix table

**Finalization**

* [ ] Body tables filled (≤6 rows)
* [ ] Appendix tables exported
* [ ] Quote bank complete
* [ ] Comparability notes present
* [ ] PROVENANCE.md updated

---

## 14) Hand‑off note for the whitepaper author

When the above is complete, the author will:

* Insert the **two short tables** in the Results section and cite the sources by ID.
* Include the **appendix tables** and the **quote bank** as supplemental material or footnoted references.
* Add a 1–2 sentence comparison line per environment (e.g., “Howso RL solves CartPole in **X** episodes (median over **N** seeds), consistent with/competitive against PPO/DQN ranges reported in [S1–S3]”).

