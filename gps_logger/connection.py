# telemetry-gps/gps_logger/connection.py
"""
Manage gps connections through serial interfaces.
"""
from serial import Serial
import logging
from UltraDict import UltraDict
from .gps_config import (
    turn_off_all_messages_on_all_interfaces, turn_on_nmea_messages,
    set_base_message_rate, set_port_configuration, parsed_data_to_dict,
    gps_software_version, gps_hardware_version,
    logger, INTERFACES
)

SHARED_DICTIONARY_COMMAND_LIST = [
    "NMEA_GNGNS",       # Fix data
    "NMEA_GNGST",       # Pseudorange error statistics
    "NMEA_GNVTG",       # Course over ground and ground speed
    "NMEA_GNZDA",       # Time and data
]

def connect_to_gps(device_path:str, **kwargs)->Serial:
    """
    Open USB/UART/Serial GPS and return serial IO handle
    """
    logging.debug("open GPS serial port {device_path}")
    return Serial(port=device_path, **kwargs)

def initialize_gps(device_path:str, message_rate:int, **kwargs)->Serial:
    """
    Initializes GPS for delivering stream of NMEA messages over interface
    """
    logging.debug("initializing GPS at {device_path}")
    io_handle = connect_to_gps(device_path, **kwargs)

    set_port_configuration(io_handle, INTERFACES["USB"])

    set_base_message_rate(io_handle)

    turn_off_all_messages_on_all_interfaces(io_handle)

    gps_software_version(io_handle)
    gps_hardware_version(io_handle)

    turn_on_nmea_messages(io_handle, message_rate)

    return io_handle

def dict_to_log_format(data_dict:dict)->dict:
    """
    Converts .gps_config.parsed_data_to_dict() output to obd-logger output format:
    {
        'command_name': "name identifier",
        'obd_response_value': "result of said command",
        'iso_ts_pre': "ISO format Linux time before running said command",
        'iso_ts_post': "ISO format Linux time after running said command",
    }
    """
    log_value = {
        "command_name": f"NMEA_{data_dict['talker_identifier']}{data_dict['sentence_formatter']}",
        "obd_response_value": {},
    }

    for key, value in data_dict.items():
        # filter out "command_name" values
        if key in ("Message_Type", "talker_identifier", "sentence_formatter"):
            continue
        if type(value) == str and not len(value):
            # make empty strings into None
            value = None
        log_value["obd_response_value"][key] = value

    return log_value

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
