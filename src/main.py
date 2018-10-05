from entity import Entity, Coords
from simulation import Simulation

if __name__ == "__main__":
    square = Entity(1, "../assets/mario.png", Coords(50,50))
    background = Entity(2, "../assets/background.png", Coords(0,0))

    simulation = Simulation("../configs/simulation.json")

    simulation.addEntity(square)
    simulation.addEntity(background)

    simulation.run()