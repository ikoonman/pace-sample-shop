# ADR-0001: Layered architecture

Status: accepted

## Context

Handlers, use cases and storage were mixed in the first prototype, which made
changes to storage ripple into the API.

## Decision

Each domain has `api`, `services`, `storage` and `domain` layers. Dependencies
point downwards only. API handlers call services, never storage.

## Consequences

Storage can be replaced without touching handlers. Services carry the logic,
so they are where tests go first.
