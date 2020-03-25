class Photo:
    def __init__(self, original):
        self._original = original
        self._cropped = []

    def get_original(self):
        return self._original

    def get_cropped(self):
        return self._cropped

    def add_cropped_photo(self, photo):
        self._cropped.append(photo)
