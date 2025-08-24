import ollama
import threading

class LLMClient:
    def __init__(self, model='gemma3', reaction_callback=None):
        self.model = model
        self.reaction_callback = reaction_callback
        self.history = [
            {
                'role': 'system',
                'content': (
                    "You are a video-watching buddy. "
                    "You will be given transcribed text from a video. "
                    "Your task is to react to the text in a short, conversational, and interesting way. "
                    "Keep your reactions to one or two sentences. "
                    "Be insightful, funny, or ask a question. "
                    "Do not repeat the transcribed text."
                )
            }
        ]

    def get_reaction(self, text):
        """Gets a reaction from the LLM for the given text."""
        # Add the user's message to the history
        self.history.append({'role': 'user', 'content': text})

        # Start the streaming response in a new thread
        threading.Thread(target=self._stream_reaction).start()

    def _stream_reaction(self):
        """Streams the reaction from the LLM."""
        full_response = ""
        try:
            stream = ollama.chat(
                model=self.model,
                messages=self.history,
                stream=True,
            )
            for chunk in stream:
                content = chunk['message']['content']
                full_response += content
                if self.reaction_callback:
                    self.reaction_callback(content)

            # Add the assistant's response to the history
            self.history.append({'role': 'assistant', 'content': full_response})

            # Keep history to a reasonable size
            if len(self.history) > 10:
                # Keep the system message and the last 9 messages
                self.history = [self.history[0]] + self.history[-9:]

        except Exception as e:
            print(f"Error getting reaction from LLM: {e}")
            if self.reaction_callback:
                self.reaction_callback(f"\n[Error: {e}]")


if __name__ == '__main__':
    # Example Usage
    import time

    def my_reaction_callback(chunk):
        print(chunk, end='', flush=True)

    llm_client = LLMClient(reaction_callback=my_reaction_callback)

    print("Getting reaction for: 'That's one small step for man, one giant leap for mankind.'")
    llm_client.get_reaction("That's one small step for man, one giant leap for mankind.")

    # Keep the main thread alive to see the streaming response
    time.sleep(10)

    print("\n\nGetting reaction for: 'I am your father.'")
    llm_client.get_reaction("I am your father.")

    time.sleep(10)
    print("\n\nExample finished.")
