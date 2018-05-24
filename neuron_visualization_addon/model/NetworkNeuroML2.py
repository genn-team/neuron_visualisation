import bpy
from neuron_visualization_addon.model.Network import Network

class NetworkNeuroML2(Network):
    '''
    This class represents a network
    '''
    def __init__(self, id, network):
        Network.__init__(self, network.id)
        self.populations = {}
        for population in network.networks[0].populations:
            self.populations[population.id] = PopulationNeuroML2(population)
