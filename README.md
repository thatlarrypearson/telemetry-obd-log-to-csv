# telemetry-gps - Telemetry GPS Location and Time Logger

## Motivation

## Features

## Usage

## Installation

### Dependencies

Follow installation instructions for the following:

* [PyGPSClient](docs/PyGPSClient.md) - install this first
* [Telemetry OBD Logging](https://github.com/thatlarrypearson/telemetry-obd) - install this second

Installation instructions for following are below:

* [pyubx2](https://github.com/semuconsulting/pyubx2)
* [pynmeagps](https://github.com/semuconsulting/pynmeagps)
* [UltraDict](https://github.com/ronny-rentner/UltraDict)

```bash
# UltraDict Dependencies
sudo apt-get install -y cmake
python3.8 -m pip install --user --upgrade pyrtcm
python3.8 -m pip install --user --upgrade atomics

# UltraDict
git clone https://github.com/ronny-rentner/UltraDict.git
cd UltraDict
python3.8 -m build
python3.8 -m pip install --user dist/...........

# UBX and NMEA Libraries
python3.8 -m pip install --user --upgrade pyubx2 pynmeagps

# Atomics
python3.8 -m pip install --user --upgrade atomics
```

## Examples

## Known Problems

## Related

## License

[MIT](LICENSE)
