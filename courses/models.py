# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from departments.models import Department


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    departments = models.ManyToManyField(Department)

    def __str__(self):
        return self.name
