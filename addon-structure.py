import bpy, bmesh, os, sys

import neuroml
import neuroml.loaders as loaders

from network.Cell import Cell

cell_dict = {}

def load_cells(includes):
    for include in includes:
        cell = loaders.NeuroMLLoader.load('examples/' + include.href)
        for c in cell.cells:
            tmp = Cell(c)
            cell_dict[tmp.id] = tmp

if __name__ == '__main__':
    # --- Clean the scene ---
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # --- Parse files ---
    path = sys.argv[-1]
    if path[-8:] != '.net.nml':
        sys.exit("Please provide network file")
    network_file = loaders.NeuroMLLoader.load(sys.argv[-1])
    load_cells(network_file.includes)

    for population in network_file.networks[0].populations:
        cell = cell_dict[population.component]
        for instance in population.instances:
            x = instance.location.x / 100.0
            y = instance.location.y / 100.0
            z = instance.location.z / 100.0
            cell.update_location((x,y,z))

    # --- Render a png ---
    #bpy.data.scenes['Scene'].render.filepath ='./text.png'
    #bpy.ops.render.render(write_still=True )
