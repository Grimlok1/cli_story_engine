from .Story_node import StoryNode, Choice, Description, Timer, Counter

class StoryFactory:
    def create_story_node(self, *, name, text, **optional_arguments):
        _check_story_node(self, name)
        self.story_nodes[name] = StoryNode(name, text, **optional_arguments)
        
    def create_choice(self, *, node, text: str, target: str, **optional_arguments):
        story_node = _get_story_node(self, node) #get StoryNode object
        choice = Choice(text, target, **optional_arguments)
        story_node.choices.append(choice)
        
    def create_description(self, *, node, text, **optional_arguments):
        story_node = _get_story_node(self, node)
        story_node.descriptions.add_description(Description(text, **optional_arguments))
        
    def next_story_node(self, *, node, next_node, **parameters):
        node = _get_story_node(self, node)
        node.store_next_node(next_node, **parameters)
        
    def create_timer(self, *, duration):
        self.timer = Timer(duration)
        
    def create_counter(self, name, max_count, nodes, **optional_arguments):
        self.counters[name] = Counter(max_count, nodes, **optional_arguments)
        
    def on_enter(self, node, function, *args):
        story_node = _get_story_node(self, node)
        story_node.on_enter.append(lambda: function(*args))
        
    def on_update(self, node, function):
        story_node = _get_story_node(self, node)
        story_node.on_update = function
        
    def add_callback(self, time, function, *args):
        self.timer.add_callback(time, lambda: function(*args))
        
def _check_story_node(game, name):
    if name in game.story_nodes.keys():
        raise ValueError(f"StoryNode {name} already exists")