IcepapCMS 3.2.X
-------------------------------------------------------------------------
Added:
* Add auto solved conflict to migrate to 3.35 from: 2.0 to 3.14, 3.15, 3.17,
  3.182, 3.185, 3.187, 3.192, 3.193, 3.23, 3.25, 3.29, 3.31, 3.33
* Generic method to compare and solve conflicts.

Fixed:
* The icepap needs time to save the firmware and the automatic firmware update 
  does not wait it and uses the previous saved firmware instead of the new one. 

Removed:

IcepapCMS 3.1.3
-------------------------------------------------------------------------
Added:
* Update to use icepap 3.6.0 to read faster the versions on the loading time.
* Add debug command option to have direct access to the communication 
  debugging.
* Add how to configure the all network flag and the ldap on the README file

Fixed:
* Avoid GUI crashing for icepap library exceptions.
* Change error message to avoid confusion in diagnosis.  
* Fix wrong driver name size on DB scripts creation.
* Fix some error on the dialog preference:
    * Wrong reading of the sqlite folder from icepapcms.conf file.
    * Update templated edit dialog when change the snapshot folder.
    * Save the snapshots folder on the icepapcms.conf file.
* Fix absolute encoder offset limits to 32 bits
* Fix ldap not user allowed matching to allow regex.

Removed:

 
IcepapCMS 3.0.1
-------------------------------------------------------------------------
Added:
* Reorganize reorganize repository some modules and files change name to
 avoid problems on the installation.
* Migrate to Python >= 3.5
* Migrate to Qt5 >= 5.12
* Migrate to storm >= 0.23, add custom support to MySQL Databases
* Migrate to icepap >= 3.3
* Migrate to ldap3, pure python library
* Add automatic firmware upgrade based on the current icepap version
* Allow to generate snapshot of the system. All the configuration parameters
 and some important operation register are saved on a YAML file
* Add MCPUx on expert mode programming 
* Add LDAP configuration on the configuration file
* Add All-Networks flag on the configuration file in addition to the
 launcher script.


Fixed:
* Sizes of some widget to show all the information
* Adapt programing dialog to icepap library API 3.4
* Adapt update firmware driver dialog to icepap library API 3.4
* Rename files with spaces


Removed:
* Duplicated and/or unused files 
* Remove to use ICEPAP_ALL_NETWORKS environment variable, it is included on
 the configuration file
 
IcepapCMS 2.3.X 2018/11/29
-------------------------------------------------------------------------
Added:
* Update to use pyIcePAP API 2.0
* Add protection on add new system

Fixed:
* Fix error on the version generation.
* Fix bug on power button.
* Fix exception raising on activate/deactivate axis
* Fix ipapconsole launcher

IcepapCMS 2.x.x 2018/xx/xx
-------------------------------------------------------------------------
* Fixed issues with non-ascii characters in Driver's NAME

IcepapCMS 2.02 2016/04/04
-------------------------------------------------------------------------
* 

IcepapCMS 2.01 2016/04/04
-------------------------------------------------------------------------
* ISSUE 078 Fixed bug when removing location, now DB is properly cleared

IcepapCMS 2.0 2016/02/11
-------------------------------------------------------------------------
* Support for driver conflicts when firmware >= 3.14
* ISSUE 076 [PROTOTYPE] - waiting input from MAX-IV and ESRF

IcepapCMS 1.32 2015/05/29 ;-D
-------------------------------------------------------------------------
* ISSUE <email> allow negative values in home position
* ISSUE <email> Unknown-tab parameters available in Database and Load/Export files

IcepapCMS 1.31 2015/03/02 ;-D
-------------------------------------------------------------------------
* ISSUE <email> absolute and incremental move fields size restored (bug introduced in 1.30)
* ISSUE <email> CJOG used when in CONFIG MODE, and JOG added when in OPER MODE
* Set minimum size of 1200x720 to avoid fields/text overlaps

IcepapCMS 1.30 2014/12/11
-------------------------------------------------------------------------
* Some IO and ENCODER comboboxes are now wider to adjust to options length
* ISSUE 074 [TEST] ADDED CSWITCH command input parameter (not functional)
* ISSUE 074 [IO] EXTDISABLE, EXTBUSY and EXTPOWER parameters accessible
* ISSUE 074 [IO] Alarm signals group renamed to Input Control Signals
* ISSUE 074 [CLOOP] STRTVEL paramter accessible
* ISSUE 074 [CLOOP] PCLMODE SIMPLECHK flag parameter accessible
* ISSUE 074 [AXIS] STRTVEL moved to closed loop tab
* ISSUE 074 [AXIS] LNKNAME parameter accessible
* ISSUE 074 [AXIS] POSSRC paramter removed
* ISSUE 074 [AXIS] Position Control updated
?) renamed user manual from doc/IcePAP_UserManual_working.pdf to doc/IcePAP_UserManual.pdf

