################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPTemperatureSensorMap

HPTemperatureSensorMap maps the cpqHeTemperatureTable table to temperaturesensors
objects

$Id: HPTemperatureSensorMap.py,v 1.2 2011/01/02 21:00:14 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPTemperatureSensorMap(SnmpPlugin):
    """Map HP/Compaq insight manager Temperature Sensors table to model."""

    maptype = "HPTemperatureSensorMap"
    modname = "ZenPacks.community.HPMon.HPTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cpqHeTempTable',
                    '.1.3.6.1.4.1.232.6.2.6.8.1',
                    {
                        '.3': '_location',
                        '.5': 'threshold',
                        '.6': 'status',
                    }
        ),
    )

    localemap = {1: "other", 
                2: "unknown",
                3: "system",
                4: "systemBoard",
                5: "ioBoard",
                6: "cpu",
                7: "memory",
                8: "storage",
                9: "removableMedia",
                10: "powerSupply",
                11: "ambient",
                12: "chassis",
                13: "bridgeCard",
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        localecounter = {}
        for oid, tsensor in tabledata.get("cpqHeTempTable", {}).iteritems():
            try:
                om = self.objectMap(tsensor)
                if om.status == 1: continue
                om.snmpindex = oid.strip('.')
                if om._location in localecounter:
                    localecounter[om._location] = localecounter[om._location]+1
                else:
                    localecounter[om._location] = 1
                om.id = self.prepId("%s%d" % (self.localemap.get(
                                                 getattr(om, '_location', 1),
                                                 self.localemap[1]),
                                            localecounter[om._location]))
            except AttributeError:
                continue
            rm.append(om)
        return rm
