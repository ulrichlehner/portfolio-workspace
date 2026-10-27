# Proposal

## Why

The look-through feature works, but its UI is hard to use. Its name ("Portfolio Lens") is a vague brand, the view
shows several paragraphs of text above a long table, and the toolbar actions are confusing. Nothing guides a user
who has no API key, and the data status pane blends into the table. The settings page offers three long buttons
for what should be a single API key field. Both tables lose their selection every 60 seconds because the view
recalculates everything on each status tick, which also makes the view feel slow. The feature has no charts,
although looking at composition is mainly a visual task.

The base feature (`feature/automatic-portfolio-xray` in the fork) is not upstream yet. Reworking the UI now
avoids publishing the old name and layout at all.

## What Changes

- **Name and placement**: rename the feature to "Breakdown" / "Aufschlüsselung", shown as a sub-item of
  Statement of Assets / Vermögensaufstellung (next to Chart and Holdings) instead of a separate report entry.
  The view title is "Breakdown by Company" / "Aufschlüsselung nach Unternehmen". Rename the `PortfolioLens*`
  classes to `LookThrough*`, keep the `lookthrough` packages, and title the settings page plain "Eulerpool".
- **Responsiveness**: recalculate only when inputs actually change, compute off the UI thread, and keep the
  selection, expansion and scroll position of both tables across updates.
- **View layout**: one header line with the valuation date, a summary strip (securities value, resolved share,
  top-10 concentration, decomposed funds), and a coverage bar in place of the explanatory paragraphs. Below
  that, a chart area next to the company table. The details move to tooltips and the information pane.
- **Actions and progress**: one refresh action. While a refresh runs, an inline progress line shows the count
  and a stop control, so there is no permanent Cancel action anymore.
- **Onboarding states**: clear banners for "no API key" (with a direct link into the settings page), "no
  funds held", "empty portfolio" and "provider suspended". Direct holdings stay visible without a key.
- **Charts** with libraries PP already ships: a coverage bar, a company treemap (engehausen treemap,
  colored direct vs. through funds) and a top-N bar chart stacked direct vs. indirect. Selecting a company in
  a chart selects it in the table.
- **Data status pane**: reduce ten text columns to fund, status icon, retrieved date and coverage. The full
  details move into tooltips.
- **Settings page**: one API key field saved through the dialog's Apply/OK, a "remove key" control, a single
  status line and the request-key link. Session-only entry only appears as a fallback when secure storage is
  unavailable. The persistence preference stays as one checkbox with a one-line status.

## Capabilities

### New Capabilities
- `breakdown-view`: layout, summary, onboarding states, actions, progress, charts, data status presentation
  and interaction behavior (selection, responsiveness) of the look-through view.
- `composition-provider-settings`: how a user configures a composition provider's API key and persistence
  preference.

### Modified Capabilities
- `portfolio-look-through`: the "Feature identity" requirement changes from "Portfolio Lens" to
  Breakdown / Aufschlüsselung under Statement of Assets.

## Impact

- Fork, UI bundle only: `ui/views/lookthrough/*`, `ui/preferences/EulerpoolPreferencePage.java`,
  `ui/editor/Navigation.java`, `Messages.java` and all `messages*.properties` (renamed and removed keys).
  The calculation engine, the provider adapter, the credential store and cache policies stay unchanged.
- Existing column settings stored under the view's preference key may reset once because of the class
  rename.
- Delivery: one focused commit per increment on `feature/breakdown-ui-rework`, stacked on
  `feature/automatic-portfolio-xray`. Increments: (A) responsiveness and selection, (B) rename and
  placement, (C) settings page, (D) layout, onboarding and status pane, (E) charts. Each increment is shaped so
  it can fold into a focused upstream PR when the base feature is split.

## Out of scope

- Splitting the overall look-through work into upstream PRs and opening them (separate planning step).
- Fund overlap matrix and sector/country breakdowns (the latter depend on provider data that is not checked
  yet). Both are follow-ups.
- Changes to calculation, validation, provider access, quotas or persistence policy.
- Enabling real-data persistence; the provider gates stay as recorded.
