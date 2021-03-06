import json
import numpy as np
from utils import PriorityQ
from entity import Drawable, Coords, Color
from PIL import Image


def load_default_config(config_for):
    config_file_path = "../defaults/{0}.json".format(config_for)
    f = open(config_file_path)
    if f is None:
        return {}
    return json.load(f)

class Frame:
    itemsPerPixel = 5 # red, green, blue, alpha, owner

    def __init__(self, resolution):
        self.size = Coords(resolution["width"], resolution["height"])
        # set up "canvas" here (i.e. a matrix of pixels)
        # For each frame, 5 pieces of information are stored
        # r, g, b, a: red, green, blue, alpha information of the pixel
        # e: "writing" entity: needed to identify "who" wrote that pixel
        #    (useful for detecting collisions) (0 -> nobody)
        self.canvas = np.zeros(self.size.y * self.size.x * Frame.itemsPerPixel)
    
    def setBgColor(self, color):
        self.canvas = np.tile([*color.color, 0], self.size.y * self.size.x)

    # draw a drawable to the canvas
    # if a collision is detected,it should
    # return an id of the "collided" object
    def draw(self, drawable, entityId):
        # collisions are stored in a set and
        # eventually returned (multiple collisions
        # with the same entity will only be
        # returned once)
        collisions = set({})
        for i_ in range(drawable.size.y):
            for j_ in range(drawable.size.x):
                i = i_ + int(drawable.origin.y)
                j = j_ + int(drawable.origin.x)
                # TODO use rotation matrix to rotate
                # (i,j) by an angle `drawable.rotation`
                if i >= 0 and i < self.size.y and j >= 0 and j < self.size.x:
                    # pixel is within the frame's
                    # boundaries and can thus be drawn
                    pos = (i * self.size.x + j) * Frame.itemsPerPixel
                    if drawable.size.x == 100 and i_ == 0 and j_ == 0:
                        print(pos)
                    color = drawable.getPixel(Coords(j_, i_))
                    # if the pixel is completely transparent,
                    # skip it (and ignore collisions)
                    if color.a == 0:
                        continue
                    pr,pg,pb,pa,owner = self.canvas[pos:pos+Frame.itemsPerPixel]
                    if owner != 0 and owner != entityId:
                        # the pixel had previously been drawn
                        # by someone else (!= 0) who isn't the
                        # current entity (it might happen, with
                        # rotations, that the same pixel is drawn
                        # multiple times by the same entity)
                        collisions.add(owner)
                    prevColor = Color(pr,pg,pb,pa)
                    color.over(prevColor)
                    # draw the new pixel to the canvas
                    # (the new "owner" of the pixel is
                    # the latest drawer (previous ones
                    # are overwritten))
                    self.canvas[pos:pos+Frame.itemsPerPixel] = [*color.color, entityId]
        return collisions # return a collision array for the caller to handle

    # TODO: this method "compresses" the image by
    # removing the information about "who" wrote
    # each pixel -- this results in a reduction in
    # space of 1/5 (this should be run after all
    # entities have been drawn and there no longer
    # is a need to store information about collisions)
    def compress(self):
        pass

class Simulation:
    def __init__(self, configFile=None):
        self.configFile = configFile
        defaultConfig = load_default_config("Simulation")

        if self.configFile is not None:
            f = open(self.configFile)

            if f is None:
                raise Exception("Cannot open configuration file")
            config = json.load(f)
        else:
            config = {}

        self._config = { **defaultConfig, **config }

        self.q = PriorityQ()
    

    def config(self, key, default=None):
        return self._config.get(key, default)
        
    def run(self):
        totalFrames = self.config("durationSeconds") * self.config("frameRate")
        delta = self.config("frameRate")**-1
        # TODO: if `frames` gets too large, alternative non-volatile-memory-based
        # solutions should be considered (e.g. store on disk)
        self.frames = [] # this will contain a list of all the frames
        resolution = self.config("resolution")

        for i in range(totalFrames):
            # create new image for the frame
            frame = Frame(resolution)
            if self.config("bgColor") is not None:
                frame.setBgColor(Color(*self.config("bgColor")))
            

            # iterate over entities to update them
            for _, entity in self.q:
                entity.update(delta)

            # iterate over entities to draw them
            for _, entity in self.q:
                entity.draw(frame)

            # store frame
            frame.compress()
            #self.frames.append(frame) # currently storing frames on disk

            w = self.config('resolution')['width']
            h = self.config('resolution')['height']
            v = np.reshape([ np.uint8(frame.canvas[j*5:j*5+3]) for j in range(w*h) ], (h, w, 3))
            print(v.shape)

            im = Image.fromarray(v, "RGB")
            im.save("test{0}.png".format(i))
            im.close()
        
        # add an entity to the queue of
    # entities (with priority `priority`)
    # (highest priorities are drawn top-most)
    # by default, it should draw on top of
    # everything else (queue.peek().priority + 1)
    def addEntity(self, entity, priority=None):
        if priority is None:
            try:
                priority = self.q.peek()[0] + 1
            except IndexError:
                priority = 0 # empty queue, let's start from 0
        self.q.put((priority, entity))