class Shape():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle(Shape):
    def __init__(self, width, height, x=0, y=0):
        super().__init__(x, y)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val


class Square(Rectangle):
    def __init__(self, side, x=0, y=0):
        super().__init__(side, side, x, y)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val
        self._height = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val
        self._width = val


def main():
    rec = Rectangle(5, 10)
    rec.width = 30
    rec.height = 20
    print(rec.__dict__)

    sq = Square(5)
    sq.width = 30
    sq.height = 20
    print(sq.__dict__)

main()
