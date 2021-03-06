################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFcTapeCntlrMap

HPFcTapeCntlrMap maps the cpqFcTapeCntlrTable table to cpqFcTapeCntlr objects

$Id: HPFcTapeCntlrMap.py,v 1.3 2011/01/05 00:16:55 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPExpansionCardMap import HPExpansionCardMap

class HPFcTapeCntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqFcTapeCntlrTable table to model."""

    maptype = "cpqFcTapeCntlr"
    modname = "ZenPacks.community.HPMon.cpqFcTapeCntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqFcTapeCntlrTable',
                    '.1.3.6.1.4.1.232.16.3.1.1.1',
                    {
                        '.2': 'status',
                        '.5': 'wwnn',
                        '.6': 'FWRev',
                        '.8': 'setProductKey',
                        '.9': 'serialNumber',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('cpqFcTapeCntlrTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqFcTapeCntlr%s" % om.snmpindex.replace(
                                                                    '.', '_'))
                om.slot = getattr(om, 'slot', 0)
                if not getattr(om, 'setProductKey', ''):
                    om.setProductKey = 'Unknown FC Tape Controller'
                om.setProductKey = MultiArgs(om.setProductKey,
                                            om.setProductKey.split()[0])
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

