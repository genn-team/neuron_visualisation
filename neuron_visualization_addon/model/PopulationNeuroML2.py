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
        for instance in population.instances:
            x = instance.location.x / 10
            z = instance.location.y / 10
            y = instance.location.z / 10
            self.cells[instance.id] = Cell(str(instance.id), (x,y,z))
