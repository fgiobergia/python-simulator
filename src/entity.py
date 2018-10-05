from PIL import Image
import numpy as np
import json

class Color:
    def __init__(self, r, g, b, a):
        self.color = (r,g,b,a)
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def over(self, colorB):
        # self is the "top-most" color
        # TODO use alpha compositing to
        # correctly overlay colors
        # https://en.wikipedia.org/wiki/Alpha_compositing
        # (by not implementing this method,
        # the new color will always "cover" the
        # underlying one, even though the alpha channel
        # is not 1)
        pass

class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Drawable:
    def __init__(self, target, origin, rotation):
        self.target = target
        # open image & convert it to RGBA
        im = Image.open(self.target)
        imRGBA = im.convert("RGBA")

        # load size and the image itself (as an array of pixels)
        self.size = Coords(*im.size) # width, height
        self.content = np.array([ int(x) for x in imRGBA.tobytes() ]) # TODO change type to np.uint8 (check what "owner" type needs to be for frames)
        
        # close stuff that is no longer needed
        im.close()
        imRGBA.close()

        self.origin = origin # TODO make this the "center" of the image
        self.rotation = rotation
    
    def getPixel(self, coords):
        # get the 4 values contained in "content"
        # at the appropriate position and return them
        offset = (coords.y * self.size.x + coords.x) * 4
        return Color(*self.content[offset:offset + 4])


class Entity:
    # TODO: load the drawable from 
    # the appropriate file
    def __init__(self, _id, spriteFile, coords=Coords(0,0), rotation=0):
        # An entity acts in ways that
        # update the underlying Drawable,
        # which is identified by
        # - a size (width, height)
        # - a content (array of length width * height)
        # - an origin (x,y) for the top-left corner (in the canvas)
        # - a rotation (in degrees, around the center)
        # Additionally, each Entity needs to be assigned a
        # unique identifier
        self.drawable = Drawable(spriteFile, coords, rotation)
        self.id = _id
    
    # delta: amount of time
    # passed since previous 
    # update
    # (this function should update
    # some information of the drawable)
    def update(self, delta):
        pass

    def getX(self):
        return self.drawable.origin.x

    def setX(self, x):
        self.drawable.origin.x = x
    
    def getY(self):
        return self.drawable.origin.y
        
    def setY(self, y):
        self.drawable.origin.y = y

    # Draw the drawable to the frame
    def draw(self, frame):
        return frame.draw(self.drawable, hash(self.id))
    
