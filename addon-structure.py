import bpy, bmesh, os, sys

import neuroml
import neuroml.loaders as loaders

from network.CellNeuroML2 import CellNeuroML2
from network.PopulationNeuroML2 import PopulationNeuroML2

cell_dict = {}

def load_cells(includes):
    for include in includes:
        if include.href[-9:] != '.cell.nml':
            continue
        cell = loaders.NeuroMLLoader.load('examples/' + include.href)
        for c in cell.cells:
            tmp = CellNeuroML2(c)
            cell_dict[tmp.id] = tmp

if __name__ == '__main__':
    # --- Clean the scene ---
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # --- Parse files ---
    path = sys.argv[-1]
    if path[-8:] != '.net.nml':
        sys.exit("Please provide a network file")
    network_file = loaders.NeuroMLLoader.load(sys.argv[-1])
    if len(network_file.includes) != 0:
        load_cells(network_file.includes)

    populations = []
    for population in network_file.networks[0].populations:
        populations.append(PopulationNeuroML2(population))

    # --- Render a png ---
    #bpy.data.scenes['Scene'].render.filepath ='./text.png'
    #bpy.ops.render.render(write_still=True )
