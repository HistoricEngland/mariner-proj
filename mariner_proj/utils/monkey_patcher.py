import os
from inspect import isclass, getmembers

from mariner_proj.utils.patches.base import BasePatch


def apply_monkey_patches():
    print("Applying monkey patches...")

    patches_dir = os.path.join(os.path.dirname(__file__), "patches")
    for filename in os.listdir(patches_dir):
        if filename.endswith(".py"):
            module_name = f"mariner_proj.utils.patches.{filename[:-3]}"
            module = __import__(module_name, fromlist=[""])
            for name, obj in getmembers(module):
                if isclass(obj) and issubclass(obj, BasePatch):
                    obj().apply()

    print("All monkey patches applied successfully!")
