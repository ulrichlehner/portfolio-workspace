# Portfolio Performance workspace

Instructions for AI coding agents (Codex, Claude Code and others) and for humans.
This repository wraps a fork of [Portfolio Performance](https://github.com/portfolio-performance/portfolio)
(PP) and holds everything that must not go upstream: agent rules, the dev container and helper scripts.

All project-specific knowledge belongs in this file. Do not keep it only in an agent's private memory.

## Layout

```
portfolio-workspace/
├── AGENTS.md          this file, the rules for all agents
├── CLAUDE.md          imports this file for Claude Code
├── .devcontainer/     the only dev environment (Java 21, Maven, Node.js, OpenSpec, zsh)
├── .vscode/           editor settings for the workspace (no format on save)
├── scripts/dev.sh     build, test, PDF and app commands, all run in Docker
├── scripts/openspec   the OpenSpec CLI, run in Docker
├── openspec/          feature specs and changes (OpenSpec), stay in this repo
├── .claude/ .agents/  OpenSpec commands and skills for Claude Code, Codex and others
├── bootstrap.sh       clones the fork into portfolio/ and adds the upstream remote
├── scratch/           private temporary files (gitignored), deleted after use
└── portfolio/         the fork (gitignored), contains only upstream code
```

Start agents in this folder, not in `portfolio/`, so these rules are loaded.
The upstream files `portfolio/AGENTS.md`, `portfolio/CLAUDE.md` and `portfolio/CONTRIBUTING.md`
apply for code style and conventions. Where they conflict with this file, this file wins.

## Rule 1: Docker only, nothing on the host

- Never install Java, Maven, Node.js or other dev toolchains on the host. Never run `mvn`, `java`, `node`, `npm` or `npx` on the host.
- Run every build and test through `scripts/dev.sh` or inside the dev container.
  When upstream docs say "set JAVA_HOME" or show a `mvn` command, run it in the container instead.
- `scripts/dev.sh` uses the image `portfolio-dev` (built from `.devcontainer/`) and the volume `portfolio-m2` for the Maven cache.
- When work is finished, clean up: `scripts/dev.sh clean` (build output) and, if the user wants, `scripts/dev.sh purge` (image and volume too).
  Never remove Docker containers, images or volumes that belong to other projects.

Commands:

| Task | Command |
| :--- | :--- |
| Core tests + Checkstyle | `scripts/dev.sh test` |
| One test class | `scripts/dev.sh test FinTechGroupBankPDFExtractorTest` |
| macOS app with bundled Java, for manual tests | `scripts/dev.sh app` |
| Start that app with its own workspace | `scripts/dev.sh run-app` |
| PDF to text like PP does | `scripts/dev.sh pdftext scratch/file.pdf` |
| Shell in the container | `scripts/dev.sh shell` |
| Delete build output | `scripts/dev.sh clean` |
| Also remove image and volume | `scripts/dev.sh purge` |

## Dev container

Optional, for working in VS Code: "Dev Containers: Reopen in Container" builds `.devcontainer/` and installs
the extensions there (Java, Eclipse PDE, Maven, XML, YAML, GitLens, GitHub, Claude Code, Codex and others).

- The workspace is mounted at its host path and the host's Docker socket is shared, so `scripts/dev.sh` works
  inside the container too. `mvn` and `openspec` also run directly in its terminal. `scripts/dev.sh run-app`
  only works on the host (it starts the macOS app).
- Shell: zsh with Oh My Zsh, Starship prompt (git status, Java version, command duration), history kept across rebuilds,
  suggestions, syntax highlighting, fzf, completions for git, gh, docker, mvn and openspec.
- gh, Claude Code and Codex keep their logins in shared volumes (`devcontainer-gh-config`,
  `devcontainer-claude-config`, `devcontainer-codex-config`).
- Never enable format on save. Upstream formats with the Eclipse settings in each bundle's `.settings/` and
  PDF extractors are aligned by hand (see `.vscode/settings.json`).

## Planning features with OpenSpec

New features are planned with [OpenSpec](https://openspec.dev) before any code is written.

- Specs and changes live in `openspec/` of this workspace. They never go into `portfolio/` or upstream.
  Code is implemented in `portfolio/` and goes upstream as usual (Rule 3).
- The OpenSpec CLI runs only in Docker (Rule 1). It is installed in the `portfolio-dev` image, so inside the dev
  container `openspec` works directly. On the host, the OpenSpec skills and commands must call
  `scripts/openspec <args>` wherever they say `openspec <args>`.
- Workflow: explore, propose (planning only, no code), apply (implement the tasks), archive.
  Claude Code: `/opsx:propose`, `/opsx:apply` and so on. Codex: `$openspec-propose` and so on.
- Project constraints for the artifacts are in `openspec/config.yaml`.
- Telemetry is disabled in the image (`OPENSPEC_TELEMETRY=0`).
- After changing `OPENSPEC_VERSION` in `.devcontainer/Dockerfile`, rebuild the image and run `scripts/openspec update`.

## Rule 2: Everything is public, protect personal data

The fork, upstream PRs, the PP forum and this repository are public. Never publish personal data of
the user or anyone else: names, addresses, IBANs, account or depot numbers, references, document IDs,
amounts, holdings or ISINs from real documents. Bank and company data (bank name, address, register
numbers, board members in the legal notice, BIC, SEPA creditor ID) is public and stays.

- Real documents (PDFs, PP debug texts, portfolio files, logs) go only into `scratch/` or a temporary
  folder outside the repo, and are deleted after use. Never commit them.
- Never write real values into examples, comments, commit messages or rules, not even as "do not publish X".
- Before every commit and push, scan the diff against the real source for leaked values.
- The user may be credited by real name and their GitHub account.

### Anonymizing a PDF test sample

1. Start from PP's debug export (File > Import > Debug: Create text from PDF), or `scripts/dev.sh pdftext`.
   Keep the header, every line, the line order, page breaks and trailing spaces exactly.
2. Personal data: replace with PP's anonymize algorithm (`PDFAnonymizeMouseListener` in the UI bundle):
   each letter becomes a random letter of random case, each digit a random digit, other characters stay.
   This applies to names, addresses, account numbers, IBANs, mandate and payment references, order numbers and document IDs.
3. Amounts: replace with plausible values of the same order of magnitude (roughly 0.75 to 1.25 times the real value,
   round amounts stay round). Keep related amounts consistent (purchase and matching debit, opening balance plus
   bookings equals closing balance). No value may equal a real one.
4. ISINs: replace with other real ISINs that do not appear in the user's documents or portfolio.
5. Dates and bank texts stay unchanged.
6. Check the result: same line count and structure as the real export, no real value left, the test fails without the fix.

## Rule 3: Contributing upstream

- Remotes in `portfolio/`: `origin` is the fork, `upstream` is portfolio-performance/portfolio.
  Keep the fork's `master` equal to upstream. Work on one branch per fix, created from `upstream/master`.
- One focused commit per PR, rebased on `upstream/master`. Never merge `master` into a branch.
- Commit message: subject at most 50 characters, body wrapped at 72, explain what and why.
  Link forum threads with `Issue: <url>` and GitHub issues with `Closes #<n>`.
- No AI attribution in commits or PRs that go upstream (no `Co-Authored-By` for an AI, no "Generated with" footer).
  The maintainer removes them ("the code is mostly generated, but reviewed and signed off by a human", PR #5866).
- Tests: add a focused test for every importer change. Run `scripts/dev.sh test` before pushing and check that the
  new test fails without the fix.
- The PR is opened from the fork branch into `upstream/master`, never on the fork.
  First-time contributors need a maintainer to approve the CI run.
- CodeRabbit comments automatically. Its "Docstring coverage" warning does not apply (the project does not use Javadoc
  on importer methods), do not let it push fixes.
- The maintainer often merges by hand, so a merged PR may show as "Closed". He adds new contributors to
  `about.contributors.txt` himself.
- A contribution may be folded into another contributor's PR (PR #6116 went into #5998). The commit then has the
  other author; credit comes from "Includes the work by @<user> done in #<pr>" in the commit message and the
  contributor list. Before closing such a PR, check that the test and sample arrived intact.
- After merge: delete the branch, update `master` from upstream, delete the local branch with `git branch -D`.

## PDF importer knowledge

- Extractors: `portfolio/name.abuchen.portfolio/src/name/abuchen/portfolio/datatransfer/pdf/`,
  tests and samples in `portfolio/name.abuchen.portfolio.tests/src/name/abuchen/portfolio/datatransfer/pdf/<bank>/`.
  Follow `portfolio/.claude/rules/pdfextractors.md` (formatting, regex conventions, test format) and keep the style
  of the surrounding code, consistency matters more than nicer code.
- Layout variants of the same booking get their own section inside `oneOf(...)`, each with the verbatim document lines above it.
- Silent fallback: `PDFImportAssistant.run()` first converts with PDFBox 3. If no extractor returns any booking
  (for example because one block throws), it retries with the legacy PDFBox 1.8 conversion and only reports errors
  if that also finds nothing. So in the app an extractor error can show up as silently missing bookings.
  Sign of the fallback in the PP log (`~/Library/Application Support/name.abuchen.portfolio.product/workspace/.metadata/.log` on macOS):
  `PDF successfully imported with PDFBox 1.8.x <file>`. Unit tests call the extractor directly and show the real error.
- Account statements: PP only reads bookings that are not available from other documents (transfers, debits, interest,
  fees, taxes). Buys, sells and dividends come from their dedicated PDFs.
- flatex: the extractor is `FinTechGroupBankPDFExtractor` (flatex, flatexDEGIRO, biw). Documents since 2026 say
  "flatexDEGIRO Bank SE", older ones "flatexDEGIRO Bank AG". Keep the name as the document prints it.

## Manual testing with a local build

1. `scripts/dev.sh app` builds the macOS app with a bundled Java runtime (no Java on the host needed).
2. `scripts/dev.sh run-app` starts it with its own workspace in `scratch/`, so the installed PP and its settings stay untouched.
3. Test only with a copy of the user's portfolio file. Afterwards quit the app and run `scripts/dev.sh clean`.

## Writing texts

- PRs and commits in English, the PP forum in German.
- Plain, factual wording. Avoid typical AI phrasing such as em dashes and filler. Only state what is verified.
