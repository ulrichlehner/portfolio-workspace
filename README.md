# portfolio-workspace

Workspace for contributing to [Portfolio Performance](https://github.com/portfolio-performance/portfolio)
from a fork, with a Docker-only dev environment and rules for AI coding agents.
The fork itself stays free of these files, so nothing of it can end up in an upstream PR.

## Setup

```bash
git clone git@github.com:ulrichlehner/portfolio-workspace.git
cd portfolio-workspace
./bootstrap.sh
```

`bootstrap.sh` clones the fork into `portfolio/` and adds the upstream remote.
To use your own fork: `FORK_URL=git@github.com:<you>/portfolio.git ./bootstrap.sh`.

Requirements on the host: git and Docker. No Java or Maven.

## Usage

Run `scripts/dev.sh` without arguments for the list of commands, for example:

```bash
scripts/dev.sh test FinTechGroupBankPDFExtractorTest
```

Or open the folder in VS Code and choose "Dev Containers: Reopen in Container": Java, Maven, Node.js,
OpenSpec, zsh with a Starship prompt and the matching extensions, all inside the container.

New features are planned with [OpenSpec](https://openspec.dev). The CLI runs in Docker as well:
`scripts/openspec list`. Specs and changes are in `openspec/` and stay in this repo.

The rules for agents and contributors are in [AGENTS.md](AGENTS.md). Start agents in this folder, not in `portfolio/`.

## AI-assisted development with OpenCode

The default workflow uses one long-lived OpenCode session as the orchestrator and
single point of contact. It maintains the OpenSpec plan, delegates bounded tasks
to subagents, reviews their work, and coordinates integration and verification.
The operating rules are in [AGENTS.md](AGENTS.md#agent-orchestration-default-workflow).

### Onboarding

1. Complete the setup above and open OpenCode in this workspace root, not `portfolio/`.
2. In `/connect`, select OpenAI and use the ChatGPT/Codex subscription sign-in method
   offered by your installation. Confirm the active account uses subscription access,
   rather than an API key or environment-provided API credentials. See the
   [OpenCode provider account guide](https://opencode.ai/v2/docs/cli/providers).
3. Use `/models` to select an OpenAI model available through that subscription.
   The default policy is OpenAI subscription access only: no pay-per-token API usage,
   paid fallback, or other providers without explicit authorization. Model names alone
   do not establish billing mode. If subscription access is unavailable, stop and resolve
   the connection rather than adding an API key.
4. Ask the orchestrator to read `AGENTS.md`, inspect the relevant OpenSpec change and
   current Git state, and identify the next task. For Portfolio Lens, the change is
   `openspec/changes/automatic-portfolio-xray/`.
5. Authorize implementation when ready. For example:

   > Continue implementing automatic-portfolio-xray using the default orchestrator
   > workflow. Delegate focused tasks to OpenAI subscription-backed subagents,
   > choosing models and effort appropriate to each task. Report blockers and checks.

The orchestrator handles small tasks directly and delegates when it saves work.
Independent tasks can run in parallel; overlapping edits and shared Docker operations
are coordinated. Stronger reasoning is reserved for architecture, difficult debugging,
and consequential reviews. Subagents also consume subscription quota; the agent cannot
infer remaining quota from model pricing metadata.

Before each delegation, the orchestrator states the selected model, effort and reason;
it does not silently inherit its own model. The current routing baseline is Sol 6.1
with low effort for bounded exploration and medium effort for bounded implementation
or review, subject to availability. Escalations need a task-specific reason. The same
selection discipline applies to any future authorized provider; subscription-only
billing remains the default. See `AGENTS.md` for the maintained routing policy.

Keep decisions, task completion, verification results, and pending work in the OpenSpec
artifacts, and reusable project knowledge in `AGENTS.md`. A new session should be able
to resume from these files without relying on the previous conversation. Planning,
implementation, and publishing retain the authorization boundaries in `AGENTS.md`.

## License

[MIT](LICENSE)
