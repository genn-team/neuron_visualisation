import bpy, neuroml
from neuron_visualization_addon.model.Cell import Cell
from neuron_visualization_addon.model.Population import Population

class PopulationNeuroML2(Population):
    """This class represents a population of brain cells in the network based on NeuroML2"""

    def __init__(self, population):
        """The constructor.

        :param population: Population from the parser
        :type population: neuroml.population

        """
        # Call super constructor
        Population.__init__(self,
                            population.id,
                            len(population.instances),
                            population.component)
        # Create all cells
        for instance in population.instances:
            # Switch coordinates systems
            x = instance.location.x / 10
            z = instance.location.y / 10
            y = instance.location.z / 10
            # Save in a dictionary
            self.cells[instance.id] = Cell(str(instance.id), (x,y,z))
