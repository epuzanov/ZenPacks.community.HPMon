################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPIdeAtaDiskMap

HPIdeAtaDiskMap maps the cpqIdeAtaDiskTable to disks objects

$Id: HPIdeAtaDiskMap.py,v 1.4 2011/01/05 19:29:41 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPHardDiskMap import HPHardDiskMap

class HPIdeAtaDiskMap(HPHardDiskMap):
    """Map HP/Compaq insight manager ATA Hard Disk tables to model."""

    maptype = "HPIdeAtaDiskMap"
    modname = "ZenPacks.community.HPMon.cpqIdeAtaDisk"

    snmpGetTableMaps = (
        GetTableMap('cpqIdeAtaDiskTable',
                    '.1.3.6.1.4.1.232.14.2.4.1.1',
                    {
                        '.3': 'description',
                        '.4': 'FWRev',
                        '.5': 'serialNumber',
                        '.6': 'status',
                        '.8': 'size',
                        '.12': 'bay',
                        '.16': 'diskType',
                    }
        ),
    )

    diskTypes = {1: 'other',
                2: 'ATA',
                3: 'SATA',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPHardDiskMap.oms:
            HPHardDiskMap.oms[device.id] = []
        for oid, disk in tabledata.get('cpqIdeAtaDiskTable', {}).iteritems():
            try:
                om = self.objectMap(disk)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("HardDisk%s"%om.snmpindex).replace('.','_')
                if not getattr(om,'description',''):om.description='Unknown Disk'
                om.setProductKey = MultiArgs(om.description,
                                            om.description.split()[0])
                om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1),
                                    '%s (%d)' %(self.diskTypes[1], om.diskType))
                om.rpm = self.rpms.get(getattr(om,'rpm',1), getattr(om,'rpm',1))
                om.size = getattr(om, 'size', 0) * 1048576
                if hasattr(om, 'bay'):
                    if int(om.bay) > 3:
                        om.bay = int(om.bay) - 4
                    if int(om.bay) > 16:
                        om.bay = int(om.bay) - 16
            except AttributeError:
                continue
            HPHardDiskMap.oms[device.id].append(om)
        return