IcepapCMS 1.29 2014/02/26 (ESRF-BLISS synchronization)
IcepapCMS 1.26 2014/02/26
-------------------------------------------------------------------------
* ISSUE 068 Better IcepapCMS starting time.
* ISSUE 068 Upgrade to storm to 0.20
* ISSUE 070 Added LNKNAME option in INDEXER command, and command disabled
* ISSUE 065 Removed forced uppercase driver name and lnkname
* ISSUE 055 Catalog template management available for Qt 4.7
* ISSUE 056 (part) Position control register updated in axis tab
* ISSUE 056 (part) AbsEnc offset allows negative values

IcepapCMS 1.25 2013/07/11
-------------------------------------------------------------------------
* ISG 053: Fixed, new hook available in src/lib_icepapcms/icepapsystem.py method checkAutoSolvedConflict()
* Catalog search engine uses <space> to join word with an 'OR' operator
* Added the possibility to edit STRING? param types with a QLineEdit
* Added _MANUALLY_ 'LINKED' as an 'INDEXER' option, because it is missing in CFGINFO, some day should be removed

IcepapCMS 1.24 2012/11/05
-------------------------------------------------------------------------
* ISG 022: Icon in tabs to notify about modified or validate pending parameters
* ISG 021: Parameter tooltips visible again
* ISG 010: If driver name contains 'ERROR' change it to ''
* If driver name has a non-ascii character (exception), continue the loop with the rest of the drivers
* Fixed bug in doCopy when creating TemporaryFile


IcepapCMS 1.23 2011/01/20
-------------------------------------------------------------------------
* Solved NEW driver management: leave the system as before if 'Cancel'
* CONFIG mode only while configuring driver: Send clicked and Save pending
* 'SAVE' button only when 'SEND' is done (send pending to be committed)
* Exit application dialog message changed sign word for validate
* Save config button text changed to 'Validate Config'
* Bug solved, when exiting the application if discarding changes restore config

IcepapCMS 1.22 2010/08/24
-------------------------------------------------------------------------
* JOG driver using the slider is now implemented
* Implemented actions for Copy&Paste driver configuration with shortcuts CTRL+C and CTRL+V
* Only if a driver is left in state 'save pending' the Save Config action button is enabled
* IcepapCMS handles icepap drivers in PROG mode and disables the edition of parameters
* Icepap console does not try to connect if the host text is empty
* Button to set power ON/OFF now updates it's text if the power state is changed by another process
* Fixed bug that sometimes the driver was left in a state of 'save pending'
* NAMELOCK parameter does not interfere any more when setting the name
* Driver ID does not trigger any conflict
* Added the command line option '--skip-versioncheck' == '-s' to avoid firmware version checks
* By default, log is not enabled
* Locations must have at least one character
* ?_FSTATUS and ?_FPOS used for single axis queries (old ?FSTATUS and ?FPOS are used as a fallback)
* Imporved the scan time by only asking cfginfo for unknown versions 48 axis lasted 12 secs, now 5 secs
* Check if the driver is with power ON using the status register instead of another call N:?POWER
* Do not print the warning about not standard signature

IcepapCMS 1.21 2010/04/14
-------------------------------------------------------------------------
* Fixed bug Icepap Console does not report an error if <ENTER> is pressed without a command
* Fixed bug Icepap Console now puts the prompt at the end of the document when clicked
* Fixed bug Default Enc register is now 'EncIn' instead of Axis
* Fixed bug Enocer tab 'resoluion' typo
* Fixed bug in firmware upgrade 64 bits, problem packaging the 'tocho'
* Fixed bug in firmware upgrade, if no serial ports
* Fixed bug in ldap check, generic accounts 'sicilia' and 'operator' not allowed
* Fixed bug which could not downgrade if 'old values in db' where not in the downgraded version

IcepapCMS 1.20 2010/03/05
-------------------------------------------------------------------------
* LDAP login support
* Signature time and date in a readable format %Y/%m/%d_%H:%M:%S
* Various minor bugfixes...

IcepapCMS 1.19 2009/12/17
-------------------------------------------------------------------------
* Fixed console text did not show until disconnecting
* Changed console text background to white to see the blocking cursor properly and clearer text
* Allow text selection in the console
* New launcher for just the console called: ipapconsole
* Extra flag for Homing NEGEDGE_POSDIR Changed to NEGEDGE
* Unknown Tab problem with 32-bit machines solved
* Unknown Tab that was not kept selected after send/save config solved

