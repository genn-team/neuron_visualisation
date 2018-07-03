import bpy, bmesh, os, sys

import neuroml
import neuroml.loaders as loaders

from neuron_visualization_addon.model.CellNeuroML2 import CellNeuroML2
from neuron_visualization_addon.model.NetworkNeuroML2 import NetworkNeuroML2
from neuron_visualization_addon.model.Cell import Cell

class Parser(object):
    def parse(self, filepath):
        if filepath[-8:] == '.net.nml' or filepath[-4:] == '.xml':
            # TODO
            network_file = loaders.NeuroMLLoader.load(filepath)
            if len(network_file.includes) != 0:
                self.loadCellsNeuroML2(os.path.dirname(filepath), network_file.includes)
            self.network = NetworkNeuroML2(network_file.networks[0])
            return "network"
        elif filepath[-3:] == '.st':
            activation_file = open(filepath)
            spikes = {}
            for line in activation_file.read().splitlines():
                words = line.split(" ")
                spikes[int(words[1])] = float(words[0])
            self.network.animateSpikes(spikes)
            return "activation"

    def loadCellsNeuroML2(self, dirpath, includes):
        cell_dict = {}
        for include in includes:
            if include.href[-9:] != '.cell.nml':
                continue
            cell = loaders.NeuroMLLoader.load(os.path.join(dirpath,include.href))
            for c in cell.cells:
                tmp = CellNeuroML2(c)
                cell_dict[tmp.id] = tmp
        return cell_dict

    def getPopulations(self):
        return self.network.populations.keys()

    def highlightPopulation(self, populationID):
        if populationID == 'All':
            self.network.highlightPopulationsAll()
        elif populationID == 'None':
            self.network.removeHighlightAll()
        else:
            self.network.highlightPopulation(populationID)

    def pullProjections(self):
        self.network.pullProjectionsAll()
