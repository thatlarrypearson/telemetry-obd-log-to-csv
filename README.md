# Telemetry OBD Data To CSV File

Convert [Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd) output to CSV format files suitable for importation into Python [Pandas](https://pandas.pydata.org/)  ```dataframe``` using the ```from_csv()``` method.

## Features

- Intelligently aggregates multiple vehicle OBD command responses into a record format for importing into common data analysis libraries such as Python Pandas
- Comes with Python Pandas data analysis examples
- Runs in Jupyter Notebooks and can run as a function in Python programs
- Comes with post processing programs that add in
  - rates of change in numeric columns - e.g. ```SPEED``` can become ```ACCELERATION```
  - ratios in pairs of columns - e.g. ```RPM/SPEED``` provides a current gear ratio
- Uses Python 3.8 or newer (Testing done with Python 3.11)
- Runs on Windows, Mac and Linux

When aggregating multiple OBD commands into records, ```obd_log_to_csv``` considers a record complete when it finds another entry for an OBD command already placed into the record.  OBD commands not found in the input by the time the record is complete are set to ```None``` in Python and that is translated to missing values in the CSV file.  In Pandas, such missing values get changed to ```NaN``` or Not a Number.

Time stamps are handled in the following way:

- ```iso_ts_pre```, the ISO format time stamp from right before an OBD command request is made to the vehicle, is set by the first OBD command included in the output record.

- ```iso_ts_post```, the ISO format time stamp from right after an OBD command response is received from the vehicle, is set by the last OBD command included in the output record.

- ```duration```, the number of seconds between ```iso_ts_pre``` and ```iso_ts_post```.

## ```obd_log_to_csv.obd_log_to_csv``` Usage

Given vehicle telemetry data files created by ```telemetry_obd.obd_logger```, create ```CSV``` files suitable for importation into spreadsheets (i.e. Microsoft Excel) or Python Pandas ecosystem components.

```bash
$ python3.11 -m obd_log_to_csv.obd_log_to_csv --help
usage: obd_log_to_csv [-h] [--commands COMMANDS] [--csv CSV] [--no_header]
                      [--verbose]
                      files [files ...]

Telemetry OBD Log To CSV

positional arguments:
  files                telemetry_obd generated data files separated by spaces.
                       Data file names can include full or relative paths.

optional arguments:
  -h, --help           show this help message and exit
  --commands COMMANDS  Command name list to include in CSV output record
                       generation. Comma separated list. e.g.
                       "SPEED,RPM,FUEL_RATE". In the JSON input,
                       "command_name" labelled items will be used. No default
                       value provided.
  --csv CSV            CSV output file. File can be either a full or relative
                       path name. If the file already exists, it will be
                       overwritten. Defaults to standard output (stdout)
                       instead of file.
  --no_header          CSV output file will NOT have a column name header
                       record. Default is False. (That is, a header will be
                       produced by default.)
  --verbose            Turn verbose output on. Default is off.

$
```

## ```obd_log_to_csv.obd_log_to_csv``` Command Line Usage Examples

The following example assumes data was collected using ```telemetry_obd.obd_logger``` and that the collected vehicle data is in the local directory ```data/{VehicleIdentificationNumber-VIN}```.  File names in the vehicle data directory will be in the form ```{VehicleIdentificationNumber-VIN}-{YYYYMMDDhhmmss}-utc.json``` where

- ```{VehicleIdentificationNumber-VIN}``` is the vehicle's VIN as collected by ```telemetry_obd.obd_logger```
- ```{YYYMMDDhhmmss}``` represents the date/time the data file was initially created.

On Linux/Mac, convert ```obd_logger``` generated data to Pandas compatible CSV format, the following command converts all of the data files in a vehicle's data directory into a single CSV format file.

```bash
export VIN="FT8W4DT5HED00000"
python3.11 -m obd_log_to_csv.obd_log_to_csv \
        --csv="${VIN}.csv" \
        --commands=ACCELERATOR_POS_D,ACCELERATOR_POS_E,AMBIANT_AIR_TEMP,BAROMETRIC_PRESSURE,COMMANDED_EGR,CONTROL_MODULE_VOLTAGE,COOLANT_TEMP,DISTANCE_SINCE_DTC_CLEAR,DISTANCE_W_MIL,ENGINE_LOAD,FUEL_LEVEL,FUEL_INJECT_TIMING,FUEL_RAIL_PRESSURE_ABS,FUEL_RAIL_PRESSURE_DIRECT,INTAKE_PRESSURE,INTAKE_TEMP,MAF,OIL_TEMP,RELATIVE_ACCEL_POS,RUN_TIME \
        data/"${VIN}"/*.json
```

In the above example, ```--commands={List-Of-OBD-Commands``` is all on a single line.  The ```\``` (back-slashes) at the ends of lines tell the ```bash``` (and other shells) interpreter to treat the following line as part of the current line.  The back-slashes were added to separate individual options/elements with the goal of improving readability.

Similarly, on Windows using PowerShell, the following will also process a group of files for the same vehicle assuming the same directory layout.

```powershell
$VIN ="FT8W4DT5HED00000"
python3.11 -m obd_log_to_csv.obd_log_to_csv --csv=${VIN}.csv --commands=RPM,SPEED,FUEL_RATE data/${VIN}/*.json
```

## ```obd_log_to_csv.obd_log_to_csv``` Jupyter Notebook Usage Example

```python
```

## Installation

Clone this repository from `git` and install using Python pip where the Python version is 3.11 or higher.

In some newer version of Python, ```pip``` is handled differently and not necessarily better which is why the two following ```pip``` installations have the command line options they do.

```bash
git clone https://github.com/thatlarrypearson/telemetry-obd-log-to-csv.git
python3.11 --version

# Python pip Install Support
python3.11 -m pip install --upgrade --force-reinstall --user pip
python3.11 -m pip install --upgrade --force-reinstall --user wheel setuptools markdown build
cd telemetry-obd-log-to-csv
python3.11 -m build
python3.11 -m pip install --user dist/telemetry_obd_log_to_csv-0.3.3-py3-none-any.whl
```

## Documentation

This [README](./README.md) has other companion documents as shown below in [OBD Log Evaluation](#OBD-LOG-EVALUATION), [Post Processing](#Post-Processing) and [Data Analysis](#Data-Analysis).

### OBD Log Evaluation

As an aid to determining which OBD commands should be in ```obd_logger``` configuration files, [```obd_log_evaluation```](./docs/OBD_LOG_EVALUATION.md) analyses output from  ```telemetry_obd.obd_command_tester``` and ```telemetry_obd.obd_logger```.

### Post Processing

Additional data manipulation tools are available as part of this library and are described in [CSV File Post Processing](./docs/POST_PROCESSING.md).

### Data Analysis

Simple analysis tools based on [Python Pandas](https://pandas.pydata.org/) are shown in [CSV File Data Analysis](./docs/DATA_ANALYSIS.md).

## Example Programs

The repository's ```examples``` directory contains example programs showing how to extend and customize capabilities for different types of analysis.  The examples break down into two families of example programs:

- [Distance](docs/EXAMPLES-distance.md):
  Two methods for calculating distance travelled when target vehicle doesn't support ```ODOMETER``` OBD command.

- [Initial Data Analysis](docs/EXAMPLES-data_analysis.md):
  Simple data analysis creating artifacts assisting data analysts in identifying important or unexpected data relationships.

## Known Problems

Vehicle Identification Number (VIN) is not always correct.

- 2013 Jeep Wrangler Rubicon is missing leading ```1``` digit/letter
- 2017 Ford F-450 VIN is missing leading ```1``` digit/letter
- 2021 Toyota Sienna Hybrid LE is missing the trailing ```0``` digit/letter while another 2021 Sienna Hybrid LE (VIN: 5TDKRKEC6MS043967) was not missing any digits or letters.

## Related

Here are some related projects

- [telemetry-obd](https://github.com/thatlarrypearson/telemetry-obd): Telemetry OBDII (Onboard Diagnostic Data 2) Logger
- [telemetry-django-obd](https://github.com/thatlarrypearson/telemetry-django-obd): Django database OBD/ECU data loader

## License

[MIT](./LICENSE.md)
