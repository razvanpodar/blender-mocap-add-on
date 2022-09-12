"""Blender motion capture add-on."""

from pathlib import Path
import subprocess
import sys

if "bpy" in locals():
    import importlib
    importlib.reload(motion_capture)
    importlib.reload(operators)
    importlib.reload(user_interface)
    print("Reloaded files!")
else:
    from . import motion_capture
    from . import operators
    from . import user_interface

import bpy
from bpy.app.handlers import persistent

bl_info = {
    "name": "Motion Capture",
    "blender": (3, 0, 0),
    "category": "Animation"
}

# def install_modules():
#     python_exe = str(sys.executable)
#     lib = Path(python_exe).parent.parent / "lib"

#     # subprocess.call([python_exe, "-m", "ensurepip", "--user"])
#     # subprocess.call([python_exe, "-m", "pip", "install", "--upgrade",
#         # "pip"])

#     try:
#         import mediapipe
#         print("LOG: Mediapipe imported!")
#     except ModuleNotFoundError:
#         print("LOG: Mediapipe missing! Installing...")

#         subprocess.call([python_exe, "-m", "pip", "install", 
#             f"--target={str(lib)}", "mediapipe"])
#         print("LOG: Mediapipe installed!")
#         import mediapipe

#     try:
#         import cv2
#         print("LOG: OpenCV imported!")
#     except ModuleNotFoundError:
#         print("LOG: OpenCV missing! Installing...")
#         subprocess.call([python_exe, "-m", "pip", "install", 
#             f"--target={str(lib)}", "opencv-python"])
#         print("LOG: OpenCV installed!")
#         import cv2

def register():
    """Register classes."""
    print("Motion Capture enabled!")

    bpy.utils.register_class(user_interface.MotionCapturePanel)
    bpy.utils.register_class(operators.MoveObject)
    bpy.utils.register_class(operators.GenerateArmature)
    bpy.utils.register_class(operators.LinkArmature)
    bpy.utils.register_class(operators.StartCameraCapture)
    bpy.utils.register_class(operators.StopCameraCapture)

def unregister():
    """Unregister classes."""
    print("Motion Capture disabled!")
    bpy.utils.unregister_class(user_interface.MotionCapturePanel)
    bpy.utils.unregister_class(operators.MoveObject)
    bpy.utils.unregister_class(operators.GenerateArmature)
    bpy.utils.unregister_class(operators.LinkArmature)
    bpy.utils.unregister_class(operators.StartCameraCapture)
    bpy.utils.unregister_class(operators.StopCameraCapture)
