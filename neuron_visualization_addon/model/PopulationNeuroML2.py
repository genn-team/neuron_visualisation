import bpy, neuroml
from neuron_visualization_addon.model.Cell import Cell
from neuron_visualization_addon.model.Population import Population

class PopulationNeuroML2(Population):
    """This class represents a population of brain cells in the network based on NeuroML2"""

    def __init__(self, population, scale=10, loaded_cells={}):
        """The constructor.

        :param population: Population from the parser
        :type population: neuroml.population
        :param scale: Scale of a model (DEFAULT: 1:10)
        :type scale: int
        :param loaded_cells: Dictionary of loaded cell models
        :type loaded_cells: dictionary

        """
        # Call super constructor
        Population.__init__(self,
                            population.id,
                            len(population.instances),
                            population.component)
        # Create all cells
        for instance in population.instances:
            # Switch coordinates systems
            x = instance.location.x / scale
            z = instance.location.y / scale
            y = instance.location.z / scale
            # Save in a dictionary
            # TODO
            #if population.component in loaded_cells:
            #    loaded_cells[population.component].location = (x,y,z)
            #else:
            self.cells[instance.id] = Cell(str(instance.id), (x,y,z))
