#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from setuptools import find_packages, setup


setup(
    # The name of the plugins. Need to be seishub.plugins.PLUGIN_NAME.
    name="seishub.plugins.template",
    # The version number of the plugin.
    version="0.0.0",
    # The description of the plugin.
    description="Template for SeisHub plug-ins.",
    # Your name.
    author="Author Name",
    # Your email.
    author_email="email@yourmail.com",
    # Don't forget the licence! LGPL is a solid choice.
    license="GNU Lesser General Public License, Version 3 (LGPLv3)",
    packages=find_packages(),
    namespace_packages=["seishub", "seishub.plugins"],
    include_package_data=True,
    zip_safe=False,
    # The requirements for the plugin. Add any additional modules here.
    install_requires=[
        "setuptools",
        "seishub.core",
    ],
    # You need to define entry points so that SeisHub can find the plugin.
    # Usually something like this is fine.
    entry_points={"seishub.plugins": [
     "seishub.plugins.template = seishub.plugins.template",
     ]
    },
)
