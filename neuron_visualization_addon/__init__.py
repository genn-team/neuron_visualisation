bl_info = {
    "name": "Network Visualization",
    "description": "Converts neural network description files into 3D models",
    "author": "",
    "blender": (2, 79, 0),
    "location": "3D View > Tools Props",
    "category": "3D View"
}

import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.app.handlers import persistent

from neuron_visualization_addon.controller.Parser import Parser

def populationHighlight(self, context):
    scene = context.scene
    inputs = scene.panelSettings
    inputs.parser.highlightPopulation(inputs.populationsDropdown)
    return None

def pullProjections(self, context):
    scene = context.scene
    inputs = scene.panelSettings
    inputs.parser.pullProjections(inputs.pullProjections)
    return None

def rotateCamera(self, context):
    scene = context.scene
    inputs = scene.panelSettings
    inputs.parser.rotateCamera()
    return None

class PanelSettings(PropertyGroup):
    """
    Class of panel elements

    :param networkFileUpload: string filepath to model or animation file
    :param cameraRotation: boolean that indicates whether camera should be rotated
    :param populationsDropdown: dropdown of population IDs
    :param colorMapDropdown: dropdown of available color maps
    :param parser: pointer to the parser instance
    :param pullProjections: int that indicates whether the projections between populations should be pulled
    """

    networkFileUpload = bpy.props.StringProperty(
        name="File Path",
        description="Provide description file",
        default="",
        subtype ='FILE_PATH'
        )
    cameraRotation = bpy.props.BoolProperty(
        name="Rotate camera",
        description="Rotate the camera around the objects",
        default = False,
        update = rotateCamera
        )
    populationsDropdown = bpy.props.EnumProperty(
        name="Highlight populations",
        description="Select populations to highlight",
        items=[ ('None', "None", ""),
                ('All', "All", "")
               ]
        )
    colorMapDropdown = bpy.props.EnumProperty(
        name="Color Map",
        description="Select color map for animation",
        items=[]
        )
    parser = Parser()
    pullProjections = bpy.props.IntProperty(
        name = "Pull projections",
        description = "Pull projections together in a 'sand-clock' form between populations",
        default = 0,
        soft_min = 0,
        soft_max = 3,
        update = pullProjections
        )
    modelScale = bpy.props.IntProperty(
        name = "Model scale:  1 ",
        description = "How many Blender units correspond to a unit defined in your file",
        default = 10,
        step = 10,
        subtype = 'FACTOR',
        soft_min = 1,
        soft_max = 100
        )


class ParseOperator(bpy.types.Operator):
    """
    Operator that parses the file into a model or animation
    """
    bl_idname = "wm.parser"
    bl_label = "Parse"

    def execute(self, context):
        scene = context.scene
        inputs = scene.panelSettings
        file_type = inputs.parser.parse(inputs.networkFileUpload, inputs.modelScale, inputs.colorMapDropdown)
        if file_type == "network":
            self.updateDropdowns(inputs.parser)
            bpy.context.scene['fileParsed'] = True
        return {'FINISHED'}

    def updateDropdowns(self, parser):
        # Population dropdown
        _, panelSettings = PanelSettings.populationsDropdown
        for p in parser.populations:
            panelSettings['items'].append((p, p, ""))
        PanelSettings.populationsDropdown = bpy.props.EnumProperty(
            name="Highlight populations",
            description="Select populations to highlight",
            items=panelSettings['items'],
            update=populationHighlight
            )
        # Color map dropdown
        items = [(i,i,'') for i in parser.colorMaps]
        PanelSettings.colorMapDropdown = bpy.props.EnumProperty(
            name="Color map",
            description="Select color map for animation",
            items=items
            )

class ClearOperator(bpy.types.Operator):
    """
    Operator that clears the objects from the scene
    """

    bl_idname = "wm.clear"
    bl_label = "Clear All"

    def execute(self, context):
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
        bpy.ops.object.select_by_type(type='CURVE')
        bpy.ops.object.delete()
        PanelSettings.populationsDropdown = bpy.props.EnumProperty(
            name="Highlight populations",
            description="Select populations to highlight",
            items=[ ('None', "None", ""),
                    ('All', "All", "")
                   ],
            update=populationHighlight
            )
        bpy.context.scene['fileParsed'] = False
        return {'FINISHED'}

class MainPanel(Panel):
    """
    Main panel that the user sees
    """
    bl_idname = "MainPanel"
    bl_label = "Network Visualization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        inputs = scene.panelSettings

        # Initial layout with a filepath, parse and clear buttons
        layout.prop(inputs, "networkFileUpload")
        layout.prop(inputs, "modelScale")
        row = layout.row()
        row.operator("wm.parser")
        row.operator("wm.clear")
        # Unfold the rest, once the network was parsed
        if bpy.context.scene['fileParsed']:
            # --- Model manipulation ---
            layout.label(text="Model manipulation")
            layout.prop(inputs, "populationsDropdown", text="")
            layout.prop(inputs, "pullProjections")
            # --- Animation ---
            layout.label(text="Animation")
            layout.prop(inputs, "networkFileUpload")
            layout.prop(inputs, "colorMapDropdown", text="")
            layout.operator("wm.parser")
            layout.prop(inputs, "cameraRotation")

@persistent
def initSceneProperties(scene):
    bpy.app.handlers.scene_update_pre.remove(initSceneProperties)
    bpy.types.Scene.fileParsed = bpy.props.BoolProperty(name='fileParsed',description='')
    scene['fileParsed'] = False
    return

def register():
    bpy.app.handlers.scene_update_pre.append(initSceneProperties)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.panelSettings = bpy.props.PointerProperty(type=PanelSettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.panelSettings

if __name__ == "__main__":
    initSceneProperties(bpy.context.scene)
    register()
