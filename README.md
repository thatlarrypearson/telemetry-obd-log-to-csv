# telemetry-gps

This repository is still under construction.

## Telemetry GPS Location and Time Logger

## Motivation

## Features

## Target System

## Target Hardware

## Usage

## Log File Format

Logging is enabled by setting the log file directory ```--log_file_directory``` in the command line options.  The log file format is the same format used by [Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd#telemetry-obd-logger-output-data-files).  Downstream processing of data captured by both **Telemetry OBD Logger** and **Telemetry GPS Logger** and other data sources can be processed using the same analysis tools.

Records in the log files are separated by line feeds ```<LF>```.  Each record is in JSON format representing the key/value pairs described below under [JSON Fields](#json-fields).

### JSON Fields

```command_name``` provides ```NMEA_<talker identifier><sentence formatter>``` identifying the GPS data source.  See **Section 31 NMEA Protocol** in the [u-blox 8 / u-blox M8 Receiver description Manual](https://content.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_UBX-13003221.pdf).  The current GPS data sources have a talker identifier if ```GN``` indicating any combination of GNSS (GPS, SBAS, QZSS, GLONASS, Galileo and/or BeiDou) as supported by the GPS unit will be used for positioning output data.  The supported sentence formatters are ```GNS```, ```GST```, ```VTG``` and ```ZDA```.

- ```NMEA_GNGNS```: Fix data
- ```NMEA_GNGST```: Pseudorange error statistics
- ```NMEA_GNTHS```: True heading and status
- ```NMEA_GNZTD```: Time and data

```obd_response_value``` reflects the key/value pairs returned by the GPS.

```iso_ts_pre``` ISO formatted timestamp taken before the GPS command was processed (```datetime.isoformat(datetime.now(tz=timezone.utc))```).

```iso_ts_post``` ISO formatted timestamp taken after the GPS command was processed (```datetime.isoformat(datetime.now(tz=timezone.utc))```).

### NMEA Output

## Installation

Installation instructions were written for Raspberry Pi OS 64 bit:

* ```/etc/debian_version``` shows *11.3*
* ```/etc/release``` shows *bullseye*

With some, little or no modification, the installation instructions should work for other Linux based systems.  The amount of effort will vary by Linux distribution with Debian based distributions the easiest.

### Dependencies

*telemetry-gps* requires a number of Libraries and Python packages that need to be installed before installing this package.  Follow installation instructions for the following:

* [Pythoon 3.10](https://github.com/thatlarrypearson/telemetry-obd#raspberry-pi-system-installation)
* [Telemetry OBD Logging](https://github.com/thatlarrypearson/telemetry-obd)
* [PyGPSClient](docs/PyGPSClient.md)

Then install the following in no particular order.

* [pyserial](https://pyserial.readthedocs.io/en/latest)
* [pyubx2](https://github.com/semuconsulting/pyubx2)
* [pynmeagps](https://github.com/semuconsulting/pynmeagps)
* [UltraDict](https://github.com/ronny-rentner/UltraDict)

```bash
# Serial Interface Library
python3.10 -m pip install pyserial

# UltraDict Dependencies
sudo apt-get install -y cmake
python3.10 -m pip install --user --upgrade pyrtcm
python3.3.10 -m pip install --user --upgrade atomics

# UBX and NMEA Libraries
python3.10 -m pip install --user --upgrade pyubx2 pynmeagps

# Atomics
python3.10 -m pip install --user --upgrade atomics

# UltraDict
git clone https://github.com/ronny-rentner/UltraDict.git
cd UltraDict
python3.10 -m build
python3.10 -m pip install --user dist/UltraDict-0.0.4-cp38-cp38-linux_aarch64.whl
```

## Examples

## Known Problems

[UltraDict](https://github.com/ronny-rentner/UltraDict) only supports Python versions 3.9 and newer.  This is requiring all **telemetry** modules to move away from Python 3.8.

```bash
# issue with UltraDict python3.8 support
python3.8 -m pip install --user dist/UltraDict-0.0.4-cp38-cp38-linux_aarch64.whl
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Processing ./dist/UltraDict-0.0.4-cp38-cp38-linux_aarch64.whl
ERROR: Package 'ultradict' requires a different Python: 3.8.13 not in '>=3.9'
```

## Diagnosing UltraDict Related Problems

The following provides a method to verify that the shared memory has been mapped into the ```gps_logger``` process space.  These commands work on most Linux based computers including Raspberry Pi's running Raspberry Pi OS.

The first command gets a list of processes (```ps```) and sends its output to a filter (```grep```) that only passes through processes that contain the string ```python3.10```.  The first filter passes its output onto another filter (```-v```) that removes all output lines that contain ```grep```.  This results in process (```ps```) information that only includes process names with ```python3.10``` in them.

The second field in the process output is the process ID number.  This number (```384572```) is unique to an individual process running on the system.

Using the process ID number (```384572```), the process memory map command (```pmap```) is used to get that specific process's shared memory (```-x```) information.  We use the filter (```grep```) to pull out the lines that contain the shared dictionary name (```--shared_dictionary_name```) command line parameter (```GPS```) in a case independent way (```-i```).

The result is two memory mapped regions supporting the shared dictionary between ```gps_logger``` and other running processes like ```gps_logger```.

```bash
$ ps -eaf | grep python3.10 | grep -v grep
human     384572  380137  0 13:02 pts/2    00:00:00 python3.10 -m gps_logger.gps_logger --shared_dictionary_name GPS --log_file_directory data
$ pmap -x 384572 | grep -i GPS
384572:   python3.10 -m gps_logger.gps_logger --shared_dictionary_name GPS --log_file_directory data
0000007f9027a000    1024       0       0 rw-s- GPS_memory
0000007f91507000       4       4       4 rw-s- GPS
$
```

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

## License

[MIT](LICENSE)
