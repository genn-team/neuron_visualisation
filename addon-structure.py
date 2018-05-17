import bpy, bmesh, os, sys
import neuroml
import neuroml.loaders as loaders

if __name__ == '__main__':
    # --- Clean the scene ---
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # --- Parse files ---
    path = sys.argv[-1]
    if path[-8:] != '.net.nml':
        sys.exit("Please provide network file")
    network_file = loaders.NeuroMLLoader.load(sys.argv[-1])

    for population in network_file.networks[0].populations:
        for instance in population.instances:
            print("New instance is being processed")
            x = instance.location.x / 100.0
            y = instance.location.y / 100.0
            z = instance.location.z / 100.0
            cell = loaders.NeuroMLLoader.load('cADpyr229_L23_PC_5ecbf9b163_0_0.cell.nml')
            cell_dict = {}
            for segment in cell.cells[0].morphology.segments:
                cell_dict[segment.id] = (segment.distal.x / 100.0 + x, segment.distal.y / 100.0 + y, segment.distal.z / 100.0 + z)
                print("New segment is being processed")
                if segment.parent == None or segment.distal.diameter > 2.0:
                    d = segment.distal.diameter / 100.0
                    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=d,location=cell_dict[segment.id])
                else:
                    bpy.ops.object.editmode_toggle()
                    obj = bpy.context.object
                    me = obj.data
                    bm = bmesh.from_edit_mesh(me)

                    v1 = bm.verts.new(cell_dict[segment.id])
                    v2 = bm.verts.new(cell_dict[segment.parent.segments])

                    bm.edges.new((v1, v2))

                    bmesh.update_edit_mesh(obj.data)
                    bpy.ops.object.editmode_toggle()

    #cell = loaders.NeuroMLLoader.load(network_file.includes[0].href)

    # --- Render a png ---
    #bpy.data.scenes['Scene'].render.filepath ='./text.png'
    #bpy.ops.render.render(write_still=True )
