import bpy
from neuron_visualization_addon.model.Network import Network
from neuron_visualization_addon.model.PopulationNeuroML2 import PopulationNeuroML2

class NetworkNeuroML2(Network):
    '''
    This class represents a network
    '''
    def __init__(self, network):
        Network.__init__(self, network.id)
        self.populations = {}
        self.projections = {}
        for population in network.populations:
            self.populations[population.id] = PopulationNeuroML2(population)
        for projection in network.projections:
            for connection in projection.connection_wds:
                # Precell
                pre_cell_adress = connection.pre_cell_id.split('/')
                population_id_1 = pre_cell_adress[1]
                pre_cell = self.populations[population_id_1].cells[int(pre_cell_adress[2])]
                # Postcell
                post_cell_adress = connection.post_cell_id.split('/')
                population_id_2 = post_cell_adress[1]
                post_cell = self.populations[population_id_2].cells[int(post_cell_adress[2])]
                # Sort the projections
                projection = pre_cell.drawAxon(post_cell.getLocation(),0.2)
                if (pre_cell.id, post_cell.id) not in self.projections:
                    self.projections[(pre_cell.id, post_cell.id)] = [projection]
                else:
                    self.projections[(pre_cell.id, post_cell.id)].append(projection)
