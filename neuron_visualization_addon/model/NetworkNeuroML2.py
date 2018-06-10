import bpy
from neuron_visualization_addon.model.Network import Network
from neuron_visualization_addon.model.PopulationNeuroML2 import PopulationNeuroML2

class NetworkNeuroML2(Network):
    '''
    This class represents a network
    '''
    def __init__(self, network):
        Network.__init__(self, network.id)
        for population in network.populations:
            self.populations[population.id] = PopulationNeuroML2(population)
        print(self.populations)
        for projection in network.projections:
            firstPopulationID = projection.presynaptic_population
            secondPopulationID = projection.postsynaptic_population
            for connection in projection.connection_wds:
                # Precell
                pre_cell_adress = connection.pre_cell_id.split('/')
                pre_cell = self.populations[firstPopulationID].cells[int(pre_cell_adress[-1])]
                # Postcell
                post_cell_adress = connection.post_cell_id.split('/')
                post_cell = self.populations[secondPopulationID].cells[int(post_cell_adress[-1])]
                # Sort the projections
                projection = pre_cell.drawAxon(post_cell.getLocation(),0.2)

                if (firstPopulationID,secondPopulationID) not in self.projections:
                    self.projections[(firstPopulationID,secondPopulationID)] = [projection]
                else:
                    self.projections[(firstPopulationID,secondPopulationID)].append(projection)
