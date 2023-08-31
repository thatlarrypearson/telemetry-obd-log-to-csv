# Telemetry GPS Location and Time Logger

## **STILL UNDER CONSTRUCTION** but it is getting closer

The Telemetry GPS Logger captures location and time data using a GPS receiver. While the logger is running, location and time output is written to files and/or shared memory.

## Motivation

Integrate GPS location and time data collection with vehicle engine data for better, more accurate analytics.

## Features

- Logs location data to file and/or to shared memory
- Works with a chip set family ([u-blox]((https://www.u-blox.com)) supporting GPS, GLONASS, Galileo and BeiDou Global Navigation Satellite Systems (GNSS)
- Works with large family of GNSS enabling multiple constellations of satellites transmitting positioning and timing data
- Works with Python 3.10 and newer
- Raspberry Pi 4 hardware and Raspberry Pi OS target environment
- When using the shared memory feature, it doesn't matter which program is started first - this program ```gps_logger.gps_logger```, the location data generator, can start first or consuming programs like ```telemetry_obd.obd_logger``` can start first
- Two forms of data file naming based on the existence of the parameter ```--output_file_name_counter```.  The first form without the parameter is ```data/NMEA-<YYYYMMDDhhmmss>-utc.json```.  The second form with the parameter is ```data/NMEA-<counter>``` where counter would be ```0000000001``` for the first file, ```0000000002``` for the second file and so on.

## Target System

Raspberry Pi 4 with 4 GB RAM (or more) and with a 32 GB (or more) SD card.

## Target Hardware

Devices supporting USB or **RS-232**/**UART** interfaces made from **u-blox 8** or **u-blox M8** GPS receiver chip sets are required for this application.  **u-blox** devices support the **UBX** protocol in addition to the **NMEA** protocol.  UBX is used for device configuration.  **NMEA** is used to decode **NMEA** location data.  The libraries used to support this application are bilingual.  That is, the libraries speak both **UBX** and **NMEA**.

Interfaces not supported include **SPI**, **I2C** and **DDC**.

The reference hardware is [Waveshare NEO-M8T GNSS TIMING HAT for Raspberry Pi, Single-Satellite Timing, Concurrent Reception of GPS, Beidou, Galileo, GLONASS](https://www.waveshare.com/neo-m8t-gnss-timing-hat.htm).  The board has a USB interface as well as a serial RS-232/UART interface.  The correct USB cable comes in the package.  The board is also a Raspberry Pi HAT.  Using the Raspberry Pi header, the board plugs into a UART interface.  GPS board comes with an external GPS antenna, a useful feature to keep electronics off the dashboard and out of the sun.

The **u-blox** device on the reference hardware is a [NEO-M8T](https://www.u-blox.com/en/product/neolea-m8t-series) chip.

## Usage

```bash
$ python3.10 -m gps_logger.gps_logger --help
usage: gps_logger.py [-h] [--log_file_directory LOG_FILE_DIRECTORY] [--shared_dictionary_name SHARED_DICTIONARY_NAME]
                     [--shared_dictionary_command_list SHARED_DICTIONARY_COMMAND_LIST] [--serial SERIAL] [--verbose] [--version]

Telemetry GPS Logger

options:
  -h, --help            show this help message and exit
  --log_file_directory LOG_FILE_DIRECTORY
                        Enable logging and place log files into this directory
  --shared_dictionary_name SHARED_DICTIONARY_NAME
                        Enable shared memory/dictionary using this name
  --shared_dictionary_command_list SHARED_DICTIONARY_COMMAND_LIST
                        Comma separated list of NMEA commands/sentences to be shared (no spaces), defaults to all.
  --message_rate MESSAGE_RATE
                        Number of whole seconds between each GPS fix.  Defaults to 1.
  --output_file_name_counter
                        Base output file name on counter not timestamps
  --serial SERIAL       Full path to the serial device where the GPS can be found, defaults to /dev/ttyACM0
  --verbose             Turn DEBUG logging on. Default is off.
  --version             Print version number and exit.
$
```

### ```--output_file_name_counter```

```--output_file_name_counter``` changes the way data files are named.  Without this flag, data file names are in the form ```<VIN>-YYYYMMDDhhmmss-utc.json```.  With this flag set, data files are named using the counter stored in a file named in the form ```<VIN>-counter_value.txt``` found in the ```base_path``` directory (defaults to ```data```).  The first time a particular VIN (vehicle identification number) is encountered, the first value will be ```1```.

The **counter** values can be retrieved using the following ```bash``` commands:

```bash
cd ~/telemetry-obd/data
for fname in *counter_value.txt
do
  echo ${fname}: $(cat ${fname})
done
```

### ```--shared_dictionary_command_list```

List of NMEA commands/sentences that are known to this application:

- ```NMEA_GNGNS```: Fix data
- ```NMEA_GNGST```: Pseudorange error statistics
- ```NMEA_GNTHS```: True heading and status
- ```NMEA_GNZTD```: Time and data

### ```--version```

Responds with the version and exits.

## Log File Format

Logging is enabled by setting the log file directory ```--log_file_directory``` in the command line options.  The log file format is the same format used by [Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd#telemetry-obd-logger-output-data-files).  Downstream processing of data captured by both **Telemetry OBD Logger** and **Telemetry GPS Logger** and other data sources can be processed using the same analysis tools.

Records in the log files are separated by line feeds ```<LF>```.  Each record is in JSON format representing the key/value pairs described below under [JSON Fields](#json-fields).

### JSON Fields

#### ```command_name```

The ```command_name``` identifies (```NMEA_<talker identifier><sentence formatter>```) the GPS data source.  See **Section 31 NMEA Protocol** in the [u-blox 8 / u-blox M8 Receiver description Manual](https://content.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_UBX-13003221.pdf).  The current GPS data sources have a talker identifier of ```GN``` indicating any combination of GNSS (GPS, SBAS, QZSS, GLONASS, Galileo and/or BeiDou) as supported by the GPS unit will be used for positioning output data.  The supported sentence formatters are ```GNS```, ```GST```, ```THS``` and ```VTD```.

- ```NMEA_<talker identifier><sentence formatter>```
  - ```NMEA_<GN><GNS>```: Fix data
  - ```NMEA_<GN><GST>```: Pseudorange error statistics
  - ```NMEA_<GN><THS>```: True heading and status
  - ```NMEA_<GN><ZDA>```: Time and date

#### ```obd_response_value```

Reflects the key/value pairs returned by the GPS.  The actual parsed NMEA output is contained in the ```obd_response_value``` field as a dictionary (key/value pairs).  That is, ```obd_response_value``` is a field that contains an NMEA record which also contains fields.  The field name is the key portion of the field.  The field value is the value part of the field.  Each NMEA sentence has its own unique set of field names.

- ```NMEA_GNGNS```: ```GNS``` Fix data
  - ```field_name_0```: ```field_value_type_0```
- ```NMEA_GNGST```: ```GST``` Pseudorange error statistics
  - ```field_name_0```: ```field_value_type_0```
- ```NMEA_GNTHS```: ```THS``` True heading and status
  - ```field_name_0```: ```field_value_type_0```
- ```NMEA_GNVTD```: ```VTD``` Time and data
  - ```field_name_0```: ```field_value_type_0```

```iso_ts_pre``` ISO formatted timestamp taken before the GPS command was processed (```datetime.isoformat(datetime.now(tz=timezone.utc))```).

```iso_ts_post``` ISO formatted timestamp taken after the GPS command was processed (```datetime.isoformat(datetime.now(tz=timezone.utc))```).

### NMEA Sample Log Output

In the sample output below, the format has been modified for readability.  Below, the ```<LF>``` refers to Linux line feed and is used as a record terminator.

```bash
$ cd teleletry-gps/data
$ cat NMEA-20220525142137-utc.json
{
    "command_name": "NMEA_GNVTG",
    "obd_response_value":
    {
        "cogt": null,
        "cogtUnit": "T",
        "cogm": null,
        "cogmUnit": "M",
        "sogn": "0.024",
        "sognUnit": "N",
        "sogk": "0.045",
        "sogkUnit": "K",
        "posMode": "A"
    },
    "iso_format_pre": "2022-05-25T14:45:18.162234+00:00",
    "iso_format_post": "2022-05-25T14:45:22.121613+00:00"
}<LF>
{
    "command_name": "NMEA_GNGNS",
    "obd_response_value":
    {
        "time": "14:45:22",
        "lat": "29.5000000",
        "NS": "N",
        "lon": "-98.43000000",
        "EW": "W",
        "posMode": "AA",
        "numSV": "11",
        "HDOP": "1.08",
        "alt": "300.6",
        "sep": "-22.8",
        "diffAge": null,
        "diffStation": null
    },
    "iso_format_pre": "2022-05-25T14:45:22.125739+00:00",
    "iso_format_post": "2022-05-25T14:45:22.128793+00:00"
}<LF>
{
    "command_name": "NMEA_GNGST",
    "obd_response_value":
    {
        "time": "14:45:22",
        "rangeRms": "32.0",
        "stdMajor": null,
        "stdMinor": null,
        "orient": null,
        "stdLat": "2.1",
        "stdLong": "1.1",
        "stdAlt": "2.4"
    },
    "iso_format_pre": "2022-05-25T14:45:22.133219+00:00",
    "iso_format_post": "2022-05-25T14:45:22.135003+00:00"
}<LF>
{
    "command_name": "NMEA_GNZDA",
    "obd_response_value":
    {
        "time": "14:45:22",
        "day": "25",
        "month": "5",
        "year": "2022",
        "ltzh": "00",
        "ltzn": "00"
    },
    "iso_format_pre": "2022-05-25T14:45:22.141224+00:00",
    "iso_format_post": "2022-05-25T14:45:22.142981+00:00"
}<LF>
$
```

## Installation

Installation instructions were written for Raspberry Pi OS 64 bit:

- ```/etc/debian_version``` shows *11.3*
- ```/etc/release``` shows *bullseye*

With some, little or no modification, the installation instructions should work for other Linux based systems.  The amount of effort will vary by Linux distribution with Debian based distributions the easiest.

### Dependencies

*telemetry-gps* requires a number of Libraries and Python packages that need to be installed before installing this package.  Follow installation instruction links for the following:

- [Python 3.10 and 3.11](https://github.com/thatlarrypearson/telemetry-obd#raspberry-pi-system-installation)
  - provides the runtime environment for the application
  - follow the above link
- [PyGPSClient](docs/PyGPSClient.md)
  - provides a method to debug GPS connection and configuration issues
  - follow the above link

Then install the following in no particular order.

- [pyserial](https://pyserial.readthedocs.io/en/latest)
- [pyubx2](https://github.com/semuconsulting/pyubx2)
- [pynmeagps](https://github.com/semuconsulting/pynmeagps)

```bash
# Serial Interface Library
python3.10 -m pip install pyserial

# UBX and NMEA Libraries
python3.10 -m pip install --user --upgrade pyubx2 pynmeagps
```

The following are optional packages and are only required if vehicle location data is to be combined with weather and vehicle engine data using shared memory.

- [Telemetry OBD Logging](https://github.com/thatlarrypearson/telemetry-obd)
  - Engine data logger supporting shared memory
- [Telemetry Weather Logging](https://github.com/thatlarrypearson/telemetry-wthr)
  - Weather data logger supporting shared memory
- [UltraDict](docs/README-UltraDict.md)
  - Python library providing shared memory support

Once the dependencies are installed and working, the shared memory features can be tested.

### Building and Installing ```gps_logger``` Python Package

```bash
git clone https://github.com/thatlarrypearson/telemetry-gps.git
cd telemetry-gps
python3.10 -m build .
python3.10 -m pip install dist/ telemetry_gps-0.1.0-py3-none-any.whl
```

### Raspberry Pi Headless Operation

To access the GPS, the username running ```gps_logger``` will need to be a member of the ```dialout``` group.

```bash
# add dialout group to the current user's capabilities
sudo adduser $(whoami) dialout
```

To start ```gps_logger.gps_logger``` at boot on a Raspberry Pi, add the section of code starting with ```# BEGIN TELEMETRY-GPS SUPPORT``` and ending with ```# END TELEMETRY-GPS SUPPORT``` to ```/etc/rc.local```.

```bash
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

# BEGIN TELEMETRY-GPS SUPPORT
# This section goes before the TELEMETRY_OBD section

/bin/nohup "/root/bin/telemetry.rc.local.gps" &

# END TELEMETRY-GPS SUPPORT

# BEGIN TELEMETRY-OBD SUPPORT

/bin/nohup "/root/bin/telemetry.rc.local" &

# END TELEMETRY-OBD SUPPORT

exit 0
```

```/etc/rc.local``` executes ```/root/bin/telemetry.rc.local```.  In this file, the value for ```GPS_USER``` will need to be changed to match the username responsible for running this application.

```bash
#!/usr/bin/bash
#
# telemetry.rc.local.gps - This script is executed by the system /etc/rc.local script on system boot

export GPS_USER="human"
export GPS_GROUP="dialout"
export GPS_HOME="/home/${GPS_USER}"
export DEBUG="True"
export LOG_FILE="/tmp/telemetry-gps_$(date '+%Y-%m-%d_%H:%M:%S').log"

# Debugging support
if [ "${DEBUG}" == "True" ]
then
	# enable shell debug mode
	set -x
fi

# turn off stdin
0<&-

# redirect all stdout and stderr to file
exec &> "${LOG_FILE}"

## Run the script gps_logger.sh as user "${GPS_USER}" and group "${GPS_GROUP}"
runuser -u "${GPS_USER}" -g dialout "${GPS_HOME}/telemetry-gps/bin/gps_logger.sh" &

exit 0
```

To ready the system to autostart GPS logging, copy ```telemetry.rc.local``` to ```/root/bin``` and set its file system permissions as shown below.

```bash
$ cd
$ cd telemetry-gps/root/bin
$ sudo mkdir /root/bin
$ sudo cp telemetry.rc.local.gps /root/bin/
$ sudo chmod 0755 /root/bin/telemetry0rc.local.gps
$ sudo chmod 0755 /root/bin/telemetry.rc.local.gps
$ cd
```

```/root/bin/telemetry.rc.local``` executes ```telemetry-gps/bin/gps_logger.sh```  Lines 47 and 48 of ```gps_logger.sh``` have ```--shared_dictionary_name``` and ```--log_file_directory``` arguments.

If the shared dictionary/memory feature is going to be used, leave that line in place.  If logging to a file is needed, leave that line in place.  Otherwise, remove the unwanted argument lines.  One final note.  Lines ending in ```\``` indicate a line continuation in the shell environment.  The last line shouldn't have a ```\``` at the end as there wouldn't be any lines to continue to.

If the GPS serial device isn't ```/dev/ttyACM0```, the serial device command line option will need to be added after lines 47 and 48.  If adding the default device, the added line might look like:

```bash
    --serial /dev/ttyACM0
```

Don't forget.  Lines ending in ```\``` indicate a line continuation.  A line continuation may be needed for the line above ```--serial```.

Finally, set ```gps_logger.sh``` file permissions to executable.

```bash
$ cd telemetry-gps
$ cd bin
$ chmod 0755 gps_logger.sh
$ cd
$
```

## Examples

See the ```bin/gps_logger.sh``` ```bash``` shell program for an example.

## Known Problems

The ```gps_logger.gps_logger``` application fails periodically when noise on the serial interfaces causes bit changes.  This extremely rare occurrence causes an ```NMEAParseError``` exception to be raised.  When ```NMEAParseError```s occur, the boot startup shell program ```bin/gps_logger.sh``` waits 20 seconds before restarting ```gps_logger.gps_logger```.

Zero length data files can occur when the Raspberry Pi host isn't seeing the GPS device.  For example, when a USB GPS device either has a bad cable or wasn't plugged in properly, the log files found in the ```tmp``` directory off the telemetry-gps project directory will have entries similar to the following:

```bash
Traceback (most recent call last):
  File "/home/human/.local/lib/python3.10/site-packages/serial/serialposix.py", line 322, in open
    self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
FileNotFoundError: [Errno 2] No such file or directory: '/dev/ttyACM0'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/local/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/home/human/telemetry-gps/gps_logger/gps_logger.py", line 148, in <module>
    main()
  File "/home/human/telemetry-gps/gps_logger/gps_logger.py", line 103, in main
    io_handle = initialize_gps(serial_device, 4)
  File "/home/human/telemetry-gps/gps_logger/connection.py", line 34, in initialize_gps
    io_handle = connect_to_gps(device_path, **kwargs)
  File "/home/human/telemetry-gps/gps_logger/connection.py", line 27, in connect_to_gps
    return Serial(port=device_path, **kwargs)
  File "/home/human/.local/lib/python3.10/site-packages/serial/serialutil.py", line 244, in __init__
    self.open()
  File "/home/human/.local/lib/python3.10/site-packages/serial/serialposix.py", line 325, in open
    raise SerialException(msg.errno, "could not open port {}: {}".format(self._port, msg))
serial.serialutil.SerialException: [Errno 2] could not open port /dev/ttyACM0: [Errno 2] No such file or directory: '/dev/ttyACM0'
```

Note the above places where it says ```No such file or directory: '/dev/ttyACM0'```.  ```/dev/ttypACM0``` is the default device file name for a Raspberry Pi USB GPS device.

The following shows how to identify and then remove zero length JSON data files.

```bash
$ # From the telemetry-gps project directory
$ cd data
$ ls -l
-rw-r--r-- 1 human 197609    3570 Aug 14 06:31 NMEA-20220814113106-utc.json
-rw-r--r-- 1 human 197609  143497 Aug 26 08:39 NMEA-20220826133137-utc.json
-rw-r--r-- 1 human 197609 1883662 Aug 26 10:34 NMEA-20220826134824-utc.json
-rw-r--r-- 1 human 197609   81748 Aug 26 10:39 NMEA-20220826153428-utc.json
-rw-r--r-- 1 human 197609  102988 Aug 26 10:56 NMEA-20220826155057-utc.json
-rw-r--r-- 1 human 197609   18169 Aug 26 11:08 NMEA-20220826160759-utc.json
-rw-r--r-- 1 human 197609 1617134 Aug 26 12:58 NMEA-20220826162732-utc.json
-rw-r--r-- 1 human 197609  411207 Aug 26 13:21 NMEA-20220826175820-utc.json
-rw-r--r-- 1 human 197609   19072 Sep  5 14:51 NMEA-20220905195019-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:08 NMEA-20220910170858-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:09 NMEA-20220910170909-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:09 NMEA-20220910170921-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:09 NMEA-20220910170931-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:09 NMEA-20220910170942-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:09 NMEA-20220910170952-utc.json
-rw-r--r-- 1 human 197609       0 Sep 10 12:10 NMEA-20220910171003-utc.json
$
$ # Above, files starting with "NMEA-20220910" are all zero length
$
$ # To find zero length JSON files programmatically:
$ find . -type f -name '*.json' -size 0 -print
NMEA-20220910170858-utc.json
NMEA-20220910170909-utc.json
NMEA-20220910170921-utc.json
NMEA-20220910170931-utc.json
NMEA-20220910170942-utc.json
NMEA-20220910170952-utc.json
NMEA-20220910171003-utc.json
$
$ # To find and delete zero length JSON files programmatically:
$ find . -type f -name '*.json' -size 0 -print | while read filename
> do
> echo "${fname}"
> rm -f "${fname}"
> done
./NMEA-20220910170858-utc.json
./NMEA-20220910170909-utc.json
./NMEA-20220910170921-utc.json
./NMEA-20220910170931-utc.json
./NMEA-20220910170942-utc.json
./NMEA-20220910170952-utc.json
./NMEA-20220910171003-utc.json
$
```

## Diagnosing UltraDict Related Problems

When using ```UltraDict```, the most embarrassing **bug** to find is the one where ```--shared_dictionary_name``` is set in the consuming application (e.g. ```telemetry_obd.obd_logger```) but GPS or weather data just isn't showing up.  When the expected data isn't showing up, add one or more of the following to the command line of ```telemetry_obd.obd_logger```:

- ```--shared_dictionary_command_list```
- ```--gps_defaults```
- ```--weather_defaults```

Ask me how I know. :unamused:

```UltraDict``` can be difficult to install on some systems such as **Windows 10**.  This library will work without UltraDict installed.  However, there will be a log message on startup whenever the ```--shared_dictionary_name``` command line argument is used as shown below.

```powershell
PS C:\Users\human\src\telemetry-wthr> python3.10 -m gps_logger.gps_logger --shared_dictionary_name gps
ERROR:gps_logger:import error: Shared Dictionary (gps) feature unsupported: UltraDict Not installed.
...
...
...
```

The following provides a method to verify that the shared memory has been mapped into the ```gps_logger``` process space.  These commands work on most Linux based computers including Raspberry Pi's running Raspberry Pi OS.

```bash
$ ps -eaf | grep python3.10 | grep -v grep
human     384572  380137  0 13:02 pts/2    00:00:00 python3.10 -m gps_logger.gps_logger --shared_dictionary_name GPS --log_file_directory data
$ pmap -x 384572 | grep -i GPS
384572:   python3.10 -m gps_logger.gps_logger --shared_dictionary_name GPS --log_file_directory data
0000007f9027a000    1024       0       0 rw-s- GPS_memory
0000007f91507000       4       4       4 rw-s- GPS
$
```

The first command gets a list of processes (```ps```) and sends its output to a filter (```grep```) that only passes through processes that contain the string ```python3.10```.  The first filter passes its output onto another filter (```-v```) that removes all output lines that contain ```grep```.  This results in process (```ps```) information that only includes process names with ```python3.10``` in them.

The second field in the process output is the process ID number.  This number (```384572```) is unique to an individual process running on the system.

Using the process ID number (```384572```), the process memory map command (```pmap```) is used to get that specific process's shared memory (```-x```) information.  We use the filter (```grep```) to pull out the lines that contain the shared dictionary name (```--shared_dictionary_name```) command line parameter (```GPS```) in a case independent way (```-i```).

The result is two memory mapped regions supporting the shared dictionary between ```gps_logger``` and other running processes like ```gps_logger```.

The following also shows shared memory owned by user ```human```.  It doesn't identify the use for the shared memory like the above example does.  This **is** useful because it shows the shared memory access permissions in the **perms** column.  The value ```600``` means the shared memory segment is accessible for read and write only by the owner ```human```.

```bash
$ ipcs -m

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status
0x00000000 2          human      600        134217728  2          dest
0x00000000 8          human      600        524288     2          dest
0x00000000 11         human      600        524288     2          dest
0x00000000 16         human      600        524288     2          dest
0x00000000 28         human      600        524288     2          dest

$
```

## Related

- [Telemetry OBD Data To CSV File](https://github.com/thatlarrypearson/telemetry-obd-log-to-csv)
  - Convert [Telemetry OBD Logger] and [Telemetry GPS Logger]() output to CSV format files suitable for importation into Python Pandas dataframes using the from_csv() method
  - Provides initial data analysis programs for ```telemetry_obd.obd_command_tester```, ```telemetry_obd.obd_logger``` and ```gps_logger.gps_logger``` output

- [Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd)
  - Logs vehicle engine data gathered using OBD interface
  - Accepts shared dictionary/memory information from this library for integration into its own log files

- [Telemetry Weather Logging](https://github.com/thatlarrypearson/telemetry-wthr)
  - Weather data logger supporting shared memory
  - Uses shared memory to share data with **Telemetry OBD Logger**

## License

[MIT](LICENSE.md)
