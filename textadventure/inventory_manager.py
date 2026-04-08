class InventoryManager:
    def get_inventory(self, inventory):
        return {str(index) : element for (index, element) in enumerate(inventory, start=1)}
        
    def check_for_item(self, inventory, item_name):
        return item_name in inventory
        
    def add_item(self, item, inventory):
        if item not in inventory:
            inventory.append(item)
            item.take()
            
    def render_inventory(self, game, inventory): #render the content of the bag
        self.render_title("Backpack")
        inventory = game.inventory_manager.get_inventory(inventory)
        if inventory:
            for key, item in inventory.items():
                print(f"{key}. {item.name}")
        else:
            print("Backpack is empty")
        print(f"{len(inventory) + 1}. Close backpack")
    
