import bpy, bmesh, os, sys

import neuroml
import neuroml.loaders as loaders

from neuron_visualization_addon.model.CellNeuroML2 import CellNeuroML2
from neuron_visualization_addon.model.PopulationNeuroML2 import PopulationNeuroML2

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

    populations = {}
    for population in network_file.networks[0].populations:
        populations[population.id] = PopulationNeuroML2(population)
    for projection in network_file.networks[0].projections:
        for connection in projection.connection_wds:
            pre_cell_adress = connection.pre_cell_id.split('/')
            pre_cell = populations[pre_cell_adress[1]].cells[int(pre_cell_adress[2])]
            post_cell_adress = connection.post_cell_id.split('/')
            post_cell = populations[post_cell_adress[1]].cells[int(post_cell_adress[2])]
            bpy.ops.object.editmode_toggle()
            # Augment the mesh
            pre_cell.blender_obj.select = True
            obj = bpy.context.object
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            # Create verteces
            print(pre_cell.getLocation())
            print(post_cell.getLocation())
            v1 = bm.verts.new(pre_cell.getLocation())
            v2 = bm.verts.new(post_cell.getLocation())
            bm.edges.new((v1, v2))
            bmesh.update_edit_mesh(obj.data)
            bpy.ops.object.editmode_toggle()
    # --- Render a png ---
    #bpy.data.scenes['Scene'].render.filepath ='./text.png'
    #bpy.ops.render.render(write_still=True )
