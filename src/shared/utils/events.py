"""A tiny in-process event bus."""
from typing import Callable, Dict, List

_handlers: Dict[str, List[Callable[[dict], None]]] = {}


def subscribe(topic: str, handler: Callable[[dict], None]) -> None:
    _handlers.setdefault(topic, []).append(handler)


def publish(topic: str, payload: dict) -> None:
    for handler in _handlers.get(topic, []):
        handler(payload)
