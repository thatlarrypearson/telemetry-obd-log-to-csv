# telemetry-gps/gps_logger/gps_logger.py
"""
GPS Logger
"""
from argparse import ArgumentParser
import logging
from sys import stdout, stderr
from os import fsync
from datetime import datetime, timezone
import json

from pyubx2 import UBXReader

from .__init__ import __version__
from .gps_config import (
    parsed_data_to_dict,
    get_log_file_handle,
)
from .connection import (
    initialize_gps, dict_to_log_format,
)
from obd_logger.telemetry_common_functions import (
    default_shared_gps_command_list as SHARED_DICTIONARY_COMMAND_LIST,
    SharedDictionaryManager,
)

DEFAULT_SERIAL_DEVICE="/dev/ttyACM0"
TIMEOUT=1.0
MESSAGE_RATE=1

logger = logging.getLogger("gps_logger")

def argument_parsing()-> dict:
    """Argument parsing"""
    parser = ArgumentParser(description="Telemetry GPS Logger")
    parser.add_argument(
        "--shared_dictionary_name",
        default=None,
        help="Enable shared memory/dictionary using this name"
    )
    parser.add_argument(
        "--shared_dictionary_command_list",
        default=None,
        help="Comma separated list of NMEA commands/sentences to be shared (no spaces), defaults to all."
    )
    parser.add_argument(
        "--message_rate",
        default=MESSAGE_RATE,
        type=int,
        help=f"Number of whole seconds between each GPS fix.  Defaults to {MESSAGE_RATE}."
    )
    parser.add_argument(
        "--serial",
        default=DEFAULT_SERIAL_DEVICE,
        help=f"Full path to the serial device where the GPS can be found, defaults to {DEFAULT_SERIAL_DEVICE}"
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

def main():
    """Run main function."""

    args = argument_parsing()

    if args['version']:
        print(f"Version {__version__}", file=stdout)
        exit(0)

    verbose = args['verbose']
    serial_device = args['serial']
    shared_dictionary_name = args['shared_dictionary_name']
    shared_dictionary_command_list = args['shared_dictionary_command_list']
    message_rate = args['message_rate']

    logging_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(stream=stderr, level=logging_level)

    logging.debug(f"argument --verbose: {verbose}")

    log_file_handle = get_log_file_handle()
    logging.info(f"log file name: {log_file_handle.name}")

    if shared_dictionary_command_list:
        shared_dictionary_command_list = shared_dictionary_command_list.split(sep=',')
    else:
        shared_dictionary_command_list = SHARED_DICTIONARY_COMMAND_LIST

    if shared_dictionary_name:
        shared_dictionary = SharedDictionaryManager(shared_dictionary_name)
        logging.info(f"shared_dictionary_command_list {shared_dictionary_command_list}")
    else:
        shared_dictionary = None

    logging.info(f"shared_dictionary_name {shared_dictionary_name})")

    io_handle = initialize_gps(serial_device, message_rate)

    # reads NMEA, UBX and RTM input
    gps_reader = UBXReader(io_handle)

    iso_ts_pre = datetime.isoformat(datetime.now(tz=timezone.utc))

    for (raw_data, parsed_data) in gps_reader:
        data_dict = parsed_data_to_dict(parsed_data)

        logging.debug(f"GPS data {data_dict}\n")

        if 'umsg_name' in data_dict and data_dict['umsg_name'] == 'MON-VER':
            gps_software = data_dict
            logging.info(f"GPS SOFTWARE: {data_dict}")

        if 'umsg_name' in data_dict and data_dict['umsg_name'] == 'MON-HW':
            gps_hardware = data_dict
            logging.info(f"GPS HARDWARE: {data_dict}")

        if data_dict['Message_Type'] != "NMEA":
            "Skipping UBX and RTM messages"
            logging.debug(f"skipping Message_Type {data_dict['Message_Type']}")
            iso_ts_pre = datetime.isoformat(datetime.now(tz=timezone.utc))
            continue

        log_value = dict_to_log_format(data_dict)

        log_value['iso_ts_pre'] = iso_ts_pre
        log_value['iso_ts_post'] = datetime.isoformat(datetime.now(tz=timezone.utc))

        logging.debug(f"logging: {log_value}")

        if log_file_handle:
            log_file_handle.write(json.dumps(log_value) + "\n")
            log_file_handle.flush()
            fsync(log_file_handle.fileno())

        if shared_dictionary is not None and log_value["command_name"] in shared_dictionary_command_list:
                logging.debug( f"writing to shared dictionary {log_value['command_name']}")
                shared_dictionary[log_value['command_name']] = log_value

        iso_ts_pre = datetime.isoformat(datetime.now(tz=timezone.utc))

if __name__ == "__main__":
    main()
