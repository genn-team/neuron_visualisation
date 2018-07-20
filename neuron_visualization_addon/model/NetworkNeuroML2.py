import bpy
from neuron_visualization_addon.model.Network import Network
from neuron_visualization_addon.model.PopulationNeuroML2 import PopulationNeuroML2

## This class represents a network read from NeuroML file
class NetworkNeuroML2(Network):

    ## The constructor
    def __init__(self, network):
        # Call parent class constructor
        Network.__init__(self, network.id)
        # Create populations
        for population in network.populations:
            self.populations[population.id] = PopulationNeuroML2(population)
        # Create projections between populations
        for projection in network.projections:
            firstPopulationID = projection.presynaptic_population
            secondPopulationID = projection.postsynaptic_population
            # If connections_wd are given
            if len(projection.connection_wds) > 0:
                for connection in projection.connection_wds:
                    # Precell
                    pre_cell_adress = connection.pre_cell_id.split('/')
                    pre_cell = self.populations[firstPopulationID].cells[int(pre_cell_adress[-2])]
                    # Postcell
                    post_cell_adress = connection.post_cell_id.split('/')
                    post_cell = self.populations[secondPopulationID].cells[int(post_cell_adress[-2])]
                    # Sort the projections
                    projection = pre_cell.drawAxon(0.2, post_cell)

                    if (firstPopulationID,secondPopulationID) not in self.projections:
                        self.projections[(firstPopulationID,secondPopulationID)] = [projection]
                    else:
                        self.projections[(firstPopulationID,secondPopulationID)].append(projection)
            # If connections are given
            '''if len(projection.connections) > 0:
                for connection in projection.connections:
                    # Precell
                    pre_cell_adress = connection.pre_cell_id.split('/')
                    pre_cell = self.populations[firstPopulationID].cells[int(pre_cell_adress[-2])]
                    # Postcell
                    post_cell_adress = connection.post_cell_id.split('/')
                    post_cell = self.populations[secondPopulationID].cells[int(post_cell_adress[-2])]
                    # Sort the projections
                    projection = pre_cell.drawAxon(0.2, post_cell)

                    if (firstPopulationID,secondPopulationID) not in self.projections:
                        self.projections[(firstPopulationID,secondPopulationID)] = [projection]
                    else:
                        self.projections[(firstPopulationID,secondPopulationID)].append(projection)'''
