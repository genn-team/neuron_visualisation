import bpy, bmesh, os, sys
import neuroml
import neuroml.loaders as loaders
from neuron_visualization_addon.model.Cell import Cell

class CellNeuroML2(Cell):
    '''
    This class represents brain cells in the network
    '''
    def __init__(self, cell):
        Cell.__init__(self, cell.id)
        #if id not in Cell.generated_models:
        # Remove the dummy soma
        self.blender_obj.select = True
        bpy.ops.object.delete()
        # Parse new model
        self.parse_model(cell)
        print(self.id + " model is parsed")

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
                print(d)
                bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=d, location=cell_dict[segment.id])
                # Name object as cell
                bpy.context.object.name = self.id
                # Save referrence
                self.blender_obj = bpy.context.object
            elif segment.distal.diameter > 2.0:
                d = segment.distal.diameter / 100.0
                print(d)
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

        #Cell.generated_models[self.id] = self.blender_obj
