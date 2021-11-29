# OBD Log Evaluation

A vehicle's ```obd_logger``` configuration file should not contain unrecognizable OBD commands.  The ```obd_log_evaluation``` tool identifies non-responsive OBD commands.  It also identifies intermittant OBD commands possibly indicating the need to increase ```--timeout``` with ```telemetry_obd.obd_command_tester``` and ```telemetry_obd.obd_logger``` programs.

- An intermittant OBD command sometimes returns a valid value and sometimes returns ```no response```.

## Features

- Identifies unsupported OBD commands
- Identifies intermittant OBD commands
- Provides basic data types for each column (string, integer, float, list)
- When available, provides units of measure for numeric columns
- OBD commands returning lists of values are handled as a collection of individual commands
  - When subfield names are available, command names are modified for each element in the list
    - The command name shown in the report output is hyphenated with the subfield name
  - When subfield names are not available, subfields are identified by their number in the list
    - The command name shown in the report output is hyphenated with the subfield position in the list
- See [Examples](#examples) for more

## Usage

```bash
python3.8 -m obd_log_to_csv.obd_log_evaluation --help
usage: obd_log_evaluation [-h] [--verbose] [--csv] files [files ...]

OBD Log Evaluation performs simple analysis on telemetry_obd.obd_logger and telemetry_obd.obd_command_tester output
files. The analysis is oriented toward validating obd_logger config files and providing units for each OBD command.

positional arguments:
  files       telemetry_obd generated data files separated by spaces. Data file names can include full or relative
              paths.

optional arguments:
  -h, --help  show this help message and exit
  --verbose   Turn verbose output on. Default is off.
  --csv       Output CSV on stdout. Default is to rich table print on stdout.
```

## Examples

### ```obd_log_evaluation``` Processing Sample Output From Frematics OBD-II Emulator

#### Input

- Sample input collected during testing.
- Collection program interrupted (```<CTRL-C>```) after 26 full test cycles.
- See [```telemetry_obd.obd_command_tester```](https://github.com/thatlarrypearson/telemetry-obd).

```python
# Command Tester Collection Program
python3.8 -m telemetry_obd.obd_command_tester --cycles 100
```

#### Output

- OBD log evaluation program run on collected input data.
- Output was in CSV format for importation into [Microsoft Visual Studio Code](https://code.visualstudio.com/).
- Output can be viewed in table format at [TESTVIN012345678](OBD_LOG_EVALUATION-FrematicsEmulatorOutout.md)

```python
python3.8 -m obd_log_to_csv.obd_log_evaluation --csv ./TESTVIN012345678-TEST-20211127145538.json
```

## Related

Here are some related projects

- [telemetry-obd](https://github.com/thatlarrypearson/telemetry-obd): Telemetry OBDII (Onboard Diagnostic Data 2) Logger
  - ```telemetry_obd.obd_logger```
  - ```telemetry_obd.obd_command_tester```
- [telemetry-django-obd](https://github.com/thatlarrypearson/telemetry-django-obd): Django database OBD/ECU data loader

## License

[MIT](../LICENSE.md)