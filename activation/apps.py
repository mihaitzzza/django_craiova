# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ActivationConfig(AppConfig):
    name = 'activation'

    def ready(self):
        import activation.signals
