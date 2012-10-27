========================
ZenPacks.community.HPMon
========================

About
=====

This ZenPack provides additional monitoring options for HP Servers with HP
System Insight Manager Agent installed.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2, Zenoss 3.2 and Zenoss 4.2. You can download the free Core
version of Zenoss from http://community.zenoss.org/community/download.

ZenPacks
--------

You must first install:

- `Advanced Device Details ZenPack <http://community.zenoss.org/docs/DOC-3452>`_


Monitored Systems
-----------------

On monitored system, HP System Insight Manager Agents must be installed and
properly configured.


Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `HP ProLiant Monitor <http://community.zenoss.org/docs/DOC-3394>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.HPMon-2.3.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the HPMon
ZenPack you should clone the git `repository <https://github.com/epuzanov/ZenPacks.community.HPMon>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.HPMon.git
        zenpack --link --install ZenPacks.community.HPMon
        zenoss restart


Usage
=====

Go to the specific device (yes, it needs to already be added).

#. From the > Menu select More -> Collector Plugins
#. Remove the zenoss.snmp.Cpu
#. Click "Add Fields"
#. Drag and drop all of the "community.snmp.HP*" entries in the right list over
   into the left list. Note that community.snmp.HPLogicalDiskMap,
   community.snmp.HPHardDiskMap and community.snmp.HPExpansionCardMap plugins
   must be at the END of lists.
#. CLICK SAVE (don't forget this step)
#. From the > Menu select Manage -> Model Device
#. Once it is completed modeling check out the hardware tab for the device,
   you should see CPUs, Harddrives, Fans, etc. If you don't you may have
   problems with snmp, so check those settings the usual way.

Installing the ZenPack will add the following items to your Zenoss system.


zProperties
-----------

- **zHPExpansionCardMapIgnorePci** - ignore PCI cards other than RAID and iLO
  controllers


Modeler Plugins
---------------

- **community.snmp.HPCPUMap** - CPU modeler plugin
- **community.snmp.HPDaCntlrMap** - modeler plugin for HP Smart Array
  controllers
- **community.snmp.HPDaLogDrvMap** - modeler plugin for Logical Disks on
  HP Smart Array controllers
- **community.snmp.HPDaPhyDrvMap** - modeler plugin for Physical Disks on
  HP Smart Array controllers
- **community.snmp.HPDeviceMap** - device modeler plugin, tried
  to identify Model, Vendor and Serial Number
- **community.snmp.HPExpansionCardMap** - PCI cards modeler plugin, tried to
  identify all PCI cards, RAID and iLO controllers, put it to the end of
  ***Collector Plugins*** list
- **community.snmp.HPFanMap** - Fan modeler plugin
- **community.snmp.HPFcTapeCntlrMap** - modeler plugin for FC Tape controllers
- **community.snmp.HPFcaCntlrMap** - modeler plugin for HP StorageWorks Modular
  Smart Array controllers
- **community.snmp.HPFcaLogDrvMap** - modeler plugin for Logical Disks on
  HP StorageWorks Modular Smart Array controllers
- **community.snmp.HPFcaPhyDrvMap** - modeler plugin for Physical Disks on
  HP StorageWorks Modular Smart Array controllers
- **community.snmp.HPHardDiskMap** - Hard Disks modeler plugin returned to
  zenmodeler information collected by other Physical Disk modeler plugins, so
  put it in **Collector Plugins** list after all Physical Disk modeler plugins.
- **community.snmp.HPIdeAtaDiskMap** - modeler plugin for IDE/ATA Physical Disks
- **community.snmp.HPIdeControllerMap** - modeler plugin for IDE/ATA controllers
- **community.snmp.HPIdeLogicalDriveMap** - modeler plugin for Logical Disks on
  IDE/ATA controllers
- **community.snmp.HPLogicalDiskMap** - Logical Disks modeler plugin returned to
  zenmodeler information collected by other Logical Disk modeler plugins, so
  put it in **Collector Plugins** list after all Logical Disk modeler plugins.
- **community.snmp.HPMemoryModuleMap** - Physical Memory modeler plugin, tried
  to identify memory modules
- **community.snmp.HPNicMap** - Network Cards modeler plugin
- **community.snmp.HPPowerSupplyMap** - Power Supply modeler plugin
- **community.snmp.HPSasHbaMap** - modeler plugin for SAS controllers
- **community.snmp.HPSasLogDrvMap** - modeler plugin for Logical Disks on SAS
  controllers
- **community.snmp.HPSasPhyDrvMap** - modeler plugin for Physical Disks on SAS
  controllers
- **community.snmp.HPScsiCntlrMap** - modeler plugin for SCSI controllers
- **community.snmp.HPScsiLogDrvMap** - modeler plugin for Logical Disks on SCSI
  controllers
- **community.snmp.HPScsiPhyDrvMap** - modeler plugin for Physical Disks on SCSI
  controllers
- **community.snmp.HPSm2CntlrMap** - modeler plugin for iLO Management
  controllers
- **community.snmp.HPSsChassisMap** - External Chassis modeler plugin
- **community.snmp.HPTemperatureSensorMap** - Temperature Sensor modeler plugin

Monitoring Templates
--------------------

- **Devices/Server/rrdTemplates/HPFan**
- **Devices/Server/rrdTemplates/HPPowerSupply**
- **Devices/Server/rrdTemplates/HPTemperatureSensor**
- **Devices/Server/rrdTemplates/cpqDaCntlr**
- **Devices/Server/rrdTemplates/cpqDaCntlrPerf**
- **Devices/Server/rrdTemplates/cpqDaLogDrv**
- **Devices/Server/rrdTemplates/cpqDaLogDrvPerf**
- **Devices/Server/rrdTemplates/cpqDaPhyDrv**
- **Devices/Server/rrdTemplates/cpqFcaCntlr**
- **Devices/Server/rrdTemplates/cpqFcaHostCntlr**
- **Devices/Server/rrdTemplates/cpqFcaLogDrv**
- **Devices/Server/rrdTemplates/cpqFcaPhyDrv**
- **Devices/Server/rrdTemplates/cpqHeResMem2Module**
- **Devices/Server/rrdTemplates/cpqIdeAtaDisk**
- **Devices/Server/rrdTemplates/cpqIdeController**
- **Devices/Server/rrdTemplates/cpqIdeLogicalDrive**
- **Devices/Server/rrdTemplates/cpqNicIfPhysAdapter**
- **Devices/Server/rrdTemplates/cpqSasHba**
- **Devices/Server/rrdTemplates/cpqSasLogDrv**
- **Devices/Server/rrdTemplates/cpqSasPhyDrv**
- **Devices/Server/rrdTemplates/cpqScsiCntlr**
- **Devices/Server/rrdTemplates/cpqScsiLogDrv**
- **Devices/Server/rrdTemplates/cpqScsiPhyDrv**
- **Devices/Server/rrdTemplates/cpqSiMemModule**
- **Devices/Server/rrdTemplates/cpqSm2Cntlr**
- **Devices/Server/rrdTemplates/cpqSsChassis**

Reports
-------

- **Reports/Device Reports/HP ProLiant Reports/Hard Disks**
- **Reports/Device Reports/HP ProLiant Reports/Storage Controllers**
- **Reports/Device Reports/HP ProLiant Reports/iLO Boards**

MIBs
----

- **CPQFCA-MIB**
- **CPQHLTH-MIB**
- **CPQIDA-MIB**
- **CPQIDE-MIB**
- **CPQNIC-MIB**
- **CPQSCSI-MIB**
- **CPQSM2-MIB**
