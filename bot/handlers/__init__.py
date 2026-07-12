def register_handlers():
    from . import admin, crypto, events, user, moderation  # noqa: F401

__all__ = ["register_handlers"]
