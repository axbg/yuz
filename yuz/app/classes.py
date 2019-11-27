

class Photo:
    def __init__(self, original):
        self._original = original
        self._cropped = []

    def get_original(self):
        return self._original

    def add_cropped_photo(self, cropped):
        self._cropped.append(cropped)