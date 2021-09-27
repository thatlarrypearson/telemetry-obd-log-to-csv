
# Telemetry OBD Data To CSV File

[Telemetry OBD Logger](https://github.com/thatlarrypearson/telemetry-obd) output is converted into CSV format files suitable for importation into Python [Pandas](https://pandas.pydata.org/)  ```dataframe```s by the ```from_csv()``` method.

## Author

- [@thatlarrypearson](https://www.github.com/thatlarrypearson)

## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform

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
                        labelled items will be used. Defaults to all distinct command names
                        in the set of files.
  --csv CSV             CSV output file. File can be either a full or relative path name. If the file already exists,
                        it will be overwritten.
  --no_header           CSV output file will NOT have a column name header record. Default is False.
                        (That is, a header will be produced by default.)
  --verbose             Turn verbose output on. Default is off.
```

## Documentation

[Documentation](https://linktodocumentation)

## Related

Here are some related projects

[Awesome README](https://github.com/matiassingers/awesome-readme)

## Usage/Examples

```python
import Component from 'my-project'

function App() {
  return <Component />
}
```

## License

[MIT](./LICENSE.md)
