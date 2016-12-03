class Sprite:
    def __init__(self, text):
        self.lines = text.split('\n')
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        if not self.width or not self.height:
            raise ValueError
        for line in self.lines:
            if len(line) != self.width:
                raise ValueError

    @staticmethod
    def from_file(filename):
        with open(filename) as f:
            return Sprite(f.read())

    def draw(self, canvas, pos):
        x, y = pos
        for sprite_y, canvas_y in zip(range(self.height), range(y, y + self.height)):
            if canvas_y < 0 or canvas_y >= len(canvas):
                continue
            for sprite_x, canvas_x in zip(range(self.width), range(x, x + self.width)):
                if canvas_x < 0 or canvas_x >= len(canvas[0]):
                    continue
                canvas[canvas_y][canvas_x] = self.lines[sprite_y][sprite_x]
