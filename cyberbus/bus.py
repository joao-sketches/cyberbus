# -*- coding: utf-8 -*-
# todo add parameters to be hable to print notifications etc.
from .singleton import Singleton
from multiprocessing.pool import ThreadPool


@Singleton
class Bus:

    def __init__(self):
        """
        Constructor of Bus, this method is not callable, it will raise when
        :code:`Bus()` is invoked, instead to acquire a instance call :code:`Bus.instance()`
        """
        # initialize subscriptions
        self.subscriptions = list()
        self.executor = ThreadPool()

    def notify(self, event, payload):
        """
        Notify the subscriptions of :code:`event` to handle the payload
        :param event: they event where the payload will be sent
        :param payload: the content to subscriber handle
        :return self:
        """
        if not isinstance(event, str):
            raise ValueError('event must be a string')

        for s in self.subscriptions:
            if event in s:
                function = s[1]
                self.executor.apply(func=function, args=([payload]))

    def subscribe(self, event, handler):
        """
        Register the :code:`handler` to handle the incoming payload once it
        is notified.
        The handler takes one parameter and must return None, or else the
        return value will be ignored.
        A subscription is a tuple formed by the event name and the handler
        :param event: the event to bind the handler to
        :param handler: handle the payload
        :return self:
        """
        if not callable(handler):
            raise ValueError('handler must be a callable')
        if not isinstance(event, str):
            raise ValueError('event must be a string')

        for s in self.subscriptions:
            if event in s:
                raise ValueError(
                    'handler already registed to event: {}'.format(event))

        subscription = (event, handler)
        self.subscriptions.append(subscription)

        return self

    def unsubscribe(self, event):
        """
        Unsubscribe from the event, unregistering the handler of it and
        allowing for a resubscription.
        :param event: the name of the event to unsubscribe
        """
        if not isinstance(event, str):
            raise ValueError('event must be a string')

        for s in self.subscriptions:
            if event in s:
                self.subscriptions.remove(s)

        return self
