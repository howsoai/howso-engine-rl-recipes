# RL Results Pack — QC & Redlines (Finalized for Handoff)

**Why this doc exists:** Quick self‑audit of the prior “Clarifying Questions Response,” removal of unverified specifics, and a **sanitized, ready‑to‑send** answer set your agent can use immediately. Anything requiring confirmation is clearly marked.

---

## 1) What’s verified vs. not

### Verified (from this project thread)

* We need **CartPole** and **Wafer‑Thin‑Mints (WTM)** results for Howso and a **literature sweep** for baseline comparisons.
* CI adversarial tests are **regression guards** (not RL); RL nightlies are **owned by Chris**.
* Agent must **not** run external RL baselines; they should **collect** published numbers + quotes.

### Not verified (remove assumptions)

* Any specific **S3/bucket names**, **paths**, or **sync scripts**.
* **Python version** for RL: CI logs showed 3.13 for adversarial recipes, but RL stack version is **unknown**.
* Exact **gym/env versions**, **seeds**, **horizons**, **hardware**, **access procedures**, **internal Zotero/JIRA IDs**, **timelines**, or **CSV templates already committed**.

> Action: Use the prompts below to obtain the real values before work starts.

---

## 2) Cleaned answers (what we can state now)

### Access & Permissions

* **Where are nightlies stored?** **[CONFIRM]** Ask Chris for the canonical location (repo or storage) and read‑only path for **CartPole** and **WTM** runs.
* **How to access?** **[CONFIRM]** Request the exact access method (VPN/SSO/keys) and who approves it.
* **Automation?** **[CONFIRM]** If a pull script exists, request its repo path and example command.

### Environment & Tooling

* **Python/deps:** Use the version and dependency spec the **RL maintainer** provides **[CONFIRM]** (don’t reuse adversarial CI versions by assumption).
* **Hardware & quotas:** **[CONFIRM]** If local reruns are needed, ask for minimum CPU/GPU and memory guidance.
* **Literature access:** Online search (Scholar/arXiv) is expected; if restricted, agent will download PDFs externally and attach.

### Our Results (CartPole & WTM)

* **Curated summaries exist?** **[CONFIRM]** If yes, request path/format; if no, agent will create them.
* **Canonical env setup:** **[CONFIRM]** Gym/env version, observation type, episode length cap, and training horizon per env.
* **Seeds/episodes:** Suggest **≥5 seeds** unless maintainer specifies otherwise **[CONFIRM]**.
* **Configs:** **[CONFIRM]** Ask for official config files (YAML/JSON) and keep them unchanged.
* **Where to store outputs:** Use a project folder the team designates **[CONFIRM]**; include a PROVENANCE note (see §4 templates).
* **Change control:** Any deviation from defaults must be pre‑approved by **Chris or Dom**.

### Literature Review

* **Baselines/papers to include:** Start with **PPO, DQN, A2C, SAC**; expand if strong CartPole/WTM sources are found. Quality peer‑reviewed or well‑cited arXiv with code is acceptable.
* **Extra stats:** Capture wall‑clock time and variance **if reported**.
* **Source IDs:** Use a simple scheme the author prefers; proposal: `RL-C#` (CartPole), `RL-W#` (WTM). **[CONFIRM]**

### Quote Bank & Appendix Tables

* **Templates:** If none exist, use the **embedded templates in §4**. **[CONFIRM]** if there’s a house style to follow.
* **Formatting:** ≤2 sentences per quote; include page/fig/section.
* **Appendix rows:** Include both **Howso** and **literature** rows. Split multiple setups into separate rows.

### Comparability Notes & Provenance

* **Comparability notes:** One short paragraph per env covering **env version, solved threshold, evaluation protocol** (sticky actions/reward shaping if any).
* **Provenance detail:** OS, Python, package versions, machine type, exact commands, artifact locations. Checksums are recommended but **[OPTIONAL]** if tooling isn’t standard.

### Review & Delivery

* **Reviewer/POC:** **Chris Hazard** (technical), **Dom G.** (integration/whitepaper).
* **Delivery target:** **[CONFIRM]** Desired date; if not specified, propose a date.
* **Where to upload:** **[CONFIRM]** Team’s shared drive/repo; attach links in the tracking ticket/thread.

---

## 3) Ready‑to‑send prompt for the agent (no assumptions)

> **Task:** Build a small, defensible **RL results pack** for **CartPole** and **Wafer‑Thin‑Mints**. You will (1) collect our existing runs (or run Howso RL if instructed), and (2) gather **published** baseline results with citations and short quotes. You will **not** run external baselines.
>
> **Deliverables:**
>
> 1. **Body tables (2):** per env — `Algorithm (ours) • Metric • Our Result • Literature Comparator (range/median) • Sources (IDs)` (≤6 rows).
> 2. **Appendix tables (2):** literature rows — `Algorithm(+ver) • Obs type • “Solved” criterion • Median episodes/steps (N) or best reward • Seeds • Year • DOI/URL • Code • Notes`.
> 3. **Quote bank (CSV):** verbatim ≤2‑sentence quotes stating the metric/claim with **page/fig**.
> 4. **Our‑results sheet (2):** raw per‑seed logs and summary (median + IQR), env v

