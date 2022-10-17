import bpy

class MotionCapturePanel(bpy.types.Panel):
    """Motion Capture Panel."""

    bl_label = "Motion Capture"
    bl_idname = "OBJECT_PT_MOTION_CAPTURE"
    bl_category = "Mocap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_context = "object"

    solution_enum: bpy.props.EnumProperty(name="Solution",
        items=[("Pose", "Pose", ""),
               ("Hands", "Hands", ""),
               ("Face", "Face", "")]
    )

    frames = 0

    def draw(self, context):
        """Draw the user interface."""

        self.draw_solution()
        self.draw_webcam()
        self.draw_video()
        self.draw_animation()

    def draw_solution(self):
        """Draw the UI for the solution box."""

        solution_box = self.layout.box()

        row = solution_box.row()
        row.split()
        row.label(text="Solution:")
        row.operator("scene.select_solution")

        row = solution_box.row()
        row.split()
        row.operator("scene.generate_armature")
        row.operator("scene.link_armature")

        self.layout.separator()

    def draw_webcam(self):
        """Draw the UI for the webcam box."""

        webcam_box = self.layout.box()

        row = webcam_box.row()
        row.split()
        row.label(text="Webcam")

        row = webcam_box.row()
        row.split()
        row.operator("scene.start_camera_capture")
        row.operator("scene.stop_camera_capture")

        self.layout.separator()

    def draw_video(self):
        """Draw the UI for the video box."""

        video_box = self.layout.box()

        row = video_box.row()
        row.split()
        row.label(text="Video")
        row = video_box.row()
        row.operator("scene.select_file")
        row.operator("scene.extract_keypoints")
        self.layout.separator()

    def draw_animation(self):
        """Draw the UI for the animation box."""

        animation_box = self.layout.box()

        row = animation_box.row()
        row.split()
        row.label(text="Animation")
        row = animation_box.row()
        row.split()
        row.label(text="Frames: " + str(self.frames))
        row.operator("scene.create_animation")