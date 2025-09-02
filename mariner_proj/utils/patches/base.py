class BasePatch:
    """
    Base class for patches that can be applied to multiple classes.
    examples usage:
    ```
    class MyPatch(BasePatch):
        def apply(self):
            # apply patch to self.target_class
            pass
    ```
    """

    def apply(self):
        pass
