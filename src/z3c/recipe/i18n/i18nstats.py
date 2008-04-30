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
"""Translation Statistics Utility

Utility to determine the status of the translations.

Usage: i18nstats.py [options]
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

SEARCHING = 0
COMMENT = 1
MSGID = 2
MSGSTR = 3
MSGDONE = 4

def usage(code, msg=''):
    """Display help."""
    print >> sys.stderr, '\n'.join(__doc__.split('\n')[:-2])
    if msg:
        print >> sys.stderr, '** Error: ' + str(msg) + ' **'
    sys.exit(code)


def getMessageDictionary(file):
    """Simple state machine."""

    msgs = []
    comment = []
    msgid = []
    msgstr = []
    fuzzy = False
    line_counter = 0
    status = SEARCHING

    for line in file.readlines():
        line = line.strip('\n')
        line_counter += 1

        # Handle Events
        if line.startswith('#'):
            status = COMMENT

        elif line.startswith('msgid'):
            line = line[6:] 
            line_number = line_counter
            status = MSGID

        elif line.startswith('msgstr'):
            line = line[7:] 
            status = MSGSTR

        elif line == '':
            status = MSGDONE

        # Actions based on status
        if status == MSGID:
            msgid.append(line.strip('"'))

        elif status == MSGSTR:
            msgstr.append(line.strip('"'))

        elif status == COMMENT:
            if line.startswith('#, fuzzy'):
                fuzzy = True
            comment.append(line[1:].strip())

        elif status == MSGDONE:
            status = SEARCHING
            # Avoid getting the meta-data message string
            if ''.join(msgid):
                msgs.append( (''.join(msgid), ''.join(msgstr),
                              line_number, '\n'.join(comment), fuzzy) )
            comment = []
            msgid = []
            msgstr = []
            fuzzy = False

    return msgs


def stats(path):
    print 'Language    Total    Done    Not Done    Fuzzy      Done %'
    print '=========================================================='
    languages = os.listdir(path)
    languages.sort()
    for language in languages:
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')

        # Make sure we got a language directory
        if not os.path.isdir(lc_messages_path):
            continue

        msgs = []
        for domain_file in os.listdir(lc_messages_path):
            if domain_file.endswith('.po'):
                domain_path = os.path.join(lc_messages_path, domain_file)
                file = open(domain_path, mode='r')
                msgs += getMessageDictionary(file)

        # We are dealing with the default language, which always has just one
        # message string for the meta data (which is not recorded). 
        if len(msgs) == 0:
            continue

        total = len(msgs)
        not_done = len([msg for msg in msgs if msg[1] == ''])
        fuzzy = len([msg for msg in msgs if msg[4] is True])
        done = total - not_done - fuzzy
        percent_done = 100.0 * done/total

        line = language + ' '*(8-len(language))
        line += ' '*(9-len(str(total))) + str(total)
        line += ' '*(8-len(str(done))) + str(done)
        line += ' '*(12-len(str(not_done))) + str(not_done)
        line += ' '*(9-len(str(fuzzy))) + str(fuzzy)
        pd_str = '%0.2f %%' %percent_done
        line += ' '*(12-len(pd_str)) + pd_str
        print line
    

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
    stats(path)

if __name__ == '__main__':
    main()

