################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPsdFan

HPsdFan is an abstraction of a fan or probe.

$Id: HPsdFan.py,v 1.3 2011/07/07 23:32:49 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.ZenModel.Fan import Fan
from HPComponent import *

class HPsdFan(Fan, HPComponent):
    """Speed Detect Fan object"""

    status = 1

    _properties = Fan._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 )


    @property
    def state(self):
        return self.statusString()

    def rpmString(self):
        """
        Return a string representation of the RPM
        """
        rpm = self.rpm()
        if rpm == 2: return "Normal"
        if rpm == 3: return "High"
        return "Unknown"

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPsdFan)
