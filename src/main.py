from entity import Entity
from simulation import Simulation

if __name__ == "__main__":
    square = Entity()
    background = Entity()

    simulation = Simulation()

    simulation.addEntity(square)
    simulation.addEntity(background)

    simulation.run()