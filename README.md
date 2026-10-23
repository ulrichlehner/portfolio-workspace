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

Or open the folder in a dev container (`.devcontainer/`).

New features are planned with [OpenSpec](https://openspec.dev). The CLI runs in Docker as well:
`scripts/openspec list`. Specs and changes are in `openspec/` and stay in this repo.

The rules for agents and contributors are in [AGENTS.md](AGENTS.md). Start agents in this folder, not in `portfolio/`.

## License

[MIT](LICENSE)
