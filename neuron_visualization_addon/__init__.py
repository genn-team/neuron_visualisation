bl_info = {
    "name": "Network Visualization",
    "description": "Converts neural network description files into ",
    "author": "",
    "blender": (2, 70, 0),
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
    inputs.parser.pullProjections()
    return None

class MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

class PanelSettings(PropertyGroup):
    networkFileUpload = bpy.props.StringProperty(
        name="File Path",
        description="Provide description file",
        default="",
        subtype ='FILE_PATH'
        )
    populationHighlight = bpy.props.BoolProperty(
        name="Highlight populations",
        description="A bool property",
        default = False
        )
    populationsDropdown = bpy.props.EnumProperty(
        name="Highlight populations",
        description="Select populations to highlight",
        items=[ ('None', "None", ""),
                ('All', "All", "")
               ]
        )
    parser = Parser()
    pullProjections = bpy.props.BoolProperty(
        name = "Pull projections",
        description = "Pull projections together between populations",
        default = False,
        update = pullProjections
        )

class ParseOperator(bpy.types.Operator):
    bl_idname = "wm.parser"
    bl_label = "Parse"

    def execute(self, context):
        scene = context.scene
        inputs = scene.panelSettings
        file_type = inputs.parser.parse(inputs.networkFileUpload)
        if file_type == "network":
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

class ClearOperator(bpy.types.Operator):
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
        layout.operator("wm.clear")
        if bpy.context.scene['fileParsed']:
            layout.label(text="Model manipulation")
            layout.prop(inputs, "populationsDropdown", text="")
            layout.prop(inputs, "pullProjections")
            layout.label(text="Animation")
            layout.prop(inputs, "networkFileUpload")

@persistent
def initSceneProperties(scene):
    bpy.app.handlers.scene_update_pre.remove(initSceneProperties)
    bpy.types.Scene.fileParsed = bpy.props.BoolProperty(name='fileParsed',description='')
    scene['fileParsed'] = False
    return

def register():
    print("REGISTER")
    bpy.app.handlers.scene_update_pre.append(initSceneProperties)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.panelSettings = bpy.props.PointerProperty(type=PanelSettings)
    bpy.utils.register_class(MessageBox)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.panelSettings

if __name__ == "__main__":
    print("MAIN")
    initSceneProperties(bpy.context.scene)
    register()
