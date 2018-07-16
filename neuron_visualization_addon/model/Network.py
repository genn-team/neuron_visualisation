import bpy, random
import mathutils
from neuron_visualization_addon.model.Population import Population

## This class represents a network
# which consists of populations and projections
# between them
class Network(object):

    ## The constructor
    # @param id   The network ID
    def __init__(self, id):
        self.id = id
        self.populations = {}
        self.projections = {}

    ## Highlights all populations with random colors
    def highlightPopulationsAll(self):
        for population in self.populations:
            self.highlightPopulation(population)

    ## Highlights a population with a random color
    # @param population_id   ID of a population
    def highlightPopulation(self, population_id):
        # TODO: Error handling
        random_color = (random.random(),
                        random.random(),
                        random.random() )
        self.populations[population_id].setColor(random_color)

    ## Removes highlight from all populations
    def removeHighlightAll(self):
        for _,population in self.populations.items():
            population.removeColor()

    ## Pulls all projections to the center of their mass
    def pullProjectionsAll(self):
        for id1, id2 in self.projections:
            if id1 != id2:
                self.pullProjections(id1, id2)

    ## Pull projections between two populations
    # @param populationID_1   First population ID
    # @param populationID_2   Second population ID
    def pullProjections(self, populationID_1, populationID_2):
        # TODO: Error handling
        projections = self.projections[(populationID_1,populationID_2)]
        # Calculate the center of mass
        middle = mathutils.Vector((0,0,0))
        for p in projections:
            middle += p.getMiddle()
        # Set the center
        for p in projections:
            p.pullCenterTo(middle / len(projections))

    ## Animate network
    # @param spikes   Dictionary of cell IDs and a tupple of time and intensity
    def animateSpikes(self, spikes):
        for cell_id in spikes:
            for _, population in self.populations.items():
                if cell_id in population.cells:
                    population.cells[cell_id].setSpikes(spikes[cell_id])
                    continue