IcepapCMS 1.18 2009/10/07
-------------------------------------------------------------------------
* Extra flag for Homing: NEGEDGE_POSDIR
* Two checkboxes removed: 'Enable closed loop' and 'Enable position control'
* Display PopUp messages when communication errors.
* Negative and Positive limit leds changed.
* IcepapCMS should be _usable_ with a resolution of 800x600.
* Icepap console updates after each keystroke
* No warning about mismatching firmware versions. (disabled)
* User interface more compact and not _so_ expanded

IcepapCMS 1.17 2009/08/04
-------------------------------------------------------------------------
* The new axis config xml file does not have sections any more. There is compatibility with old configs.
* New dialog for new driver has been integrated taking into account the expert flag
* New conflict dialogs have been integrated with extra table info for values, and checking expert flag
* As suggested, there is a highlight in the text of the tabs if some parameter is pending to send/save
* Added more info when restoring values from database if there is an exception
* Support for all types of unknown parameters and do not show the tab if not needed
* Fixed bug in send/save/action-save that was more times enabled than needed
* Fixed bug when adding systems sometimes they appeared as 'NEW' the second time the application started
* Location management has been redesigned and add/remove locations is only possible through the File menu
* Tree Explorer is not closable/movable/floatable any more
* Removed the location bar and all the logic that was used for the navigation through the tree
* The description box has tooltip for last signature details and changes backround based on 'ACTIVE'
* Fixed bug when discarding to sign drivers, the database was updated with wrong values
* The command widgets like INFOASRC/POL are now highlighted in blue if the current value is
* New ui interface in tabs has been implemented, there's pending a better layout of the widgets.
* The tree nodes are updated when the driver name changes in the database
* Support for FLAG_TYPE parameters usign a QFrame and checkboxes inside
* Drivers are always in CONFIG mode if selected. They remain in CONFIG if have to be signed
* The catalog now supports a preferences local folder for more custom sets of values
   In addendum, it is now possible to set any parameter in the template, and use doubleclick.
* The conflict resolution is driven only by the dialogs and the EXPERT_FLAG parameter
   no more preference checkbox is needed
* Adding a system without axis is now possible
* Store configuration append '.xml' extension
* Typo: close loop -> closed loop
* Adapt all the code in order to avoid deprecated pyIcePAP functions
* Blink for ten minutes instead of an hour
* All icepap interaction with # ACK by default
* Add user name in signature: user@host_hex(timestamp)
* Use pyIcePAP.drivers_alive()

IcepapCMS 1.16 2009/05/?? - Never released as a end-user version, always for developers
-------------------------------------------------------------------------
* Added support for the new ?VER SAVED command available since 1.16
* Added support for the new ?_PROG command available since MCPU 0.17
* Fixed bug on setting enc position (it did a POS command instead of an ENC command)
* Fixed bug on conflicts with FLAG-type parameters

IcepapCMS 1.15 2008/11/05
-------------------------------------------------------------------------
* Implemented behaviour for the --all-netwroks options flag
* Command line options added: --expert, --all-networks
* Two more directories in the preferences: Configurations + firmware
* Blink button remains pressed until the user clicks it again
* Save config does not popup anything unless some error in the process
* Save config also performs "Send Config" if not done by the user
* Fixed Current Config button behaviour
* Fixed Undo button behaviour
* Solve minibug in Icepap Console timout handling
* Added waiting cursor when saving configuration
* Solve minibug Sending config not always should set CONFIG mode
* Solve minibug in 2nd time starting IcepapCMS without accepting preferences
* Solve minibug when deleting systems while connected to them

