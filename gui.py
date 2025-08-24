from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Log

class TUI(App):
    """A Textual app to display LLM reactions."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    TITLE = "AI Video Watching Buddy"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reaction_log = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        self.reaction_log = Log(highlight=True)
        yield self.reaction_log
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def write_to_log(self, text: str):
        """Write text to the log."""
        if self.reaction_log:
            self.reaction_log.write(text)

    def new_reaction(self):
        """Adds a separator for a new reaction"""
        if self.reaction_log:
            self.reaction_log.write("\n---\n")


if __name__ == "__main__":
    # Example Usage
    import time
    from threading import Thread

    app = TUI()

    def stream_text():
        """Simulates streaming text to the TUI."""
        time.sleep(1) # Wait for app to be ready
        app.new_reaction()
        app.write_to_log("This is a simulated reaction. ")
        time.sleep(1)
        app.write_to_log("It streams word by word. ")
        time.sleep(1)
        app.write_to_log("Isn't that cool?")

        time.sleep(2)
        app.new_reaction()
        app.write_to_log("Here is another one! ")
        time.sleep(1)
        app.write_to_log("To show how it works.")


    # Run the text streaming in a separate thread
    thread = Thread(target=stream_text)
    thread.start()

    app.run()
    thread.join()
    print("Example finished.")
