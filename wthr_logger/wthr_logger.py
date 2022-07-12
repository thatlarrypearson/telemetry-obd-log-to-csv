# telemetry-wthr/wthr_logger/wthr_logger.py
"""
Weather Logger
"""
from argparse import ArgumentParser
import logging
from sys import stdout, stderr
from datetime import datetime, timezone
from os import fsync
from pathlib import Path
from datetime import datetime, timezone
from os import fsync
import json
from .__init__ import __version__
from .udp import WeatherReports, WEATHER_REPORT_EXCLUDE_LIST

logger = logging.getLogger("wthr_logger")

SHARED_DICTIONARY_COMMAND_LIST = [
    "WTHR_rapid_wind",          # Rapid Wind
    "WTHR_hub_status",          # Hub Status
    "WTHR_device_status",       # Time and data
    "WTHR_obs_st",              # Tempest Observation
    "WTHR_evt_strike",          # Lightning Strike Event
]

def argument_parsing()-> dict:
    """Argument parsing"""
    parser = ArgumentParser(description="Telemetry Weather Logger")
    parser.add_argument(
        "--log_file_directory",
        default=None,
        help="Enable logging and place log files into this directory"
    )
    parser.add_argument(
        "--shared_dictionary_name",
        default=None,
        help="Enable shared memory/dictionary using this name"
    )
    parser.add_argument(
        "--shared_dictionary_command_list",
        default=None,
        help="Comma separated list of WeatherFlow Tempest message types to be shared (no spaces), defaults to all."
    )
    parser.add_argument(
        "--verbose",
        default=False,
        action='store_true',
        help="Turn DEBUG logging on. Default is off."
    )
    parser.add_argument(
        "--version",
        default=False,
        action='store_true',
        help="Print version number and exit."
    )
    return vars(parser.parse_args())

try:
    # Not making UltraDict a requirement.
    from UltraDict import UltraDict

    class SharedDictionaryManager(UltraDict):
        """
        Shared Dictionary Manager - Uses a dictionary as the shared memory metaphor.
        Supports multiple instances within single process so long as 'name'
        is distinct for each instance.  This is not enforced as this class doesn't
        use the singleton pattern.

        Different processes can share the same shared memory/dictionary so long as they use the
        same value for the 'name' constructor variable.

        Code assumes there is only one writer and one or more readers for each memory region.  If more
        more than one writer is needed, create multiple instances, one for each writer.
        """
        # UltraDict(*arg, name=None, buffer_size=10000, serializer=pickle, shared_lock=False, full_dump_size=None, auto_unlink=True, recurse=False, **kwargs)

        def __init__(self, name:str):
            """
            SharedDictionaryManager constructor
            arguments
                name
                    name of the shared memory/dictionary region
            """
            super().__init__(
                name=name,
                buffer_size=1048576,    # 1 MB
                shared_lock=False,      # assume only one writer to shared memory/dictionary
                full_dump_size=None,    # change this value for Windows machines
                auto_unlink=False,      # once created, shared memory/dictionary persists on process exit
                recurse=False           # dictionary can contain dictionaries but updates not nested
            )

except ImportError:

    def SharedDictionaryManager(name:str) -> dict:
        """
        Fake class replacement.
        """
        logger.error(f"import error: Shared Dictionary ({name}) feature unsupported: UltraDict Not installed. ")
        return dict()

def dict_to_log_format(weather_report:dict) -> dict:
    """
    Converts weather report output to obd-logger output format:
    {
        'command_name': "name identifier",
        'obd_response_value': "result of said command",
        'iso_ts_pre': "ISO format Linux time before running said command",
        'iso_ts_post': "ISO format Linux time after running said command",
    }
    """
    command_name = weather_report['type']

    obd_response_value = {
        "command_name": f"WTHR_{command_name}",
        "obd_response_value": {},
    }

    for key, value in weather_report.items():
        # filter out "command_name", and serial number values
        if key in ("type", "message_type", "serial_number", "hub_sn"):
            continue
        if type(value) == str and not len(value):
            # make empty strings into None
            value = None
        obd_response_value["obd_response_value"][key] = value

    return obd_response_value

def get_directory(base_path) -> Path:
    """Generate directory where data files go."""
    path = Path(base_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_output_file_name(base_name) -> Path:
    """Create an output file name."""
    dt_now = datetime.now(tz=timezone.utc).strftime("%Y%m%d%H%M%S")
    return Path(f"{base_name}-{dt_now}-utc.json")

def get_log_file_handle(base_path:str, base_name="WTHR"):
    """return a file handle opened for writing to a log file"""
    full_path = get_directory(base_path) / get_output_file_name(base_name)
    
    logger.info(f"log file full path: {full_path}")
    
    return open(full_path, mode='w', encoding='utf-8')

def main():
    """Run main function."""

    args = argument_parsing()

    if args['version']:
        print(f"Version {__version__}", file=stdout)
        exit(0)

    verbose = args['verbose']
    log_file_directory = args['log_file_directory']
    shared_dictionary_name = args['shared_dictionary_name']
    shared_dictionary_command_list = args['shared_dictionary_command_list']

    logging_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(stream=stderr, level=logging_level)

    logger.debug(f"argument --verbose: {verbose}")

    if log_file_directory:
        logger.info(f"log_file_directory: {log_file_directory}")
        log_file_handle = get_log_file_handle(log_file_directory)
    else:
        log_file_handle = None

    if shared_dictionary_command_list:
        shared_dictionary_command_list = shared_dictionary_command_list.split(sep=',')
    else:
        shared_dictionary_command_list = SHARED_DICTIONARY_COMMAND_LIST

    if shared_dictionary_name:
        shared_dictionary = SharedDictionaryManager(shared_dictionary_name)
        logger.info(f"shared_dictionary_command_list {shared_dictionary_command_list}")
    else:
        shared_dictionary = None

    logger.info(f"shared_dictionary_name {shared_dictionary_name})")

    # reads Weather input
    weather_reports = WeatherReports(logger)

    iso_ts_pre = datetime.isoformat(datetime.now(tz=timezone.utc))

    for raw_weather_report, weather_report in weather_reports:
        if not weather_report:
            # skipping invalid (None value) data
            continue

        if weather_report['type'] in WEATHER_REPORT_EXCLUDE_LIST:
            # skipping unwanted weather report types
            logger.debug(f"skipping Message_Type {weather_report['type']}")
            iso_ts_pre = datetime.isoformat(datetime.now(tz=timezone.utc))
            continue

        log_value = dict_to_log_format(weather_report)

        log_value['iso_ts_pre'] = iso_ts_pre
        log_value['iso_ts_post'] = datetime.isoformat(datetime.now(tz=timezone.utc))

        logger.debug(f"logging: {log_value}")

        if log_file_handle:
            log_file_handle.write(json.dumps(log_value) + "\n")
            # want a command line option to enable forced buffer write to disk with default off
            # log_file_handle.flush()
            # fsync(log_file_handle.fileno())

        if shared_dictionary is not None and log_value["command_name"] in shared_dictionary_command_list:
                logger.debug( f"writing to shared dictionary {log_value['command_name']}")
                shared_dictionary[log_value['command_name']] = log_value

        iso_ts_pre = datetime.isoformat(datetime.now(tz=timezone.utc))

if __name__ == "__main__":
    main()
