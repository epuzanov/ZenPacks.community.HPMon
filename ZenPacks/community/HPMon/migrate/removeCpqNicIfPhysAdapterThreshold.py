################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class removeCpqNicIfPhysAdapterThreshold( ZenPackMigration ):
    """
    remove cpqNicIfPhysAdapter Threshold from RRDTemplates
    """
    version = Version(2, 2, 75)

    def migrate(self, pack):

        for template in pack.dmd.Devices.Server.getAllRRDTemplates():
            if template.id != 'cpqNicIfPhysAdapter': continue
            for threshold in template.thresholds():
                if threshold.id != 'status': continue
                template.thresholds.removeRelation(threshold)

removeCpqNicIfPhysAdapterThreshold()
