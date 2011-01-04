################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSasHbaMap

HPSasHbaMap maps the cpqSasHbaTable table to cpqSasHba objects

$Id: HPSasHbaMap.py,v 1.3 2011/01/05 00:23:45 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPExpansionCardMap import HPExpansionCardMap

class HPSasHbaMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqSasHbaTable table to model."""

    maptype = "cpqSasHba"
    modname = "ZenPacks.community.HPMon.cpqSasHba"

    snmpGetTableMaps = (
        GetTableMap('cpqSasHbaTable',
                    '.1.3.6.1.4.1.232.5.5.1.1.1',
                    {
                        '.2': 'slot',
                        '.3': 'setProductKey',
                        '.4': 'status',
                        '.7': 'serialNumber',
                        '.8': 'FWRev',
                    }
        ),
    )

    models =   {1: 'other',
                2: 'Unknown SAS HBA',
                3: 'HP 8 Internal Port SAS HBA with RAID',
                4: 'HP 4 Internal Port SAS HBA with RAID',
                5: 'HP SC44Ge Host Bus Adapter',
                6: 'HP SC40Ge HBA',
                7: 'HP SC08Ge Host Bus Adapter',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('cpqSasHbaTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqSasHba%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
                model = self.models.get(int(getattr(om, 'setProductKey', 1)),
                    '%s (%s)'%(self.models[1], getattr(om, 'setProductKey', 1)))
                om.setProductKey = MultiArgs(model, model.split()[0])
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

