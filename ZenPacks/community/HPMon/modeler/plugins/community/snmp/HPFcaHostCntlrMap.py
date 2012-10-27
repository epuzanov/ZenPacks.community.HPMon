################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFcaHostCntlrMap

HPFcaHostCntlrMap maps the cpqFcaHostCntlrTable table to cpqFcaHostCntlr objects

$Id: HPFcaHostCntlrMap.py,v 1.4 2012/10/27 16:41:18 egor Exp $"""

__version__ = '$Revision: 1.4 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPExpansionCardMap import HPExpansionCardMap

class HPFcaHostCntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqFcaHostCntlrTable table to model."""

    maptype = "cpqFcaHostCntlr"
    modname = "ZenPacks.community.HPMon.cpqFcaHostCntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqFcaHostCntlrTable',
                    '.1.3.6.1.4.1.232.16.2.7.1.1',
                    {
                        '.2': 'slot',
                        '.3': 'setProductKey',
                        '.4': 'status',
                        '.6': 'wwnn',
                        '.10': 'serialNumber',
                        '.12': 'wwpn',
                        '.13': 'FWRev',
                        '.14': 'ROMRev',
                    }
        ),
    )

    models =   {1: 'Unknown Fibre Channel HBA',
                2: 'Compaq StorageWorks Fibre Channel Host Bus Adapter/P',
                3: 'Compaq StorageWorks Fibre Channel Host Bus Adapter/E',
                4: 'Compaq StorageWorks 64-Bit/66-Mhz Fibre Host Bus Adapter',
                5: 'Compaq Smart Array, SAN Access Module',
                6: 'HP FCA-2101',
                7: 'Compaq StorageWorks 64bit/33Mhz PCI to Fibre Channel HBA',
                8: 'HP FCA-221x',
                9: 'HP Dual Port Fibre Channel Mezzanine Card (2 Gb) for BL20Gp2 G2',
                10: 'HP PCI-X 2Gb FCA2404 Fibre Channel HBA',
                11: 'HP PCI-X 2Gb FCA2214 Fibre Channel HBA',
                12: 'HP PCI-X 2Gb A7298A Fibre Channel HBA',
                13: 'HP PCI-X 2Gb FCA2214DC Fibre Channel HBA',
                14: 'HP PCI-X Dual Channel 2GB A6826A Fibre Channel HBA',
                15: 'HP Fibre Channel Mezzaine Card G3, BL3x p Series',
                16: 'HP Fibre Channel Mezzaine Card G4, BL2x p Series',
                17: 'HP PCI-X 2GB AB466A/AB467A Fibre Channel HBA',
                18: 'HP Fibre Channel HBA',
                19: 'HP FC1143 4Gb PCI-X 2.0 HBA',
                20: 'HP FC1243 4Gb PCI-X 2.0 DC HBA',
                21: 'HP FC2143 4Gb PCI-X 2.0 HBA',
                22: 'HP FC2243 4Gb PCI-X 2.0 DC HBA',
                23: 'HP StorageWorks 1050 HBA',
                24: 'Emulex LPe1105-HP 4Gb FC HBA for HP c-Class Blade System',
                25: 'Qlogic QMH2462 4Gb FC HBA for HP c-Class Blade System',
                26: 'HP FC1142SR 4Gb PCI-e HBA',
                27: 'HP FC1242SR 4Gb PCI-e DC HBA',
                28: 'HP FC2142SR 4Gb PCI-e HBA',
                29: 'HP FC2242SR 4Gb PCI-e DC HBA',
                30: 'Emulex based BL20p Fibre Channel Mezz HBA',
                31: 'HP StorageWorks 81Q 8Gb PCI-e FC HBA',
                32: 'HP StorageWorks 82Q 8Gb PCI-e Dual Port FC HBA',
                33: 'QLogic QMH2562 8Gb FC HBA for HP BladeSystem c-Class',
                34: 'HP StorageWorks 81E 8Gb PCI-e FC HBA',
                35: 'HP StorageWorks 82E 8Gb PCI-e Dual Port FC HBA',
                36: 'Emulex LPe 1205-HP 8Gb FC HBA for HP BladeSystem c-Class',
                37: 'HP SN1000E 16Gb Single Port FC HBA',
                38: 'HP SN1000E 16Gb Dual Port FC HBA',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('cpqFcaHostCntlrTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqFcaHostCntlr%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
                model = self.models.get(int(getattr(om, 'setProductKey', 1)),
                    '%s (%s)'%(self.models[1], getattr(om, 'setProductKey', 1)))
                om.setProductKey = MultiArgs(model, model.split()[0])
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

