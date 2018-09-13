class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Drawable:
    def __init__(self, size, content, origin, rotation):
        self.size = size
        self.content = content
        self.origin = origin 
        self.rotation = rotation


class Entity:
    # TODO: load the drawable from 
    # the appropriate file
    def __init__(self):
        # An entity acts in ways that
        # update the underlying Drawable,
        # which is identified by
        # - a size (width, height)
        # - a content (array of length width * height)
        # - an origin (x,y) for the top-left corner (in the canvas)
        # - a rotation (in degrees, around the center)
        self.drawable = Drawable((10,10), [], (0,0), 0)
        pass

    # delta: amount of time
    # passed since previous 
    # update
    # (this function should update
    # some information of the drawable)
    def update(self, delta):
        pass
    
    # returns the Drawable object
    def draw(self):
        return self.drawable
    
