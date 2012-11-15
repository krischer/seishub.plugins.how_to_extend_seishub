#!/usr/bin/env python
# -*- coding: utf-8 -*-
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerSchema, \
    registerStylesheet
from seishub.core.packages.interfaces import IPackage, IResourceType

import inspect
import os


def get_path(*args):
    """
    Helper function to get the absolute path of files in this directory or a
    subdirectory thereof.

    This function takes care of cross-platform and other issues and should just
    work.

    Example:
        Suppose you want to get the path of the file "schema.xsd" in the "xsd"
        directory:
            path = get_path("xsd", "schema.xsd")

    """
    this_dir = os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe())))
    return os.path.join(this_dir, *args)


class SimpleEventsPackage(Component):
    """
    Package to store a simple event format.
    """
    implements(IPackage)
    package_id = "simpleEvents"
    version = "0.0.0."


class EventResourceType(Component):
    """
    Simple event resource type.
    """
    implements(IResourceType)
    package_id = "simpleEvents"
    version = "0.0.0."
    resourcetype_id = "event"

    registerSchema(get_path("xsd", "simple_events.xsd"), "XMLSchema")
    registerStylesheet(get_path("xslt", "simple_events.xslt"), "kml")

    registerIndex("latitude", "/seismic_event/latitude", "float")
    registerIndex("longitude", "/seismic_event/longitude", "float")
    registerIndex("time", "/seismic_event/time", "datetime")
