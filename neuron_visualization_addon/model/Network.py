import bpy, random
import mathutils
from neuron_visualization_addon.model.Population import Population

class Network(object):
    """
    Network class.
    Network consists of populations and projections between them.
    """

    def __init__(self, id):
        """The constructor.

        :param id: The network ID.
        :type id: string

        """
        self.id = id
        self.populations = {}
        self.projections = {}

    def highlightPopulationsAll(self):
        """Highlights all populations with random colors.
        """
        for population in self.populations:
            self.highlightPopulation(population)

    def highlightPopulation(self, population_id):
        """Highlights a population with a random color.

        :param population_id: The population ID.
        :type population_id: string

        """
        # TODO: Error handling
        random_color = (random.random(),
                        random.random(),
                        random.random() )
        self.populations[population_id].setColor(random_color)

    def removeHighlightAll(self):
        """Removes highlight from all populations."""
        for _,population in self.populations.items():
            population.removeColor()

    def pullProjectionsAll(self):
        """Pulls all projections to the center of their mass."""
        for id1, id2 in self.projections:
            if id1 != id2:
                self.pullProjections(id1, id2)

    def pullProjections(self, populationID_1, populationID_2):
        """Pull projections between two populations.

        :param populationID_1: First population ID
        :type populationID_1: string
        :param populationID_2: Second population ID
        :type populationID_2: string

        """
        # TODO: Error handling
        projections = self.projections[(populationID_1,populationID_2)]
        # Calculate the center of mass
        middle = mathutils.Vector((0,0,0))
        for p in projections:
            middle += p.getMiddle()
        # Set the center
        for p in projections:
            p.pullCenterTo(middle / len(projections))

    def animateSpikes(self, spikes):
        """ Animate network.

        :param spikes: Dictionary of cell IDs as keys and a tuple of time and intensity as values
        :type spikes: dict

        """
        for cell_id in spikes:
            for _, population in self.populations.items():
                if cell_id in population.cells:
                    population.cells[cell_id].setSpikes(spikes[cell_id])
                    continue
