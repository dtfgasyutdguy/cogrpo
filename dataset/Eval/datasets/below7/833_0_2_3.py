# -*- coding: utf-8 -*-


from distutils.command.bdist import bdist

if 'egg' not in bdist.format_commands:
    try:
        bdist.format_commands['egg'] = ('bdist_egg', "Python .egg file")
# import sys
    except TypeError:
        # For backward compatibility with older distutils (stdlib)
        bdist.format_command['egg'] = ('bdist_egg', "Python .egg file")
        bdist.format_commands.append('egg')

del bdist, sys
