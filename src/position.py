

class Position:

    def __init__(self, x, y, similarity, name, minx=0, miny=0, maxx=1280, maxy=720) -> None:
        self.x = x
        self.y = y
        self.similarty = similarity
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.name = name

    @staticmethod
    def clamp(x, min, max):
        '''限制一个数在[min,max]'''
        if x < min:
            return min
        if x > max:
            return max
        return x

    def get_pos(self):
        '''返回Position类的坐标（经过clamp）'''
        x = Position.clamp(self.x, self.minx, self.maxx)
        y = Position.clamp(self.y, self.miny, self.maxy)
        return (x, y)
