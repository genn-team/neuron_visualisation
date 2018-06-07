bl_info = {
    "name": "Network Visualization",
    "description": "Converts neural network description files into ",
    "author": "",
    "blender": (2, 70, 0),
    "location": "3D View > Tools",
    "category": "Development"
}

import bpy
from bpy.props import StringProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup

from neuron_visualization_addon.controller.Parser import Parser

class PanelSettings(PropertyGroup):

    networkFileUpload = StringProperty(
        name="File Path",
        description="Provide description file",
        default="",
        subtype ='FILE_PATH'
        )

class ParseOperator(bpy.types.Operator):
    bl_idname = "wm.parser"
    bl_label = "Parse"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        Parser().parse(mytool.networkFileUpload)
        return {'FINISHED'}

class MainPanel(Panel):
    bl_idname = "MainPanel"
    bl_label = "Network Visualization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "networkFileUpload")
        layout.operator("wm.parser")


def register():
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(MainPanel)
    bpy.types.Scene.my_tool = PointerProperty(type=PanelSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
