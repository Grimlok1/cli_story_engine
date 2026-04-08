from .text_color import error, success, info, title

class Renderer:     
    def render_title(self, title):
        print("*" * (len(title) + 4))
        print(f"* {title.upper()} *")
        print("*" * (len(title) + 4))
        print()

    def render_text(self, text):
        print(text)
