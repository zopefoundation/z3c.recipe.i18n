##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(
    name="z3c.recipe.i18n",
    version="1.2",
    author="Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Zope3 egg based i18n locales extration recipes",
    long_description=(
        read("README.rst")
        + "\n\n"
        + read("CHANGES.rst")
        + "\n\n"
        + "**********************\n"
        "Detailed Documentation\n"
        "**********************"
        + "\n\n"
        + read("src", "z3c", "recipe", "i18n", "README.rst")
    ),
    license="ZPL 2.1",
    keywords="zope3 z3c i18n locales extraction recipe",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Framework :: Buildout",
    ],
    url="https://github.com/zopefoundation/z3c.recipe.i18n",
    zip_safe=False,
    packages=find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    namespace_packages=["z3c", "z3c.recipe"],
    extras_require=dict(
        test=[
            "zope.component",
            "zope.configuration",
            "zope.event",
            "zope.i18nmessageid",
            "zope.interface",
            "zope.location",
            "zope.proxy",
            "zope.schema",
            "zope.security",
            "zope.tal",
            "zope.testing",
        ]
    ),
    install_requires=[
        "setuptools",
        "zc.buildout >= 2.0.0",
        "zc.recipe.egg",
        "zope.app.locales[extract] >= 4.1",
    ],
    entry_points={"zc.buildout": ["i18n = z3c.recipe.i18n.i18n:I18nSetup"]},
    test_suite="z3c.recipe.i18n",
)
