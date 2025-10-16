# Clarifying Questions for RL Results Pack Task

## Access & Permissions
- Where are the latest Howso RL nightly artifacts for CartPole and Wafer-Thin-Mints stored (repo, bucket, or shared drive path)?
- What credentials or VPN access do I need to reach those artifacts, and how do I obtain them?
- Are there existing scripts or CLI tools that pull the nightly results automatically, and if so, where are they located?

## Environment & Tooling
- Which Python version and dependency set should I use when reproducing or rerunning our agents (exact `requirements-*.txt` file or alternative specification)?
- Are there hardware expectations or quotas (CPU/GPU type, RAM) for rerunning CartPole or WTM locally or on shared infrastructure?
- May I rely on external network access (e.g., Google Scholar, arXiv) from this environment, or should I gather literature references offline?

## Our Results (CartPole & WTM)
- Do curated summaries of recent Howso RL runs already exist, and if so, in what format (CSV, JSON, database)?
- For each environment, what is the canonical gym version, observation space configuration, and default training horizon we must match?
- How many seeds and episodes per seed are required if I need to rerun the agents, and is there a target wall-clock budget?
- Are there configuration files (YAML, JSON) that define the official CartPole/WTM experiment settings that I should reuse?
- Where should I store newly generated raw logs and summaries so other teammates can find them (path, naming conventions, retention requirements)?
- Who should review or sign off on any deviations from the default configuration before runs are executed?

## Literature Review
- Are there preferred baseline algorithms or seminal papers that must be included for CartPole and WTM comparisons?
- Is there an internal bibliography or citation manager I should reference before adding new sources?
- What level of publication quality is acceptable (peer-reviewed only, or high-quality arXiv allowed)?
- Should I capture statistics beyond episodes/steps (e.g., wall-clock time, reward variance) when papers report them?
- How should I assign source IDs for the tables—use an existing numbering scheme or create a new one?

## Quote Bank & Appendix Tables
- Do we have a template (CSV schema, example file) for the quote bank and appendix tables that I should follow exactly?
- Are there formatting constraints for quotes (escape characters, maximum length) when exporting to CSV?
- Should the appendix tables include our Howso RL rows as well, or only literature baselines?
- How should I handle papers that report multiple experimental setups—split into multiple rows or aggregate into one entry?

## Comparability Notes & Provenance
- Is there a preferred length or structure for the comparability notes per environment (bulleted list, paragraph)?
- What level of detail is expected in PROVENANCE.md regarding hardware specs, package versions, and command history?
- Are there existing checksum or artifact-tracking tools I must use when documenting logs and outputs?
- Should the provenance note reference issue IDs, ticket numbers, or internal dashboards for traceability?

## Review & Delivery
- Who is the primary reviewer or point of contact for the results pack once drafted?
- What is the expected delivery timeline or milestone for the whitepaper team?
- In addition to the prescribed directory layout, do we need to upload artifacts to a shared drive or attach them to a ticket?

Answering these questions will unblock the data collection, experimentation, literature survey, and packaging steps required by `task.md`.
