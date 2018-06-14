import bpy, random
from neuron_visualization_addon.model.Population import Population

class Network(object):
    '''
    This class represents a network
    '''
    def __init__(self, id):
        self.id = id
        self.populations = {}
        self.projections = {}

    def highlightPopulation(self, population_id):
        # TODO: Error handling
        random_color = (random.random(),
                        random.random(),
                        random.random() )
        self.populations[population_id].setColor(random_color)
        #self.populations[population_id].pullTogether()
