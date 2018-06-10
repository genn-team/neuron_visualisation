import bpy, bmesh, os, sys
import neuroml
import mathutils
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

    def parse_model(self, cell):
        '''
        Parse cell into a blender object
        '''
        # Dictionary of segment ids and locations
        # TODO fix measuremt units
        cell_dict = {}
        axon = []
        for segment in cell.morphology.segments:
            if(len(cell_dict) > 150):
                break
            cell_dict[segment.id] = (segment.distal.x / 10.0, segment.distal.y / 10.0, segment.distal.z / 10.0)
            if segment.parent == None:
                # Parent object (soma)
                d = segment.distal.diameter / 10.0
                bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=d, location=cell_dict[segment.id])
                # Name object as cell
                bpy.context.object.name = self.id
                # Save referrence
                self.blender_obj = bpy.context.object
            elif segment.distal.diameter > 2.0:
                d = segment.distal.diameter / 10.0
                bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=d, location=cell_dict[segment.id])
                bpy.context.object.parent = bpy.data.objects[self.id]
            elif segment.parent.segments + 1 == segment.id:
                #print(type(self.getLocation()))
                axon.append(mathutils.Vector(cell_dict[segment.id])) #- self.getLocation())
            else:
                # Create curve, curve object and set Cell as a parent
                cu = bpy.data.curves.new('AxonCurve', 'CURVE')
                ob = bpy.data.objects.new(str(segment.id), cu)
                bpy.context.scene.objects.link(ob)
                ob.parent = self.blender_obj

                # Create bevel object
                bpy.ops.curve.primitive_bezier_circle_add(radius=segment.distal.diameter/ 10.0)
                cu.bevel_object = bpy.context.object

                # Create spline and set Bezier control points
                spline_axon = cu.splines.new('BEZIER')
                spline_axon.bezier_points.add(len(axon))
                for n in range(len(axon)):
                    bpt = spline_axon.bezier_points[n+1]
                    bpt.co = bpt.handle_left = bpt.handle_right = axon[n]
                axon = [cell_dict[segment.id]]
        #Cell.generated_models[self.id] = self.blender_obj
