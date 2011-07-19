################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPSm2CntlrMap

HPSm2CntlrMap maps the cpqSm2CntlrTable table to cpqSm2Cntlr objects

$Id: HPSm2CntlrMap.py,v 1.3 2011/07/19 20:50:10 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
from HPExpansionCardMap import HPExpansionCardMap

class HPSm2CntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqSm2CntlrTable table to model."""

    maptype = "cpqSm2Cntlr"
    modname = "ZenPacks.community.HPMon.cpqSm2Cntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqSm2CntlrTable',
                    '.1.3.6.1.4.1.232.9.2.2',
                    {
                        '.2': 'romRev',
                        '.12': 'status',
                        '.15': 'serialNumber',
                        '.18': 'systemId',
                        '.21': 'setProductKey',
                        '.28': 'hwVer',
                        '.31': 'advLicense',
                    }
        ),
        GetTableMap('cpqSm2NicConfigTable',
                    '.1.3.6.1.4.1.232.9.2.5.1.1',
                    {
                        '.1': 'snmpindex',
                        '.4': 'macaddress',
                        '.5': 'ipaddress',
                        '.6': 'subnetmask',
                        '.14': 'dnsName',
                    }
        ),
    )

    models =   {1: 'Unknown Integrated Lights-Out Board',
                2: 'Compaq EISA Remote Insight Board',
                3: 'Compaq PCI Remote Insight Board',
                4: 'Compaq PCI Remote Insight Lights-Out Edition Board',
                5: 'Compaq Integrated Remote Insight Lights-Out Edition Board',
                6: 'Compaq Integrated Remote Insight Lights-Out Edition Ver.II Board',
                7: 'HP Integrated Lights-Out 2 Edition Board',
                8: 'HP Lights-Out 100 Edition Board',
                9: 'HP Integrated Lights-Out 3 Edition Board',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in tabledata.get('cpqSm2CntlrTable', {}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqSm2Cntlr%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
                model = self.models.get(int(getattr(om, 'setProductKey', 1)),
                    '%s (%s)'%(self.models[1], getattr(om, 'setProductKey', 1)))
                om.setProductKey = MultiArgs(model, model.split()[0])
                for nic in tabledata.get('cpqSm2NicConfigTable', {}).values():
                    om.macaddress = self.asmac(getattr(nic, 'macaddress', ''))
                    om.ipaddress = getattr(nic, 'ipaddress', '')
                    om.subnetmask = getattr(nic, 'subnetmask', '')
                    om.dnsName = getattr(nic, 'dnsName', '')
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

