################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSsChassisMap

HPSsChassisMap maps the cpqSsChassisTable table to cpqSsChassis objects

$Id: HPSsChassisMap.py,v 1.3 2011/01/05 00:26:44 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPExpansionCardMap import HPExpansionCardMap

class HPSsChassisMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqSsChassisTable table to model."""

    maptype = "cpqSsChassis"
    modname = "ZenPacks.community.HPMon.cpqSsChassis"

    snmpGetTableMaps = (
        GetTableMap('cpqSsChassisTable',
                    '.1.3.6.1.4.1.232.8.2.2.1.1',
                    {
                        '.2': 'connectionType',
                        '.3': 'serialNumber',
                        '.4': 'name',
                        '.11': 'status',
                        '.19': 'setProductKey',
                    }
        ),
    )

    models =   {1: 'Unknown Storage System Chassis',
                2: 'Compaq StorageWorks RAID Array 4000/4100',
                3: 'Compaq StorageWorks Modular Smart Array 1000',
                4: 'HP StorageWorks Modular Smart Array 500',
                5: 'Compaq StorageWorks Enterprise/Modular RAID Array',
                6: 'Compaq StorageWorks Enterprise Virtual Array',
                7: 'HP StorageWorks Modular Smart Array 500 G2',
                8: 'HP StorageWorks Modular Smart Array 20',
                9: 'HP StorageWorks Modular Smart Array 1500 CS',
                10: 'HP StorageWorks Modular Smart Array 1510i',
                11: 'HP StorageWorks 2060s Modular Smart Array',
                12: 'HP StorageWorks 2070s Modular Smart Array',
            }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('cpqSsChassisTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id=self.prepId("cpqSsChassis%s"%om.snmpindex.replace('.','_'))
                om.slot = getattr(om, 'slot', 0)
                model = self.models.get(int(getattr(om, 'setProductKey', 1)),
                    '%s (%s)'%(self.models[1], getattr(om, 'setProductKey', 1)))
                om.setProductKey = MultiArgs(model, model.split()[0])
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

