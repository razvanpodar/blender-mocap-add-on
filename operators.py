import bpy
from . import motion_capture

class SelectSolution(bpy.types.Operator):
    """Select the Motion Capture Solution."""

    bl_idname = "scene.select_solution"
    bl_label = "Select Solution"

    solution_enum: bpy.props.EnumProperty(name="Solution",
        items=[("Pose", "Pose", ""),
               ("Hands", "Hands", ""),
               ("Face", "Face", "")]
    )

    def execute(self, context):
        """Executes the SelectSolution operator."""

        return {'FINISHED'}

    def invoke(self, context, event):
        """Invoke the solution dialog."""
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        """Display the options for the solution."""
        self.layout.prop(self, "solution_enum")
        return {'FINISHED'}

class GenerateArmature(bpy.types.Operator):
    """Generates the armature necessary for motion capture."""

    bl_idname = "scene.generate_armature"
    bl_label = "Generate Armature"

    def execute(self, context):
        """Executes the GenerateArmature operator."""

        # if (bpy.data.armatures["Pose"]):
        #     print("There is already an armature!")
        #     self.report({"WARNING"}, "There is already an armature!")
        # return {'CANCELED'}

        self.generate_pose(context)

        return {'FINISHED'}

    def generate_pose(self, context):
        """Generate armature for full body pose."""

        desired_name = "FullBody"

        bpy.ops.object.armature_add(radius=0.5, enter_editmode=True)
        context.active_object.name = desired_name
        object_name = context.active_object.name
        context.active_object.data.name = "Armature_FB"
        armature_name = context.active_object.data.name
        context.active_bone.name = "Spine_FB_0"

        spine_base = context.active_bone
        print(spine_base)

        self.extrude_move_bone(context, "Spine_FB_1", (0, 0, 0.5))
        self.extrude_move_bone(context, "Spine_FB_2", (0, 0, 0.5))
        self.extrude_move_bone(context, "Spine_FB_3", (0, 0, 0.5))

        spine_top = context.active_bone

        self.generate_arm(context, "Left")
        self.select_bone(context, spine_base, False, True, False)
        self.generate_leg(context, "Left", spine_base)

        self.select_bone(context, spine_top, False, False, True)
        self.extrude_move_bone(context, "Neck_FB", (0, 0, 0.25))
        self.extrude_move_bone(context, "Head_FB", (0, 0, 0.75))

        self.select_bone(context, spine_top, False, False, True)
        self.generate_arm(context, "Right")
        self.select_bone(context, spine_base, False, True, False)
        self.generate_leg(context, "Right", spine_base)

    def generate_arm(self, context, side):
        """Generates the bones of the arm."""
        if side == "Left":
            scalar = -1
        elif side == "Right":
            scalar = 1
        else:
            return

        self.extrude_move_bone(context, side + "Shoulder_FB",
            (0, scalar * 0.5, 0))
        self.extrude_move_bone(context, side + "UpperArm_FB",
            (0, scalar * 0.2, -1))
        self.extrude_move_bone(context, side + "LowerArm_FB",
            (0, 0, -1))
        self.extrude_move_bone(context, side + "Hand_FB",
            (0, 0, -0.4))

        # wrist = context.active_bone
        # self.generate_hand(context, side, wrist)

    def generate_hand(self, context, side, wrist):
        """Generates the bones of the hand.

        Used only in case it is needed a more detailed hand.
        !! IN DEVELOPMENT !!
        """
        if side == "Left":
            scalar = -1
        elif side == "Right":
            scalar = 1
        else:
            return

        self.select_bone(context, wrist, False, False, True)
        self.extrude_move_bone(context, side + "MetacarpalThumb_FB",
            (0.05, scalar * 0.01, -0.1))
        self.select_bone(context, wrist, False, False, True)

        self.extrude_move_bone(context, side + "MetacarpalIndex_FB",
            (0.025, scalar * 0.01, -0.2))
        self.select_bone(context, wrist, False, False, True)

        self.extrude_move_bone(context, side + "MetacarpalMiddle_FB",
            (0, scalar * 0.01, -0.2))
        self.select_bone(context, wrist, False, False, True)

        self.extrude_move_bone(context, side + "MetacarpalRing_FB",
            (-0.025, scalar * 0.01, -0.175))
        self.select_bone(context, wrist, False, False, True)

        self.extrude_move_bone(context, side + "MetacarpalLittle_FB",
            (-0.05, scalar * 0.01, -0.15))

    def generate_leg(self, context, side, spine_base):
        """Generates the bones of the leg."""
        if side == "Left":
            scalar = -1
        elif side == "Right":
            scalar = 1
        else:
            return

        self.extrude_move_bone(context, side + "Hip_FB",
            (0, scalar * 0.35, 0.1))
        context.active_bone.parent = spine_base
        self.extrude_move_bone(context, side + "UpperLeg_FB",
            (0, scalar * 0.2, -1.25))
        self.extrude_move_bone(context, side + "LowerLeg_FB",
            (0, 0, -1.25))
        ankle = context.active_bone
        self.extrude_move_bone(context, side + "Heel_FB",
            (0, 0, -0.25))
        self.select_bone(context, ankle, False, False, True)
        self.extrude_move_bone(context, side + "Foot_FB",
            (0.35, 0, -0.25))

    def generate_foot(self, context, side):
        """Generates the bones of the foot."""

    def select_bone(self, context, bone, select: bool, head: bool,
                    tail: bool):
        """Selects the bone passed as argument."""
        context.active_bone.select = False
        context.active_bone.select_head = False
        context.active_bone.select_tail = False

        bone.select = select
        bone.select_head = head
        bone.select_tail = tail

    def extrude_move_bone(self, context, name, transform):
        """Adds new bone by extruding it from the last bone."""
        bpy.ops.armature.extrude_move(
            ARMATURE_OT_extrude={"forked":True},
            TRANSFORM_OT_translate={"value": transform}
        )
        context.active_bone.name = name

