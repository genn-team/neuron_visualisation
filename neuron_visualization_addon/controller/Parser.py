import bpy, bmesh, os, sys

import neuroml
import neuroml.loaders as loaders

from neuron_visualization_addon.model.CellNeuroML2 import CellNeuroML2
from neuron_visualization_addon.model.NetworkNeuroML2 import NetworkNeuroML2
from neuron_visualization_addon.model.Cell import Cell

class Parser(object):
    def parse(self, filepath, populationHighlight):
        print(filepath)
        if filepath[-8:] == '.net.nml':
            network_file = loaders.NeuroMLLoader.load(filepath)
            if len(network_file.includes) != 0:
                self.loadCellsNeuroML2(network_file.includes)

        network = NetworkNeuroML2(network_file.networks[0], populationHighlight)

    def loadCellsNeuroML2(self, includes):
        cell_dict = {}
        for include in includes:
            if include.href[-9:] != '.cell.nml':
                continue
            cell = loaders.NeuroMLLoader.load('examples/' + include.href)
            for c in cell.cells:
                tmp = CellNeuroML2(c)
                cell_dict[tmp.id] = tmp
        return cell_dict