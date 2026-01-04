from game import Event

class StoryBuilder:
    def __init__(self, game):
        self.game = game

    def event(self, name, description, *, required_flags=None, required_items=None, flag=None):
        if name in self.game.events:
            raise ValueError(f"Event {name} already exists")

        self.game.events[name] = Event(description, required_flags, required_items, flag)


    def option(self, from_event, description, to_event, *,alt_events=None, required_flags=None, required_items=None):
        source = self._get_event(from_event)
        destination = self._get_event(to_event)

        if destination.required_flags:
            raise ValueError(
                f"Event '{to_event}' has required_flags and cannot be a default option target.\n"
            )
        alt_objs = [self._get_event(alt) for alt in alt_events or []]
        source.options.append(source.Option(description, destination, alt_objs, required_flags, required_items))

    def treasure(self, event_name, name, description):
        event = self._get_event(event_name)
        event.treasure.append(event.Treasure(name, description))


     # ---------- VALIDATION ----------

    def validate(self, start):
        if start not in self.game.events:
            raise ValueError(f"Start event '{start}' does not exist")

        self.game.current_event = self.game.events[start]

        for name, event in self.game.events.items():

            for option in event.options:
                if option.def_event not in self.game.events.values():
                    raise ValueError(
                        f"Option in '{name}' points to unknown event"
                    )

            if not event.options:
                continue  # terminal event is OK

            has_default = any(
                not option.required_flags and not option.required_items
                for option in event.options
            )

            if not has_default:
                raise ValueError(
                    f"Event '{name}' has only conditional options.\n"
                    "At least one option must be unconditional."
                )


    # ---------- INTERNAL ----------

        
    def _get_event(self, name):
        try:
            return self.game.events[name]
        except KeyError:
            raise ValueError(f"Event {name} does not exist")