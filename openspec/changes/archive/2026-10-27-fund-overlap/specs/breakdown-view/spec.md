# Spec Delta

## ADDED Requirements

### Requirement: Overlap chart
The chart pane SHALL offer an "Overlap" chart kind showing each pair of decomposed funds once, as the lower triangle of a fund matrix without diagonal. Each cell SHALL show the overlap percentage and the number of shared companies, shaded by size. A cell tooltip SHALL name both funds, the overlap, the number of shared companies and the five largest shared companies. With fewer than two decomposed funds, the chart SHALL show a short message instead of a matrix.

#### Scenario: Two decomposed funds
- **WHEN** the portfolio holds two decomposed funds
- **THEN** the overlap chart shows one cell for the pair with its overlap and shared company count.

#### Scenario: Single fund
- **WHEN** only one fund is decomposed
- **THEN** the overlap chart states that at least two decomposed funds are needed.
