# Portfolio Performance workspace

Instructions for AI coding agents (OpenCode, Codex, Claude Code and others) and for humans.
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

## Agent orchestration (default workflow)

- Use one main session as the orchestrator and the user's single point of contact.
  It owns the big picture, OpenSpec consistency, task dependencies, review, integration,
  and final reporting. Delegation to subagents is authorized by default for approved work.
- Use only subscription-backed access or catalog-listed free models unless the user
  explicitly changes this policy. On 2026-10-24 the user authorized continuing with the
  free models of the `opencode` provider. Do not use pay-per-token APIs or paid fallbacks.
  A model ID does not prove billing mode; if the connection mode is uncertain, ask the
  user to confirm it. On quota exhaustion, pause rather than switch billing routes.
- Discover available models and effort variants before choosing them; do not hard-code
  assumed model availability. Use lightweight models/lower effort for bounded exploration
  and routine work, stronger models/higher effort for complex implementation, architecture,
  debugging, and consequential review. Exact model/variant overrides require user
  authorization where the agent harness requires it. Subscription quota is not inferable
  from catalog API prices; do not claim quota savings or remaining balances without evidence.
- Before every delegation, deliberately select the model and effort for the task;
  do not silently inherit the orchestrator's model. State the assignment and a brief
  rationale. Check available model IDs/variants and harness authorization before
  applying an override; if an override is unavailable or requires further authorization,
  disclose that limitation rather than claiming optimized routing.
- Current user-approved routing baseline (2026-10-24): free `opencode` models, with
  higher effort for implementation/review and lower effort for bounded exploration.
  Escalate only when complexity, risk, or observed failures justify it, and explain why.
  Reassess this baseline as models and task requirements change; free-model availability
  and quality must be verified per task rather than assumed.
- Apply the same explicit, task-appropriate selection and billing constraints to any
  future authorized LLM/provider. Provider authorization does not authorize paid API
  usage. The orchestrator owns these decisions without requiring user reminders.
- Handle trivial tasks directly. Give each delegated task a narrow objective, relevant
  OpenSpec artifacts, file ownership, acceptance criteria, required checks, and applicable
  workspace/upstream rules. Subagents start with fresh context; provide the context needed
  rather than assuming they know the parent conversation.
- Parallelize only independent work. Avoid concurrent edits to the same files. Coordinate
  shared Docker builds, tests, app launches, and cleanup centrally. Subagents must not
  switch shared branches, commit, push, or open PRs unless explicitly assigned that action
  within the user's authorization.
- Require concise handoffs: changed files, checks and results, unresolved issues, and
  decisions needing review. The orchestrator reviews the actual diff and verifies results
  before marking OpenSpec tasks complete.
- Commit coherent, verified milestones proactively under the user's implementation
  authorization. Commit workspace planning/progress separately from PP code; do not
  leave completed milestones uncommitted across handoffs without recording why.
  Run relevant checks and privacy review first, stage explicit paths, and exclude
  unrelated user changes. Keep one focused upstream commit per planned PR; accumulate
  related tasks into that increment rather than making a commit per checkbox.
  Record commit references and outstanding verification in the progress artifact.
  Publishing still requires authorization under Rule 3.
- Keep durable progress, decisions, verification evidence, and next steps in the relevant
  OpenSpec artifacts; keep reusable project knowledge here. Do not rely on a long-running
  session's memory. On resuming, inspect the artifacts and current Git state first.
- These defaults do not authorize implementation of a planning-only request or publishing.
  All Docker, privacy, provider-gate, and contribution rules apply equally to subagents.

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
| Refresh and open a private WebDAV copy | `scripts/dev.sh run-app --webdav-copy` |
| Explicitly open retained data offline | `scripts/dev.sh run-app --webdav-copy --offline` |
| Synthetic tooling tests (no live credentials) | `scripts/dev.sh test-tools` |
| Keep / recover a local generation | `scripts/dev.sh keep-data` / `scripts/dev.sh recover-data` |
| Explicitly remove managed private test data | `scripts/dev.sh clean-data` |
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
- OpenSpec tracks the workflow; it does not perform or enforce Git operations itself. Include explicit implementation
  tasks to create the branch, run required checks, scan the diff for private data, and create a focused commit per
  planned upstream PR. Record verification results and commit references when completing those tasks.
