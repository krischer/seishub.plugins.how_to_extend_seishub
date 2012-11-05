# -*- coding: utf-8 -*-
"""
Template package for SeisHub.
"""
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


class TemplateComponent(Component):
    """
    Template package for SeisHub.
    """
    implements(IPackage)
    package_id = "template_tutorial"
    version = "0.0.0"


class SomeTemplateResourceType(Component):
    """
    This demonstrates how to add a new resource type to SeisHub.
    """
    implements(IResourceType)

    # Specify the package name of the resource. The package also has to be
    # defined - in this case this is defined in the TemplateComponent class.
    package_id = "template_tutorial"
    # The resource type name. Resources of this type will now be available
    # under SEISHUB_URL/xml/template/some_resource.
    resourcetype_id = "some_resource"

    # If a XML schema is registered, every uploaded resource of this type will
    # be validate against it. If the validation fails, the uploaded file will
    # be rejected.
    # registerSchema(get_path("xsd", "some_schema.xsd"), "XMLSchema")

    # Resource can be transformed upon downloading with any registered XML
    # stylesheet.
    # registerStylesheet(get_path("xslt", "some_stylesheet.xsl"),
    #   stylesheet_name")

    # To be able to quickly query certain value of the resource, they need to
    # be indexed. This means an index has to be registered.
    # The first argument is the name of the index, the second one an xpath
    # expression applied to the XML resource to find the value of the index and
    # the third is the type of the value.
    # Possible types are:
    #     "text", "numeric", "float", "datetime", "boolean", "date", "integer",
    #     "timestamp"
    # Please take care to choose the correct type!
    #registerIndex("some_index", "/xpath/expression" , "text")
