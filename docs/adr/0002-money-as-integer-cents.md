# ADR-0002: Money as integer cents

Status: accepted

## Context

Floating point totals were off by a cent on discounted lines.

## Decision

All amounts are integer cents. Percentages are applied with
`shared.utils.money.percent_of`, rounding half up.

## Consequences

No floats in prices, tax or totals. Formatting happens only at the edges.
