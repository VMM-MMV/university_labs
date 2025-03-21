import os
import json

class SearchBuffer:
    def __init__(self, buffer_file="search_buffer.json"):
        self.buffer_file = buffer_file
        self.load_buffer()

    def load_buffer(self):
        if os.path.exists(self.buffer_file):
            with open(self.buffer_file, "r", encoding="utf-8") as f:
                try:
                    self.buffer = json.load(f)
                except json.JSONDecodeError:
                    self.buffer = []
        else:
            self.buffer = []

    def save_buffer(self):
        with open(self.buffer_file, "w", encoding="utf-8") as f:
            json.dump(self.buffer, f, indent=4)

    def update_buffer(self, results):
        self.buffer = results
        self.save_buffer()

    def get_buffer(self):
        return self.buffer