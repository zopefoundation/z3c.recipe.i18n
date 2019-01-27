#!/usr/bin/env python
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
from __future__ import print_function

"""Compile PO files to Mo files for all languages in a given locales dir

This utility requires the GNU gettext package to be installed. The command
'msgfmt' will be executed for each language.

Usage: i18ncompile.py [options]
Options:

    -h / --help
        Print this message and exit.

    -l / --locales-dir
        Specify the 'locales' directory for which to generate the statistics.

$Id:$
"""
import getopt
import os
import os.path
import subprocess
import sys


def usage(code, msg=""):
    """Display help."""
    print("\n".join(__doc__.split("\n")[:-2]), file=sys.stderr)
    if msg:
        print("** Error: " + str(msg) + " **", file=sys.stderr)
    sys.exit(code)


def msgfmt(path):
    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, "LC_MESSAGES")

        # Make sure we got a language directory
        if not os.path.isdir(lc_messages_path):
            continue

        for poFile in os.listdir(lc_messages_path):
            if poFile.endswith(".po"):
                domain = poFile.rsplit(".", 1)[0]
                base = os.path.join(lc_messages_path, domain)
                poPath = str(base + ".po")
                moPath = str(base + ".mo")
                print('Compile language "%s" for "%s"' % (language, domain))
                subprocess.call(["msgfmt", "-o", moPath, poPath])


def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(argv[1:], "l:h", ["help", "locals-dir="])
    except getopt.error as msg:
        usage(1, msg)

    path = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(0)
        elif opt in ("-l", "--locales-dir"):
            cwd = os.getcwd()
            # This is for symlinks. Thanks to Fred for this trick.
            if "PWD" in os.environ:
                cwd = os.environ["PWD"]
            path = os.path.normpath(os.path.join(cwd, arg))

    if path is None:
        usage(1, "You must specify the path to the locales directory.")
    msgfmt(path)


if __name__ == "__main__":
    main()
