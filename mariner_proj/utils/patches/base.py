class BasePatch:
    """

    Base class for patches that can be applied to multiple classes.
    examples usage:
    ```
    from arches.app.some.module import target_class_or_obj

    def patch_target_function_or_object():
        # define patch logic here
        pass

    class MyPatch(BasePatch):
        def apply(self):
            # apply patch
            target_class_or_obj.some_method = patched_some_method
    ```

    Add patch modules to the /utils/patches directory

    """

    def apply(self):
        pass
