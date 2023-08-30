# UltraDict Installation

[UltraDict](https://github.com/ronny-rentner/UltraDict) is a new package that is currently under development.  The package provides a way for different running processes to share memory using the Python dictionary as both a storage metaphor and high level object interface definition.  That is, it works justs like a Python dictionary (```{}``` or ```dict()```).

The ```UltraDict``` Python package is ```pip``` installable and plays well with ```gps_logger.gps_logger``` and ```obd_logger.obd_logger``` processes when all of the dependencies are met.  One dependency, ```pymutex``` is not ```pip``` installable and needs to be **manually** installed.  Basically, ```pymutex``` requires a hack.

## Install Dependencies

```bash
# UltraDict Documented Dependencies
sudo apt-get install -y cmake
python3.10 -m pip install --user --upgrade pyrtcm
python3.10 -m pip install --user --upgrade atomics

# Get the source code for pymutex, the undocumented dependency
cd
git clone https://github.com/HMaker/pymutex.git

# Find the site package location for UltraDict
python3.10 -m pip show UltraDict | grep Location
Location: /home/human/.local/lib/python3.10/site-packages

# Move a portion of the pymutex software into the site packages location
mv pymutex/pymutex /home/human/.local/lib/python3.10/site-packages
```

## Install UltraDict

Here is how you access the development branch and install ```UltraDict``` on Linux.  I haven't taken the time to install on Windows (missing certain Microsoft development tools) and I'm not even trying to figure out what can be done on Macs.  These instructions assume that you have already downloaded Python 3.10 source code and then built and installed Python 3.10 from that code.  You need the development tools from that build.

The following assumes that the current version is ```0.0.6```.

```bash
python3.10 -m pip install --user --upgrade UltraDict
```

This build will take some time on a Raspberry Pi.  Different architectures (like Intel X86), and operating systems (like Windows, Linux, Mac) may already have binaries included in the PyPi package.
