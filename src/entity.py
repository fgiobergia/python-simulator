from simulation import Color

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
    
    def getColor(self, coords):
        # get the 4 values contained in "content"
        # at the appropriate position and return them
        return Color(*self.content[(coords.y * self.size.x + coords.x) * 4:4])


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
        # Additionally, each Entity needs to be assigned a
        # unique identifier
        self.drawable = Drawable(Coords(10,10), [], Coords(0,0), 0)
        self.id = "bloop"
        pass

    # delta: amount of time
    # passed since previous 
    # update
    # (this function should update
    # some information of the drawable)
    def update(self, delta):
        pass
    
    # Draw the drawable to the frame
    def draw(self, frame):
        return frame.draw(self.drawable, self.id)
    
