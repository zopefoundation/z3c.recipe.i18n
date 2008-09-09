#!/usr/bin/env python2.4
##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
"""Merge a POT file with all languages

This utility requires the GNU gettext package to be installed. The command
'msgmerge' will be executed for each language.

Usage: i18mergeall.py [options]
Options:

    -h / --help
        Print this message and exit.

    -l / --locales-dir
        Specify the 'locales' directory for which to generate the statistics.

$Id:$
"""
import sys
import os
import getopt

def usage(code, msg=''):
    """Display help."""
    print >> sys.stderr, '\n'.join(__doc__.split('\n')[:-2])
    if msg:
        print >> sys.stderr, '** Error: ' + str(msg) + ' **'
    sys.exit(code)


def merge(path):
    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')

        # Make sure we got a language directory
        if not os.path.isdir(lc_messages_path):
            continue

        msgs = []
        for domain_file in os.listdir(lc_messages_path):
            if domain_file.endswith('.po'):
                domain_path = os.path.join(lc_messages_path, domain_file)
                pot_path = os.path.join(path, domain_file+'t')
                domain = domain_file.split('.')[0]
                print 'Merging language "%s", domain "%s"' %(language, domain)
                os.system('msgmerge -U %s %s' %(domain_path, pot_path))


def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'l:h',
            ['help', 'locals-dir='])
    except getopt.error, msg:
        usage(1, msg)

    path = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-l', '--locales-dir'):
            cwd = os.getcwd()
            # This is for symlinks. Thanks to Fred for this trick.
            if os.environ.has_key('PWD'):
                cwd = os.environ['PWD']
            path = os.path.normpath(os.path.join(cwd, arg))

    if path is None:
        usage(1, 'You must specify the path to the locales directory.')
    merge(path)

if __name__ == '__main__':
    main()

