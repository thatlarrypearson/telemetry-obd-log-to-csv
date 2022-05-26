# UltraDict Installation

[UltraDict](https://github.com/ronny-rentner/UltraDict) is a new package that is currently under development.  The package provides a way for different running processes to share memory using the Python dictionary as both a storage metaphor and high level object interface definition.  That is, it works justs like a Python dictionary (```{}``` or ```dict()```).

While the ```UltraDict``` Python package is ```pip``` installable, as of today (May 25, 2022), there are some issues in the package version that causes the ```gps_logger.gps_logger``` and/or ```obd_logger.obd_logger``` processes to fail.

- [Unable to access UltraDict after a certain loop Limit, Issue occurs Only on Linux.............](https://github.com/ronny-rentner/UltraDict/issues/9)

The above issue and several others have been fixed in the [UltraDict](https://github.com/ronny-rentner/UltraDict) development branch.

## Install Dependencies

```bash
# UltraDict Dependencies
sudo apt-get install -y cmake
python3.10 -m pip install --user --upgrade pyrtcm
python3.3.10 -m pip install --user --upgrade atomics
```

## Install UltraDict

Here is how you access the development branch and install ```UltraDict``` on Linux.  I haven't taken the time to install on Windows (missing certain Microsoft development tools) and I'm not even trying to figure out what can be done on Macs.  These instructions assume that you have already downloaded Python 3.10 source code and then built and installed Python 3.10 from that code.  You need the development tools from that build.

```bash
$ cd
$ git clone https://github.com/ronny-rentner/UltraDict.git
$ cd UltraDict
$ git checkout dev
$ python3.10 -m build .
$ python3.10 -m pip install dist/UltraDict-0.0.4-cp310-cp310-linux_aarch64.whl
$
```

This build was done on a Raspberry Pi.  To build on a different architecture (like Intel X86), the ```pip install``` command's wheel (```dist/*.whl```) file name will need to be modified.
