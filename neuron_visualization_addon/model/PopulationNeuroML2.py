import bpy, neuroml
from neuron_visualization_addon.model.Cell import Cell
from neuron_visualization_addon.model.Population import Population

class PopulationNeuroML2(Population):
    '''
    This class represents a population of brain cells in the network
    '''
    def __init__(self, population):
        Population.__init__(self,
                            population.id,
                            len(population.instances),
                            population.component)
        i = 0
        for instance in population.instances:
            x = instance.location.x / 100
            z = instance.location.y / 100
            y = instance.location.z / 100
            self.cells[i].setLocation((x,y,z))
            i += 1
