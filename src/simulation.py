import json
from utils import PriorityQ

def load_defualt_config(config_for):
    config_file_path = "../defaults/{0}.json".format(config_for)
    f = open(config_file_path)
    if f is None:
        return {}
    return json.load(f)

class Frame:
    def __init__(self, resolution):
        self.width = resolution["width"]
        self.height = resolution["height"]
        # set up "canvas" here (i.e. a matrix of pixels)
    
    # TODO: this is going to require arguments such as
    # matrix of pixels to draw,
    # position
    # rotation
    def draw(self):
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

        for i in range(totalFrames):
            # create new image for the frame
            frame = Frame(resolution)

            # iterate over entities to update them
            # (here, the order doesn't really matter, 
            # so we can iterate over the queue without
            # too much care about its order
            for _ in self.q:
                pass

            # iterate over entities to draw them

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