import bpy

class MotionCapturePanel(bpy.types.Panel):
    """Motion Capture Panel."""

    bl_label = "Motion Capture"
    bl_idname = "OBJECT_PT_MOTION_CAPTURE"
    bl_category = "Mocap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_context = "object"

    def draw(self, context):
        """Draw the user interface."""

        layout = self.layout

        row = layout.row()
        row.operator("scene.move_object")

        row = layout.row()
        row.operator("scene.generate_armature")
