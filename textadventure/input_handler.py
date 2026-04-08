class InputHandler:
    def handle_user_input(game, user_input): #user_input should be something like: 1, 2, 3, 4
        choices = game.current_story_node.get_choices(game)

        if user_input in choices.keys():
            choice = choices[user_input]
        
        if choice.transition:
            game.renderer.render_text(choice.transition)
            input("Continue...")
        choice.resolve()
        game.change_node(game.get_target(choice))