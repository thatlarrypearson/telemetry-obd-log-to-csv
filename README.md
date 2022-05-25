# Telemetry GPS Location and Time Logger

## **STILL UNDER CONSTRUCTION** but it is getting closer

The Telemetry GPS Logger captures location and time data using a GPS receiver. While the logger is running, lcationa dn time output is written files and/or shared memory.

## Motivation

Integrate GPS location and time data collection with vehicle engine data for better, more accurate analytics.

## Features

- Logs location data to file and/or to shared memory
- Works with a chip set family ([u-blox]((https://www.u-blox.com)) supporting GPS, GLONASS, Galileo and BeiDou Global Navigation Satellite System (GNSS)
- Works with large family of GNSS enabling multiple constellations of satellites transmitting positioning and timing data
- Works with Python 3.10 and newer
- Raspberry Pi 4 and Raspberry Pi OS target environments
- When using the shared memory feature, it doesn't matter which program is started first - this program ```gps_logger.gps_logger```, the location data generator, can start first or consuming programs like ```obd_logger.obd_logger``` can start first

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
  --serial SERIAL       Full path to the serial device where the GPS can be found, defaults to /dev/ttyACM0
  --verbose             Turn DEBUG logging on. Default is off.
  --version             Print version number and exit.
$
```

List of NMEA commands/sentences that are know to this application:

- ```NMEA_GNGNS```: Fix data
- ```NMEA_GNGST```: Pseudorange error statistics
- ```NMEA_GNTHS```: True heading and status
- ```NMEA_GNZTD```: Time and data

## Log File Format

Logging is enabled by setting the log file directory ```--log_file_directory``` in the command line options.  The log file format is the same format used by [Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd#telemetry-obd-logger-output-data-files).  Downstream processing of data captured by both **Telemetry OBD Logger** and **Telemetry GPS Logger** and other data sources can be processed using the same analysis tools.

Records in the log files are separated by line feeds ```<LF>```.  Each record is in JSON format representing the key/value pairs described below under [JSON Fields](#json-fields).

### JSON Fields

#### ```command_name```

Provides ```NMEA_<talker identifier><sentence formatter>``` identifying the GPS data source.  See **Section 31 NMEA Protocol** in the [u-blox 8 / u-blox M8 Receiver description Manual](https://content.u-blox.com/sites/default/files/products/documents/u-blox8-M8_ReceiverDescrProtSpec_UBX-13003221.pdf).  The current GPS data sources have a talker identifier of ```GN``` indicating any combination of GNSS (GPS, SBAS, QZSS, GLONASS, Galileo and/or BeiDou) as supported by the GPS unit will be used for positioning output data.  The supported sentence formatters are ```GNS```, ```GST```, ```THS``` and ```VTD```.

- ```NMEA_GNGNS```: Fix data
- ```NMEA_GNGST```: Pseudorange error statistics
- ```NMEA_GNTHS```: True heading and status
- ```NMEA_GNZDA```: Time and date

#### ```obd_response_value```

Reflects the key/value pairs returned by the GPS.  The actual parsed NMEA output is contained in the ```obd_response_value``` field as a dictionary (key/value pairs).  That is, ```obd_response_value``` is a field that contains an NMEA record which also contains fields.

- ```NMEA_GNGNS```: ```GNS``` Fix data
- ```NMEA_GNGST```: ```GST``` Pseudorange error statistics
- ```NMEA_GNTHS```: ```THS``` True heading and status
- ```NMEA_GNVTD```: ```VTD``` Time and data

```iso_ts_pre``` ISO formatted timestamp taken before the GPS command was processed (```datetime.isoformat(datetime.now(tz=timezone.utc))```).

```iso_ts_post``` ISO formatted timestamp taken after the GPS command was processed (```datetime.isoformat(datetime.now(tz=timezone.utc))```).

### NMEA Sample Log Output

In the sample output below, the format has been modified for readability.

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
}
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
}
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
}
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
}
$
```

## Installation

Installation instructions were written for Raspberry Pi OS 64 bit:

- ```/etc/debian_version``` shows *11.3*
- ```/etc/release``` shows *bullseye*

With some, little or no modification, the installation instructions should work for other Linux based systems.  The amount of effort will vary by Linux distribution with Debian based distributions the easiest.

### Dependencies

*telemetry-gps* requires a number of Libraries and Python packages that need to be installed before installing this package.  Follow installation instruction links for the following:

- [Pythoon 3.10](https://github.com/thatlarrypearson/telemetry-obd#raspberry-pi-system-installation)
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

The following are optional packages and are only required if vehicle location data is to be combined with vehicle engine data using shared memory.

- [Telemetry OBD Logging](https://github.com/thatlarrypearson/telemetry-obd)
  - Engine data logger supporting shared memory
- [UltraDict](docs/README-UltraDict.md)
  - Python library providing shared memory support

Once the dependencies are installed and working, the shared memory features can be tested.

### Building and Installing ```gps_logger``` Python Package



## Examples

## Known Problems

The ```gps_logger.gps_logger``` application fails periodically when noise on the serial interfaces causes bit changes.  This extremely rare occurrence causes an ```NMEAParseError``` exception to be raised.  When ```NMEAParseError```s occur, the boot startup shell program ```bin/gps_logger.sh``` waits 20 seconds before restarting ```gps_logger.gps_logger```.

## Diagnosing UltraDict Related Problems

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

## License

[MIT](LICENSE)
