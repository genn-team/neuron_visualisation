import bpy, random
import mathutils
from neuron_visualization_addon.model.Population import Population

class Network(object):
    '''
    This class represents a network
    '''
    def __init__(self, id):
        self.id = id
        self.populations = {}
        self.projections = {}

    def highlightPopulationsAll(self):
        for population in self.populations:
            self.highlightPopulation(population)

    def highlightPopulation(self, population_id):
        # TODO: Error handling
        random_color = (random.random(),
                        random.random(),
                        random.random() )
        self.populations[population_id].setColor(random_color)

    def removeHighlightAll(self):
        for _,population in self.populations.items():
            population.removeColor()

    def pullProjectionsAll(self):
        for id1, id2 in self.projections:
            if id1 != id2:
                self.pullProjections(id1, id2)

    def pullProjections(self, populationID_1, populationID_2):
        # TODO: Error handling
        projections = self.projections[(populationID_1,populationID_2)]
        middle = mathutils.Vector((0,0,0))
        for p in projections:
            middle += p.getMiddle()
        for p in projections:
            p.pullCenterTo(middle / len(projections))
