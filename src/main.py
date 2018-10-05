from entity import Entity, Coords
from simulation import Simulation

class Mario(Entity):
    def update(self, delta):
        self.setY(self.getY() + delta * 10)

if __name__ == "__main__":
    mario = Mario(1, "../assets/mario.png", Coords(50,50))
    background = Entity(2, "../assets/background.png", Coords(0,0))

    simulation = Simulation("../configs/simulation.json")

    simulation.addEntity(background)
    simulation.addEntity(mario)

    simulation.run()