# -*- coding: utf-8 -*-

from functools import wraps
from multiprocessing.pool import ThreadPool

from .singleton import Singleton


@Singleton
class Bus(object):

    def __init__(self, kwargs):
        """
        Constructor of Bus, this method is not callable, it will raise when
        :code:`Bus()` is invoked, instead to acquire a instance call :code:`Bus.instance()`
        """
        # initialize subscriptions
        self.subscriptions = list()
        self.executor = ThreadPool()

        # user configuration
        self.metrics_enabled = kwargs.pop('with_metrics', False)
        self._may_initialize_metrics()


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
                handler = s[1]
                self.executor.apply(func=handler, args=([payload]))
                self._count_notifications()


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
                        'handler already registered to event: {}'.format(event))

        subscription = (event, handler)
        self.subscriptions.append(subscription)
        self._count_subscriptions()

        return self


    def unsubscribe(self, event):
        """
        Un-subscribe from the event, unregistered the handler of it and
        allowing for resubscribing.
        :param event: the name of the event to un-subscribe
        """
        if not isinstance(event, str):
            raise ValueError('event must be a string')

        for s in self.subscriptions:
            if event in s:
                self.subscriptions.remove(s)
                self._neg_count_subscriptions()

        return self


    def _may_initialize_metrics(self):
        if self.metrics_enabled:
            self.counter = dict(notifications=0, subscriptions=0)


    def _count_notifications(self):
        if self.metrics_enabled:
            self.counter['notifications'] = self.counter['notifications'] + 1


    def _count_subscriptions(self):
        if self.metrics_enabled:
            self.counter['subscriptions'] = self.counter['subscriptions'] + 1


    def _neg_count_subscriptions(self):
        if self.metrics_enabled:
            self.counter['subscriptions'] = self.counter['subscriptions'] - 1


    def __repr__(self):
        if self.metrics_enabled:
            return 'Bus with: \nNotifications delivered: {0} \nSubscribers: {1} \n'.format(
                    self.counter['notifications'], self.counter['subscriptions'])
        else:
            return 'cyberbus.bus.Bus'


def subscribe(event):
    """
    Register the decorated method as a subscriber for the event
    :param event: event name to subscribe to
    """


    def outer(handler):
        Bus.instance().subscribe(event, handler)


        @wraps(handler)
        def wrapper(*args, **kwargs):
            return handler(*args, *kwargs)


        return wrapper


    return outer
