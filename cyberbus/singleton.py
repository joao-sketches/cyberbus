class Singleton:
    """
    A singleton decorator that makes easy to implement the behaviour on any class.
    Shameless implementation from https://stackoverflow.com/a/7346105
    Classes decorated with Singleton must be initialized with :code:`instance()` 
    instead  of :code:`Foo()`, e.g. Bus.instance()
    """

    def __init__(self, decorated):
        self._decorated = decorated


    def configure(self, **kwargs):
        """
        Set configuration arguments to the decorated class, allowing customizations
        on the first init of it, if invoked when a instance already exists it will
        raise :code:`ConfigurationNotAllowed` exception.
        """

        # do not ask forgiveness here because we are computing a condition
        # expressed by the presence of this attribute, rather than using it
        # and accessing it.
        if hasattr(self, '_instance'):
            raise ConfigurationNotAllowed(
                    'Do not pass configuration to an already created instance')
        else:
            self.props = kwargs

        return self

    def instance(self):
        """
        Get the current instance of the class, if one is not yet created,
        it will be using the constructor, notice that this is the only way
        to create a new instance.
        """
        try:
            return self._instance
        except AttributeError:
            """
            Initialize a new instance of the decorated class, passing to __init__
            the received properties, so it can self configure.
            """
            self._instance = self._decorated(self.props)
            return self._instance

    def __call__(self):
        raise TypeError(
            'Constructor should not be used to create singletons, use instance()')

    def __instancecheck__(self, instance):
        return isinstance(instance, self._decorated)


class ConfigurationNotAllowed(Exception):
    pass
