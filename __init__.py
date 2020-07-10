bl_info = {
    "name": "Example Menu",
    "description": "Example menu",
    "author": "Mark C",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "SHIFT + ALT + Q",
    "warning": "",
    "wiki_url": "",
    "category": "User Interface" }

import bpy


class SimpleCustomMenu(bpy.types.Menu):
    bl_label = "Simple Custom Menu"
    bl_idname = "OBJECT_MT_simple_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile", icon='FILEBROWSER')
        layout.operator("wm.save_as_mainfile", icon='FILE_BACKUP')
        layout.operator("object.add_sphereplane", icon='SURFACE_NSPHERE')
        layout.operator("object.add_bevelledcube", icon='META_CUBE')


class SpherePlane(bpy.types.Operator):
    bl_idname = "object.add_sphereplane"
    bl_label = "SpherePlane"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.ops.transform.resize(value=(6, 6, 6), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.ops.object.shade_smooth()
        bpy.ops.transform.translate(value=(0, 0, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        return {'FINISHED'}

class BevelledCube(bpy.types.Operator):
    bl_idname = "object.add_bevelledcube"
    bl_label = "BevelledCube"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].segments = 6
        bpy.ops.object.shade_smooth()

        return {'FINISHED'}

classes = (
    SimpleCustomMenu,
    SpherePlane,
    BevelledCube
    )

def register():

    addon_keymaps = []


    for cls in classes:
        bpy.utils.register_class(cls)
    wm = bpy.context.window_manager
    kc = bpy.context.window_manager.keyconfigs.addon
    if wm.keyconfigs.addon:

        km = wm.keyconfigs.addon.keymaps.new(name = "Window",space_type='EMPTY', region_type='WINDOW')

        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS' ,alt=True, shift=True)
        kmi.properties.name = "OBJECT_MT_simple_custom_menu"


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
