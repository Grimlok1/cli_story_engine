from .Story_node import StoryNode, Choice, Description, Timer, Counter

class StoryFactory:
    def __init__(self):
        self.nodes = {}

    def node(self, *, name, text, **optional_arguments):
        node = StoryNode(name, text, **optional_arguments)
        self.check_node(node) #check if node already exists
        self.nodes[name] = node
        return node
    
    def treasure(self):
        pass

    def choice(self, *, node_name, text, target, **optional_arguments):
        node = self.get_node(node_name) #get StoryNode object
        choice = Choice(text, target, **optional_arguments)
        node.choices.append(choice)
        return choice
    
    def description(self, *, node_name, text, **optional_arguments):
        node = self.get_node(node_name)
        description = Description(text, **optional_arguments)
        node.descriptions.append(description)
        return description
        
    def next_node(self, *, node_name, next_node, **parameters):
        node = self.get_node(node_name)
        node.store_next_node(next_node, **parameters)

    def validate_story(self, *, start_node_name):
        all_nodes = self.nodes.values()
        self.start_node = self.get_node(self, start_node_name)
        self.change_node(self.start_node) #set start node as current_node

        for node in all_nodes:
            if node.default_next_node:
                node.default_next_node = self.get_node(node.default_next_node)
        
            for next_node in node.next_nodes:
                next_node["node"] = self.get_node(self, next_node["node"])
                
            for choice in node.choices:
                choice.targets = [
                    self.get_node(self, target)
                    for target in choice.targets
                ]
                
    #call this and pass the return value to Game()
    def build(self, *, start_node_name):
        self.validate_story(start_node_name)
        return self.nodes
    
    def check_node(self, name):
        if name in self.nodes.keys():
            raise ValueError(f"StoryNode {name} already exists")
    
    def get_node(self, name):
        try:
            return self.nodes[name]
        except KeyError:
            raise ValueError(f"StoryNode {name} does not exist")