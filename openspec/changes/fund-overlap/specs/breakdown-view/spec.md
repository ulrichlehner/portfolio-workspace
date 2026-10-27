# Spec Delta

## ADDED Requirements

### Requirement: Overlap chart
The chart pane SHALL offer an "Overlap" chart kind showing a matrix of the decomposed funds with the overlap percentage in each cell, shaded by size. A cell tooltip SHALL name both funds, the overlap, the number of shared companies and the five largest shared companies. With fewer than two decomposed funds, the chart SHALL show a short message instead of a matrix.

#### Scenario: Two decomposed funds
- **WHEN** the portfolio holds two decomposed funds
- **THEN** the overlap chart shows a two-by-two matrix whose off-diagonal cells show their overlap.

#### Scenario: Single fund
- **WHEN** only one fund is decomposed
- **THEN** the overlap chart states that at least two decomposed funds are needed.
