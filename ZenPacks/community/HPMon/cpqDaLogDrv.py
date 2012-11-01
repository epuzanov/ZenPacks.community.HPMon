################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqDaLogDrv

cpqDaLogDrv is an abstraction of a HP DA Logical Disk.

$Id: cpqDaLogDrv.py,v 1.4 2012/11/01 17:38:00 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

import inspect
from HPLogicalDisk import HPLogicalDisk
from HPComponent import *

class cpqDaLogDrv(HPLogicalDisk):
    """cpqDaLogDrv object
    """

    __ifindex = "1"

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
                2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                3: (DOT_RED, SEV_CRITICAL, 'Failed'),
                4: (DOT_YELLOW, SEV_WARNING, 'Unconfigured'),
                5: (DOT_ORANGE, SEV_ERROR, 'Recovering'),
                6: (DOT_YELLOW, SEV_WARNING, 'Ready Rebuild'),
                7: (DOT_YELLOW, SEV_WARNING, 'Rebuilding'),
                8: (DOT_ORANGE, SEV_ERROR, 'Wrong Drive'),
                9: (DOT_ORANGE, SEV_ERROR, 'Bad Connect'),
                10:(DOT_RED, SEV_CRITICAL, 'Overheating'),
                11:(DOT_RED, SEV_CRITICAL, 'Shutdown'),
                12:(DOT_YELLOW, SEV_WARNING, 'Expanding'),
                13:(DOT_YELLOW, SEV_WARNING, 'Not Available'),
                14:(DOT_YELLOW, SEV_WARNING, 'Queued For Expansion'),
                15:(DOT_ORANGE, SEV_ERROR, 'Multi-path Access Degraded'),
                }

    def getRRDTemplates(self):
        templates = []
        tnames = ['cpqDaLogDrv', 'cpqDaLogDrvPerf']
        for tname in tnames:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

    def _getSnmpIndex(self):
        frame = inspect.currentframe(2)
        ifindex = ''

        try:
            if frame.f_locals.get('oid') == '1.3.6.1.4.1.232.3.2.8.1.1.5':
                ifindex = '.' + self.__ifindex
        finally:
            del frame

        return self.snmpindex + ifindex

    def _setSnmpIndex(self, value):
        self.__ifindex = value

    ifindex = property(fget=lambda self: self._getSnmpIndex(),
                        fset=lambda self, v: self._setSnmpIndex(v)
                        )

InitializeClass(cpqDaLogDrv)
