import json
import numpy as np
from utils import PriorityQ
from entity import Drawable

def load_defualt_config(config_for):
    config_file_path = "../defaults/{0}.json".format(config_for)
    f = open(config_file_path)
    if f is None:
        return {}
    return json.load(f)

class Color:
    def __init__(self, r, g, b, a):
        self.color = (r,g,b,a)

class Frame:
    def __init__(self, resolution):
        self.width = resolution["width"]
        self.height = resolution["height"]
        # set up "canvas" here (i.e. a matrix of pixels)
        # For each frame, 5 pieces of information are stored
        # r, g, b, a: red, green, blue, alpha information of the pixel
        # e: "writing" entity: needed to identify "who" wrote that pixel
        #    (useful for detecting collisions) (0 -> nobody)
        self.canvas = np.zeros(self.height * self.width * 5) # 5 -> (r,g,b,a,e)
    
    def setBgColor(self, color):
        self.canvas(np.tile([*color.color, 0], self.height * self.width))

    # draw a drawable to the canvas
    # if a collision is detected,it should
    # return an id of the "collided" object
    def draw(self, drawable):
        pass

    # this method "compresses" the image by
    # removing the information about "who" wrote
    # each pixel -- this results in a reduction in
    # space of 1/5 (this should be run after all
    # entities have been drawn and there no longer
    # is a need to store information about collisions)
    def compress(self):
        pass

class Simulation:
    def __init__(self, configFile):
        self.configFile = configFile
        defaultConfig = load_defualt_config("simulation")

        f = open(self.configFile)

        if f is None:
            raise Exception("Cannot open configuration file")

        self._config = { **defaultConfig, **json.load(f) }

        self.q = PriorityQ()
    

    def config(self, key, default=None):
        return self._config.get(key, default)
        
    def run(self):
        totalFrames = self.config("durationSeconds") * self.config("frameRate")
        # TODO: if `frames` gets too large, alternative non-volatile-memory-based
        # solutions should be considered (e.g. store on disk)
        frames = [] # this will contain a list of all the frames
        resolution = self.config("resolution")

        for _ in range(totalFrames):
            # create new image for the frame
            frame = Frame(resolution)

            # iterate over entities to update them
            for _, entity in self.q:
                drawable = entity.draw()
                frame.draw(drawable) # TODO check return value (there may be a collision occurring here)

            # iterate over entities to draw them
            for _ in self.q:
                pass

            # store frame
            frames.append(frame)
    
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