################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPComponent

HPComponent is an abstraction .

$Id: HPComponent.py,v 1.1 2011/01/04 23:10:11 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.deviceAdvDetail.HWStatus import *
from Products.ZenModel.ZenossSecurity import *

class HPComponent(HWStatus):

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

