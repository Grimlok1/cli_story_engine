from game import Event, ConditionalEvent

class StoryBuilder:
    def __init__(self, game):
        self.game = game

    def event(self, name, description):
        if name in self.game.events:
            raise ValueError(f"Event {name} already exists")

        self.game.events[name] = Event(description)
        
    def conditional_event(self, name, description, required_flags=None, required_items=None):
        if name in self.game.conditional_events:
            raise ValueError(f"Event {name} already exists")
            
        self.game.conditional_events[name] = ConditionalEvent(description, required_flags, required_items) 

    def option(self, from_event, description, to_event, *, conditional_events=None, required_flags=None, required_items=None, flag=None):
        source = self._get_event(from_event)
        def_event = self._get_event(to_event)
        
        if conditional_events: #ärsyttävä bugi jos ei anna listaa parametrinä conditional_eventsille
            conditional_events_obj = [self._get_conditional_event(name) for name in conditional_events]
        else:
            conditional_events_obj = None

        source.options.append(source.Option(description, def_event, conditional_events_obj, required_flags, required_items, flag))

    def treasure(self, event_name, name, description):
        event = self._get_event(event_name)
        event.treasure.append(event.Treasure(name, description))


     # ---------- VALIDATION ----------

    def validate(self, start):
        #ConditionalEvent cannot be a start event
        if start not in self.game.events:
            raise ValueError(f"Start event '{start}' does not exist")

        self.game.start = self.game.events[start]

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
            
    def _get_conditional_event(self, name):
        try:
            return self.game.conditional_events[name]
        except KeyError:
            raise ValueError(f"ConditionalEvent {name} does not exist")
        