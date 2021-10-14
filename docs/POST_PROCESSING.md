# CSV File Post Processing

## ```csv_to_delta_csv```

*OBD Log To CSV* (```obd_log_to_csv.obd_log_to_csv```) generated files are used as input to *CSV To Delta CSV* (```obd_log_to_csv.csv_to_delta_csv```).  Each column and each row in the input passes through *CSV To Delta CSV*.  *CSV To Delta CSV* adds columns, named delta colums, based on the ```--delta``` argument.

### Example

For example, an acceleration column can be added onto an input file containing a column ```SPEED``` as shown below.

```bash
$ python3.8 -m obd_log_to_csv.csv_to_delta_csv \
                --input_csv_file FT8W4DT5HED65995-cycle.csv \
                --output_csv_file delta-speed.csv \
                --delta SPEED
```

### Usage

```bash
$ python3.8 -m obd_log_to_csv.csv_to_delta_csv --help
usage: obd_log_to_csv [-h] [--input_csv_file INPUT_CSV_FILE] [--delta DELTA] [--output_csv_file OUTPUT_CSV_FILE] [--verbose]

Telemetry CSV To Delta CSV generates values indicating the rate of change for identified columns. All original columns pass through unmolested.
The delta columns are added columns.

optional arguments:
  -h, --help            show this help message and exit
  --input_csv_file INPUT_CSV_FILE
                        CSV file generated by obd_log_to_csv.obd_log_to_csv that includes the header. That is, each column in the file has a
                        valid text column name in the first row.
  --delta DELTA         Comma separated list of commands where successive pairs of non-null return values would be used to calculate the rate of
                        change between the two return values. e.g. "SPEED,FUEL_LEVEL,THROTTLE_POSITION". Calculated using
                        "(second-return-value - first-return-value) / (second-iso_ts_post - first-iso_ts_post)". 
                        Applied in this way, delta SPEED would represent
                        acceleration. The results will be in a column headed by delta-COMMAND_NAME. e.g. delta SPEED column name would be
                        "delta-SPEED".
  --output_csv_file OUTPUT_CSV_FILE
                        CSV output file. File can be either a full or relative path name. If the file already exists, it will be overwritten. Do
                        not make the input and output file the same. Bad things will happen.
  --verbose             Turn verbose output on. Default is off.
```

### Unit Conversions

In the previous example, ```SPEED``` was used for the ```--delta``` column name.  ```SPEED``` is expressed in ```kilometers / hour```.   To be meanaingful, ```kilometers / hour``` needs to be converted to ```meters / second``` so that dividing by the number of seconds between samples yields ```meters``` per ```second``` squared.

- As an example, acceleration from earth's gravity is 9.807 meters/second².

```python
SPEED_meter_per_second = (SPEED * kilomiter / hour) * ((1000 * meters) / kilometer) * (hour / (3600 * seconds))
SPEED_meter_per_second = SPEED * 1000/3600 * (meters / (second * second))
```

This sort of exercise may be needed for each column to ensure values are in the correct units.