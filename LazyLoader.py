class LazyLoader:
    _utility = None
    _arcrane = None

    @staticmethod
    def get_utility():
        if LazyLoader._utility is None:
            from Utilities import Utilities  # Import only when needed
            LazyLoader._utility = Utilities()
        return LazyLoader._utility

    @staticmethod
    def get_arcrane():
        if LazyLoader._arcrane is None:
            from Arcrane import Arcrane  # Import only when needed
            LazyLoader._arcrane = Arcrane()
        return LazyLoader._arcrane


