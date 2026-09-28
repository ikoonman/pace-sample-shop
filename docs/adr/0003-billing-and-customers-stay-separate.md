# ADR-0003: Billing and customers stay separate

Status: accepted

## Context

Billing needs a customer's region and VAT status. Reading customer storage from
billing would tie the two domains together.

## Decision

Billing takes what it needs from the order, which copies the customer's region
when it is created. Billing and customers have no dependency on each other.

## Consequences

An order records the customer facts that were true when it was placed.