- Push branches and open PRs when authorized by the user; existing authorization remains valid. Track any publishing
  steps still awaiting authorization as outstanding. Archive only after the agreed completion criteria are met.
  Planning-only requests do not authorize implementation or publishing.
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
  Keep the fork's `master` equal to upstream. Work on one branch per focused change, created from `upstream/master`.
- Name branches `<type>/<openspec-change-name>`, using generic types such as `feature/`, `fix/` or `refactor/`.
  Example: `feature/automatic-portfolio-xray`. Do not include chatbot or agent names in branch names.
  For changes without OpenSpec, use a descriptive kebab-case name after the type. If one OpenSpec change needs
  multiple focused PRs, append a descriptive scope suffix to its branch names.
- One focused commit per PR, rebased on `upstream/master`. Never merge `master` into a branch.
- Use Conventional Commits in both this workspace and the PP fork: `<type>(<optional-scope>): <description>`.
  Use types such as `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci` or `chore` according to the change.
  Mark breaking changes with `!` before the colon and explain them in a `BREAKING CHANGE:` footer.
  Example for planning artifacts: `docs(openspec): plan automatic portfolio xray`.
- Commit message: subject at most 50 characters including type and scope, body wrapped at 72, explain what and why.
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

The managed WebDAV workflow is documented in `docs/local-testing.md`. Its private
configuration is `scratch/pp-dev-secrets/webdav.json` (mode 600); it requires
confirmed server-side read-only access. Never put its contents in chat or Git.
The downloader runs only in Docker, uses verified HTTPS without redirects and
implements no remote writes. The app receives only a separate local copy.

Build manifests in `scratch/pp-dev-build/` identify the PP revision, dirty state,
source-content fingerprint, architecture and packaged app. A stale or missing
build must be rebuilt. A native kernel lock protects builds, launches, refresh
and cleanup throughout the app's lifetime. Quit the app before those operations.
Managed launches use a private resource-only Eclipse startup bundle and a fresh
development workspace to open the exact local portfolio without PP code changes.

Generations in `scratch/pp-dev-data/` retain an untouched baseline and a writable
development copy with adjacent settings/backups. Successful refresh preserves the
previous generation; `keep-data` prevents older experiments from being pruned.
Ordinary `clean` preserves generations. Use `clean-data` explicitly after private
testing; it removes only managed data and leaves unrelated scratch files and the
private configuration alone. Workspace tooling never goes into upstream PP.
Periodic remote saves by other applications are expected. A coherent local
snapshot is sufficient; later remote changes do not invalidate or replace a
running test copy, and remote downloads need not have equal digests.

## Portfolio Lens provider gates

The repository checklist and public Eulerpool permission review are recorded in
`openspec/changes/automatic-portfolio-xray/provider-gates.md` (2026-10-23).
Free desktop cache retention and distribution of an adapter using individual
keys remain unverified. The user confirmed a development-only assumption of Eulerpool
runtime/display and adapter distribution permission on 2026-10-23. Implementation
and local development may proceed under that assumption; it is not verified
permission. The task 6.3 pre-publish checklist must verify runtime/display,
source/binary distribution, attribution/other obligations and optional retention
before publication. Real-data disk persistence stays disabled until permission
and retention are verified. Persistent caching is an opt-out preference per
provider/account, defaulting on where permitted. Effective disk persistence
requires both user preference and verified provider policy/retention. If disabled,
prohibited or unverified, use permitted session-only analysis with the same
calculations and disclose restart/offline limitations. Remove affected disk data
and prevent pending jobs from recreating it when persistence is withdrawn.
Other providers' modes/settings remain independent. Generic storage contracts,
synthetic providers and calculations can be implemented before permission is
settled; real provider payloads must not be persisted until approved. Session-only
release still requires runtime/display/distribution and data-quality gates.
Provider contact requires explicit user authorization; questions remain unsent.

## Writing texts

- PRs and commits in English, the PP forum in German.
- Plain, factual wording. Avoid typical AI phrasing such as em dashes and filler. Only state what is verified.
