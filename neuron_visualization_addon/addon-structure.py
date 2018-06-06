import bpy, bmesh, os, sys

import neuroml
import neuroml.loaders as loaders

from neuron_visualization_addon.model.CellNeuroML2 import CellNeuroML2
#from neuron_visualization_addon.model.PopulationNeuroML2 import PopulationNeuroML2
from neuron_visualization_addon.model.NetworkNeuroML2 import NetworkNeuroML2
from neuron_visualization_addon.model.Cell import Cell

cell_dict = {}

def load_cells(includes):
    for include in includes:
        if include.href[-9:] != '.cell.nml':
            continue
        cell = loaders.NeuroMLLoader.load('examples/' + include.href)
        print('examples/' + include.href)
        for c in cell.cells:
            tmp = CellNeuroML2(c)
            cell_dict[tmp.id] = tmp

if __name__ == '__main__':
    # --- Clean the scene ---
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    #cell1 = Cell('test1')
    #cell1.setLocation((1.0, 0.0, 0.0))

    #cell2 = Cell('test2')
    #cell2.setLocation((2.0, 1.0, 3.0))

    #cell1.drawAxon(0.2, cell2.getLocation())

    # --- Parse files ---
    path = sys.argv[-1]
    if path[-8:] != '.net.nml':
        sys.exit("Please provide a network file")
    network_file = loaders.NeuroMLLoader.load(sys.argv[-1])
    if len(network_file.includes) != 0:
        load_cells(network_file.includes)

    network = NetworkNeuroML2(network_file.networks[0])
    population = network.populations['L6_UTPC']
    print(population)
    print(population.getLocation())

    # --- Render a png ---
    #bpy.data.scenes['Scene'].render.filepath ='./text.png'
    #bpy.ops.render.render(write_still=True )
