class Singleton:
    """
    A singleton decorator that makes easy to implement the behaviour on any class.
    Shameless implementation from https://stackoverflow.com/a/7346105
    Classes decorated with Singleton must be initialized with :code:`instance()` 
    instead  of :code:`Foo()`, e.g. Bus.instance()
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            # Penality only when used the first time
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError(
            'Constructor should not be used to create singletons, use instance()')

    def __instancecheck__(self, instance):
        return isinstance(instance, self._decorated)
