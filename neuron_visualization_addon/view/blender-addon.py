bl_info = {
    "name": "Network Visualization",
    "description": "Converts neural network description files into ",
    "author": "",
    "blender": (2, 70, 0),
    "location": "3D View > Tools Props",
    "category": "Development"
}

import bpy
from bpy.props import *
from bpy.types import Panel, Operator, PropertyGroup

from neuron_visualization_addon.controller.Parser import Parser

def populationHighlight(self, context):
    scene = context.scene
    inputs = scene.panelSettings
    inputs.parser.highlightPopulation(inputs.populationsDropdown)
    return None

class PanelSettings(PropertyGroup):
    networkFileUpload = StringProperty(
        name="File Path",
        description="Provide description file",
        default="",
        subtype ='FILE_PATH'
        )
    populationHighlight = BoolProperty(
        name="Highlight populations",
        description="A bool property",
        default = False
        )
    populationsDropdown = EnumProperty(
        name="Highlight populations",
        description="Select populations to highlight",
        items=[ ('None', "None", ""),
                ('All', "All", "")
               ]
        )
    parser = Parser()

class ParseOperator(bpy.types.Operator):
    bl_idname = "wm.parser"
    bl_label = "Parse"

    def execute(self, context):
        scene = context.scene
        inputs = scene.panelSettings
        inputs.parser.parse(inputs.networkFileUpload)
        self.updateDropdown(inputs.parser.getPopulations())
        bpy.context.scene['fileParsed'] = True
        return {'FINISHED'}

    def updateDropdown(self, populations):
        enumProp, panelSettings = PanelSettings.populationsDropdown
        for p in populations:
            panelSettings['items'].append((p, p, ""))
        PanelSettings.populationsDropdown = EnumProperty(
            name="Highlight populations",
            description="Select populations to highlight",
            items=panelSettings['items'],
            update=populationHighlight
            )

class MainPanel(Panel):
    bl_idname = "MainPanel"
    bl_label = "Network Visualization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        inputs = scene.panelSettings

        layout.prop(inputs, "networkFileUpload")
        layout.operator("wm.parser")
        if bpy.context.scene['fileParsed']:
            layout.prop(inputs, "populationsDropdown", text="")

def initSceneProperties(scene):
    bpy.types.Scene.fileParsed = BoolProperty(name='fileParsed',description='')
    scene['fileParsed'] = False
    return

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.panelSettings = PointerProperty(type=PanelSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.panelSettings

if __name__ == "__main__":
    initSceneProperties(bpy.context.scene)
    register()
