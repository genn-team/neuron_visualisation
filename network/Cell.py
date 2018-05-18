import bpy, bmesh, os, sys
import neuroml
import neuroml.loaders as loaders

class Cell:
    '''
    This class represents brain cells in the network
    '''
    def __init__(self, cell):
        self.id = cell.id
        self.parse_model(cell)
        print("Cell " + self.id + " is created")

    def parse_model(self, cell):
        '''
        Parse cell into a blender object
        '''
        # Dictionary of segment ids and locations
        cell_dict = {}

        for segment in cell.morphology.segments:

            cell_dict[segment.id] = (segment.distal.x / 100.0, segment.distal.y / 100.0, segment.distal.z / 100.0)
            if segment.parent == None:
                # Parent object (soma)
                d = segment.distal.diameter / 100.0
                bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=d, location=cell_dict[segment.id])
                # Name object as cell
                bpy.context.object.name = self.id
                # Safe referrence
                self.blender_obj = bpy.context.object
            elif segment.distal.diameter > 2.0:
                d = segment.distal.diameter / 100.0
                bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=d, location=cell_dict[segment.id])
                bpy.context.object.parent = bpy.data.objects[self.id]
            else:
                bpy.ops.object.editmode_toggle()
                # Augment the mesh
                obj = bpy.context.object
                mesh = obj.data
                bm = bmesh.from_edit_mesh(mesh)
                # Create verteces
                v1 = bm.verts.new(cell_dict[segment.id])
                v2 = bm.verts.new(cell_dict[segment.parent.segments])
                bm.edges.new((v1, v2))
                bmesh.update_edit_mesh(obj.data)

                bpy.ops.object.editmode_toggle()

    def update_location(self, location):
        self.blender_obj. location = location
