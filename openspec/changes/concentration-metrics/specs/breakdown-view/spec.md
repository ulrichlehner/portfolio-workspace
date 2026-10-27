# Spec Delta

## ADDED Requirements

### Requirement: Concentration summary
The summary SHALL show the effective number of companies, computed as one divided by the sum of squared shares of each company in the company exposure and shown together with the number of companies, and the largest company with its share of the portfolio value. When a single company exceeds 10 percent of the portfolio value, the attention indicator SHALL name that company and its share.

#### Scenario: Evenly spread
- **WHEN** the company exposure is split evenly across 100 companies
- **THEN** the summary shows an effective number of 100 of 100 companies.

#### Scenario: Dominant company
- **WHEN** one company accounts for 12 percent of the portfolio value
- **THEN** the summary shows it as the largest company and the attention indicator names it with its 12 percent share.
