class GameEvent:
    def __init__(self, type: str, payload: dict = None):
        self.type = type
        self.payload = payload or {}

class EventBus:
    def __init__(self):
        self._listeners = {}  # event_type: list of callbacks

    def subscribe(self, event_type: str, callback: callable):
        """Register a listener for a specific event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: callable):
        """Remove a listener from a specific event type."""
        if event_type in self._listeners:
            self._listeners[event_type] = [
                cb for cb in self._listeners[event_type] if cb != callback
            ]

    def publish(self, event: GameEvent):
        """Fire off an event to all registered listeners."""
        listeners = self._listeners.get(event.type, [])
        for callback in listeners:
            callback(event)

    def clear(self):
        """Remove all listeners (useful for scene resets)."""
        self._listeners.clear()
