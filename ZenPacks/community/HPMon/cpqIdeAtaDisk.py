################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqIdeAtaDisk

cpqIdeAtaDisk is an abstraction of a HP IDE Hard Disk.

$Id: cpqIdeAtaDisk.py,v 1.2 2011/01/04 23:22:12 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from HPHardDisk import HPHardDisk
from HPComponent import *

class cpqIdeAtaDisk(HPHardDisk):
    """cpqIdeAtaDisk object
    """

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
                2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                3: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
                4: (DOT_RED, SEV_CRITICAL, 'Failed'),
                }

InitializeClass(cpqIdeAtaDisk)