class LinkArmature(bpy.types.Operator):
    """Links bones from blender to mediapipe keypoints."""

    bl_idname = "scene.link_armature"
    bl_label = "Link Armature"

    def execute(self, context):
        """Executes the LinkArmature operator."""

        return {'FINISHED'}

mocap = motion_capture.MotionCapture()

class StartCameraCapture(bpy.types.Operator):
    """Starts the camera capture thread."""

    bl_idname = "scene.start_camera_capture"
    bl_label = "Start capture"

    def execute(self, context):
        """Starts the thread when the operator is executed."""

        print("Operator executed")

        mocap.start_camera_capture()
        mocap.start()

        return {'FINISHED'}

class StopCameraCapture(bpy.types.Operator):
    """Stops the camera capture thread."""

    bl_idname = "scene.stop_camera_capture"
    bl_label = "Stop capture"


    def execute(self, context):
        """Stops the thread when the operator is executed."""

        print("Operator executed")

        mocap.stop_camera_capture()

        return {'FINISHED'}


class SelectFile(bpy.types.Operator):
    """Selects the file from which to extract the keypoints 
    for motion capture."""

    bl_idname = "scene.select_file"
    bl_label = "Select File"

    def execute(self, context):
        """Executes the SelectFile operator."""

        print("Selecting the file...")

        return {'FINISHED'}

class ExtractKeypoints(bpy.types.Operator):
    """Extracts the keypoints from the video file selected."""

    bl_idname = "scene.extract_keypoints"
    bl_label = "Extract Keypoints"

    def execute(self, context):
        """Executes the ExtractKeypoints operator."""

        print("Extracting the keypoints...")

class CreateAnimation(bpy.types.Operator):
    """Maps the keypoints to the pose for each frame of the animation."""

    bl_idname = "scene.create_animation"
    bl_label = "Create Animation"

    def execute(self, context):
        """Executes the CreateAnimation operator."""

        print("Creating the animation...")