* Last driver signature updated when saving config
* Blink button available in the top blue box of the driver view
* Set EXPERT_FLAG available under Driver menu as a checkbox
* New conflict resolution based on EXPERT_FLAG
   - New drivers: Prompt "Reset to default?" Cancel | Ok (both answers resolve conflict)
   - Moved drivers: Same as New Drivers (Do not prompt for all configs of the same driver
   - Modified without EXPERT flag: "Set DataBase Values?" Cancel | Ok (only Ok resolves conflict)
   - Modified with EXPERT flag: "Set Driver Values?" Cancel | Ok (only Ok resolves conflict)
   - If expert flag is detected, the application removes the flag from the driver
   - The YES-NO dialog shows the parameters which differ
* Firmware versions check (master != drivers) and upgrade progress bar
* Solved errors in the system/crate views while in PROG MODE
* Solve minibug, now it is possible to change info signals in test tab
* Add Close Loop option in main page CLOOPENC -> PCLOOP
* Import and export configurations to files supports the Unknown parameters
* STRTVEL param is now supported (it used to be DEFIVEL)
* Support for ?active's answer: '???' instead of 'YES' in some firmware versions

IcepapCMS 1.14 2008/06/18
-------------------------------------------------------------------------
* Solved mini-bug when updating the CFG ACTIVE parameter
* New limits for spinboxes: ICURR,BCURR: 100; NRSTEPS: 2^32
* New / Moved drivers present a conflict: Reset to defaults or
   keep the current driver config
* When adding an Icepap system the cursor is changed for a waiting
   clock one
* Active status is checked in order to change the CFG ACTIVE parameter
* Support for the Icepap Motor Types Catalog
* Put a 'SAVE Config' button under the 'SEND Config'button
* Wait for the second '$' to all icepap answers that start with '$'
* The ComboBox Unkonwn parameters have "LIST value" in the
   Description field
* Parse signature and show host and epoch using the ctime() function
* typo: Status message: conflics -> conflicts
* Better names: Apply Config -> Send Config ,
   Sign Config -> Save Config
* Better names: enable -> power ON , disable -> powerOFF (driver widget)
* Added support for the driver name conflicts
* The upgrade firmware function gives time to the triton to compute
   the checksum before disconnecting
* CFGINFO answers are readed until the final '$' is found

IcepapCMS 1.13 2008/04/02
-------------------------------------------------------------------------
* The timeout errors doesn't freeze any more the application
* When scanning a system or preparing the driver page, a clock cursor
   is shown
* upper-lower case conflicts are ignored for highlighting
* Accessing for first time does not create conflicts any more
* Adding icepap: Notification of which location has already the system
* Status bar conflict messages cleared when conflicts are solved
* The system preiodic refresh task keeps only one call to refresh
   methods for system and crate
* Changing location does not report connection errors (previous
   opened systems)
* If the driver is in config mode, the application can perform
   absolute and relative movements
* It doesn't allow to add a system if it is already defined in the
   database
* Version support with the Help->About menu action
* The icepap system tree has the drivers sorted
* When adding a system handle the connection exceptions like 'No
   route to host'
* The VERSION file with all features/bug-fixing history
* The config values are set to the icepap system using the ?CFGINFO
   order
* The icepap systems tree is now sorted and it keeps the position
* Driver parameters new to the GUI can be modifed in the "Unknown
   tab"
* Some widgets did not highlight properly
* All widgets have a tooltip from the
   src/templates/driverparameters.xml file
* In case of removed drivers, the application does not hang any more
* Proper refresh of the driver name properly
* Driver name included in historic configurations
* Historic configurations syncronizations has been revised
* The too-slow behaviour when applying changes or signing has been
   fixed


IcepapCMS 1.12 2008/02/26
-------------------------------------------------------------------------
* After applying the config, the system checks all the configuration
   to highlight possible changes
* The application can connect to different drivers with different
   firmware versions. The parameters and the possible values for each
   are retrieved from the same drivers using ?CFGINFO, instead of
   hard-coded in the application
* YELLOW highlight for values that differ from IcepapCMS and Driver,
   SALMON highlight for values that are equal in the application and
   the driver, but differ from the database values
* The application can work with: IDLE VOLTAGE, REGULATION GAIN,
   POSITION SRC, IDLE CURRENT, BOOST CURRENT, and ALL SSI parameters
* Change ENABLE/DISABLE with ON/OFF
* The application supports connections and disconnections from the
   icepap systems without hanging

IcepapCMS 1.11 2008/02/21
-------------------------------------------------------------------------
* Sign driver configuration should save data in the database
* Regulation gain should be inside the 'Pi Current Regulation'
   section
* Drop down menus should be also yellow when changing the values
* The preferences dialog should end with an OK button instead of a
   CLOSE button
* Log window for firmware upgrade should auto scroll-down
* Icepap systems tree puts at bottom the last opened system it should
   preserve the systems' order presented at startup
* Idle voltage should be presented AFTER nominal voltage
* The parameter for signing could be epoch in hex + hostname
* Microstepping should disappear from the test tab
* When closing the application, it should close the console
* Typo: The tune testing tab should say 'INFO SIGNALS' instead of
   'INFO SINGAL'
* Typo: Right click a driver, the popup should say 'SYSTEM' instead
   of SYSTEN'
* When displaying a driver, the version shown should be the driver's
   one instead of the DSP one
* BM01 gets stuck when reading 4 crates
* The Add/Remove Icepap System action should commit to the database,
   by now, it only commits on exit
* The communication test in the Upgrade firmware window doesn't work
* The Default acceleration time should inform that it is in SECOND
   units
