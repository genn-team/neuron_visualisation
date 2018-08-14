import bpy, random, mathutils
from neuron_visualization_addon.model.Population import Population

class Network(object):
    """
    This class represents a network. Network consists of populations and projections between them.
    """

    def __init__(self, id):
        """The constructor.

        :param id: The network ID.
        :type id: string

        """
        self.id = id
        self.populations = {}
        self.projections = {}

    @property
    def location(self):
        """Location of the center of mass.

        :type location: Vector
        """
        location_sum = mathutils.Vector((0,0,0))
        for _, population in self.populations.items():
            location_sum += population.location
        return location_sum / len(self.populations)

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
        if not population_id in self.populations:
            raise ValueError('Population ID not found')
        random_color = (random.random(),
                        random.random(),
                        random.random() )
        self.populations[population_id].setColor(random_color)

    def removeHighlightAll(self):
        """Removes highlight from all populations."""
        for _,population in self.populations.items():
            population.removeColor()

    def pullProjectionsAll(self, strength):
        """Pulls all projections to the center of their mass.

        :param strength: Pulling strength
        :type strength: int
        """
        for id1, id2 in self.projections:
            if id1 != id2:
                self.pullProjections(id1, id2, strength)

    def pullProjections(self, populationID_1, populationID_2, strength):
        """Pull projections between two populations.

        :param populationID_1: First population ID
        :type populationID_1: string
        :param populationID_2: Second population ID
        :type populationID_2: string
        :param strength: Pulling strength
        :type strength: int
        """
        projections = self.projections[(populationID_1,populationID_2)]
        # Calculate the center of mass
        middle = mathutils.Vector((0,0,0))
        for p in projections:
            middle += p.middle
        # Set the center
        for p in projections:
            p.pullCenterTo(middle / len(projections), strength)

    def animateSpikes(self, spikes, colorMap='jet', animateAxons=True):
        """ Animate network.

        :param spikes: Dictionary of cell IDs as keys and a tuple of time and intensity as values
        :type spikes: dict
        """
        for cell_id in spikes:
            for _, population in self.populations.items():
                if cell_id in population.cells:
                    population.cells[cell_id].setSpikes(spikes[cell_id], colorMap)
                    continue
