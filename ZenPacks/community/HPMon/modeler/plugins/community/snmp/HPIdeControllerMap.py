################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPIdeControllerMap

HPIdeControllerMap maps the cpqIdeControllerTable table to cpqIdeController
objects

$Id: HPIdeControllerMap.py,v 1.3 2011/01/05 00:21:40 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPExpansionCardMap import HPExpansionCardMap

class HPIdeControllerMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqIdeControllerTable table to model."""

    maptype = "cpqIdeController"
    modname = "ZenPacks.community.HPMon.cpqIdeController"

    snmpGetTableMaps = (
        GetTableMap('cpqIdeControllerTable',
                    '.1.3.6.1.4.1.232.14.2.3.1.1',
                    {
                        '.3': 'model',
                        '.4': 'FWRev',
                        '.5': 'slot',
                        '.6': 'status',
                        '.8': 'serialNumber',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('cpqIdeControllerTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqIdeController%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
                if om.slot == -1: om.slot = 0
                if not getattr(om, 'setProductKey', ''):
                    om.setProductKey = 'Unknown IDE Controller'
                om.setProductKey = MultiArgs(om.setProductKey,
                                            om.setProductKey.split()[0])
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

