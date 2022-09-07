import bpy

class MoveObject(bpy.types.Operator):
    """Moves the object.

    Simple operator to test the functionality.
    """

    bl_idname = "scene.move_object"
    bl_label = "Move object"

    def execute(self, context):
        """Executes the MoveObject operator."""
        obj = context.active_object

        obj.location.x += 2.0

        return {'FINISHED'}

class GenerateArmature(bpy.types.Operator):
    """Generates the armature necessary for motion capture."""

    bl_idname = "scene.generate_armature"
    bl_label = "Generate Armature"

    def execute(self, context):
        """Executes the GenerateArmature operator."""

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.bone_primitive_add(name="Bone")

        return {'FINISHED'}
