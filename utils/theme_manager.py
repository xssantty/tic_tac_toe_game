class ThemeManager:
    def init(self):
        self.light_theme = {
            'bg': (255, 255, 255),
            'line': (0, 0, 0),
            'circle': (0, 0, 255),
            'cross': (255, 0, 0),
            'text': (0, 0, 0)
        }
        self.dark_theme = {
            'bg': (0, 0, 0),
            'line': (255, 255, 255),
            'circle': (0, 255, 255),
            'cross': (255, 0, 255),
            'text': (255, 255, 255)
        }
        self.current_theme = self.light_theme

    def get_theme(self):
        return self.current_theme

    def toggle_theme(self):
        self.current_theme = self.dark_theme if self.current_theme == self.light_theme else self.light_theme
        return self.current_theme
