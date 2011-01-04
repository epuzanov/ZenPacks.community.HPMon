################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPTemperatureSensor

HPTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: HPTemperatureSensor.py,v 1.2 2011/01/04 23:14:17 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.TemperatureSensor import TemperatureSensor
from HPComponent import *

class HPTemperatureSensor(TemperatureSensor, HPComponent):
    """TemperatureSensor object"""

    threshold = 0
    status = 1

    _properties = TemperatureSensor._properties + (
                {'id':'status', 'type':'int', 'mode':'w'},
                {'id':'threshold', 'type':'int', 'mode':'w'},
                )

    def state(self):
         return self.statusString()

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPTemperatureSensor)
