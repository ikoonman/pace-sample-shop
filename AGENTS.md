# Working in pace-sample-shop

## Layout

`src/<domain>/<layer>/`: domains are `customers`, `orders` and `billing`;
`shared/utils` holds helpers. The web client is in `web/src`.

## Rules

- Layers point downwards: `api` → `services` → `storage` → `domain`. Storage
  never imports services (ADR-0001).
- API handlers reach storage only through a service (ADR-0001).
- Money is integer cents; use `shared.utils.money` (ADR-0002).
- Billing and customers don't depend on each other: billing takes what it
  needs about a customer from the order (ADR-0003).
- Python names: `snake_case` functions, `CapWords` classes.

## Tests

`python -m pytest` from the repository root.
