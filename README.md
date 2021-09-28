
# Telemetry OBD Data To CSV File

Convert [Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd) output to CSV format files suitable for importation into Python [Pandas](https://pandas.pydata.org/)  ```dataframe```s using the ```from_csv()``` method.

## Features

- Intelligently aggregates multiple vehicle OBD command responses into a record format for importing into common data analysis libraries such as Python Pandas
- Uses Python 3.8 or newer
- Runs on Windows, Mac and Linux
- Runs on [CPython](https://en.wikipedia.org/wiki/CPython) and [Anaconda Python](https://www.anaconda.com/)

When aggregating multiple OBD commands into records, ```obd_log_to_csv``` considers a record complete when it finds another entry for an OBD command already placed into the record.  OBD commands not found in the input by the time the record is complete are set to ```None``` in Python and that is translated to missing values in the CSV file.  In Pandas, such missing values get changed to ```NaN``` or Not a Number.

Time stamps are handled in the following way:

- ```iso_ts_pre```, the ISO format time stamp from right before an OBD command request is made to the vehicle, is set by the first OBD command included in the output record.

- ```iso_ts_post```, the ISO format time stamp from right after an OBD command response is received from the vehicle, is set by the last OBD command included in the output record.

## Installation

Pull this repository down from `git` then install using Python pip where the Python version is 3.8 or higher.

```bash
git clone https://github.com/thatlarrypearson/telemetry-obd-log-to-csv.git
python3.8 --version
python3.8 -m pip install --user pint python-dateutil
cd telemetry-obd-log-to-csv
python3.8 -m pip install --user .
```

When running Anaconda versions of Python, modify the ```pip install``` for ```pint``` and ```dateutil``` to be as follows:

```bash
conda install -c conda-forge pint
conda install python-dateutil
```

## Command Line Arguments

```bash
python3.8 -m obd_log_to_csv.obd_log_to_csv --help
usage: obd_log_to_csv [-h] [--commands [COMMANDS]] [--csv CSV] [--no_header] [--verbose] files [files ...]

Telemetry OBD Log To CSV

positional arguments:
  files                 telemetry_obd generated data files separated by spaces. Data file names can include
                        full or relative paths.

optional arguments:
  -h, --help            show this help message and exit
  --commands [COMMANDS]
                        Command name list to include in CSV output record generation. Comma separated list.
                        e.g. "SPEED,RPM,FUEL_RATE". In the JSON input, "command_name"
                        labelled items will be used. No Default value provided.
  --csv CSV             CSV output file. File can be either a full or relative path name. If the file already exists,
                        it will be overwritten.
  --no_header           CSV output file will NOT have a column name header record. Default is False.
                        (That is, a header will be produced by default.)
  --verbose             Turn verbose output on. Default is off.
```

## Documentation

At this time, this [README](./README.md) is the documentation.

## Related

Here are some related projects

- [telemetry-obd](https://github.com/thatlarrypearson/telemetry-obd): Telemetry OBDII (Onboard Diagnostic Data 2) Logger
- [telemetry-django-obd](https://github.com/thatlarrypearson/telemetry-django-obd): Django database OBD/ECU data loader

## Usage/Examples

The following example assumes data was collected using ```telemetry_obd.obd_logger``` and that the collected vehicle data is in the local directory ```data/{VehicleIdentificationNumber-VIN}```.  File names in the vehicle data directory will be in the form ```{VehicleIdentificationNumber-VIN}-{YYYYMMDDhhmmss}-utc.json``` where

- ```{VehicleIdentificationNumber-VIN}``` is the vehicle's VIN as collected by ```telemetry_obd.obd_logger```
- ```{YYYMMDDhhmmss}``` represents the date/time the data file was initially created.

On Linux/Mac, convert ```obd_logger``` generated data to Pandas compatible CSV format, the following command converts all of the data files in a vehicle's data directory into a single CSV format file.

```bash
export VIN="FT8W4DT5HED00000"
python3.8 -m obd_log_to_csv.obd_log_to_csv \
        --csv="${VIN}.csv" \
        --commands=ACCELERATOR_POS_D,ACCELERATOR_POS_E,AMBIANT_AIR_TEMP,BAROMETRIC_PRESSURE,COMMANDED_EGR,CONTROL_MODULE_VOLTAGE,COOLANT_TEMP,DISTANCE_SINCE_DTC_CLEAR,DISTANCE_W_MIL,ENGINE_LOAD,FUEL_LEVEL,FUEL_INJECT_TIMING,FUEL_RAIL_PRESSURE_ABS,FUEL_RAIL_PRESSURE_DIRECT,INTAKE_PRESSURE,INTAKE_TEMP,MAF,OIL_TEMP,RELATIVE_ACCEL_POS,RUN_TIME \
        data/"${VIN}"/*.json
```

In the above example, ```--commands={List-Of-OBD-Commands``` is all on a single line.  The ```\``` (back-slashes) at the ends of lines tell the ```bash``` (and other shells) interpreter to treat the following line as part of the current line.  The back-slashes were added to separate individual options/elements with the goal of improving readability.

Similarly, on Windows using PowerShell, the following will also process a group of files for the same vehicle assuming the same directory layout.

```powershell
$VIN ="FT8W4DT5HED00000"
python3.8 -m obd_log_to_csv.obd_log_to_csv --csv=${VIN}.csv --commands=RPM,SPEED,FUEL_RATE data/${VIN}/*.json
```

To load data into Python [Pandas](https://pandas.pydata.org/) and see the data types of each of the columns in the CSV file:

```Python
import pandas as pd
df = pd.read_csv('FT8W4DT5HED00000.csv', parse_dates=['iso_ts_pre', 'iso_ts_post', 'duration', ])
```

Missing values in the CSV input are translated into ```NaN``` or Not a Number in Pandas.

Note the ```parse_dates``` named argument in the ```read_csv()``` method call. The generated CSV file data from ```obd_log_to_csv``` always includes:

- ```iso_ts_pre```, an ISO formatted time stamp for when the first OBD command was found in the input for this record
- ```iso_ts_post```, an ISO formatted time stamp for when the last OBD command was found in the input for this record
- ```duration```, the difference in seconds between ```iso_ts_post``` and ```iso_ts_pre```

```parse_dates``` lets Pandas know that it should process those fields as dates.  As a result, the output data from ```df.types``` is

```python
df.dtypes
ACCELERATOR_POS_D                        float64
ACCELERATOR_POS_E                        float64
AMBIANT_AIR_TEMP                         float64
BAROMETRIC_PRESSURE                        int64
COMMANDED_EGR                            float64
CONTROL_MODULE_VOLTAGE                   float64
COOLANT_TEMP                             float64
DISTANCE_SINCE_DTC_CLEAR                 float64
DISTANCE_W_MIL                           float64
ENGINE_LOAD                              float64
FUEL_LEVEL                               float64
FUEL_INJECT_TIMING                       float64
FUEL_RAIL_PRESSURE_ABS                   float64
FUEL_RAIL_PRESSURE_DIRECT                float64
INTAKE_PRESSURE                            int64
INTAKE_TEMP                                int64
MAF                                      float64
OIL_TEMP                                   int64
RELATIVE_ACCEL_POS                       float64
RUN_TIME                                 float64
iso_ts_pre                   datetime64[ns, UTC]
iso_ts_post                  datetime64[ns, UTC]
duration                          datetime64[ns]
```

## License

[MIT](./LICENSE.md)
