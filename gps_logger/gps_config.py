# telemetry-gps/gps_logger/gps_config.py
"""
functions to set configuration on u-blox GPS devices
"""
import logging
from serial import Serial
from datetime import datetime, timezone
from pathlib import Path
from pyubx2 import UBX_MSGIDS, UBXMessage, UBXReader, SET, GET, POLL
import pyubx2.ubxtypes_core as ubt
from pynmeagps import NMEAReader
from pyubx2.ubxhelpers import gnss2str, val2bytes

logger = logging.getLogger("gps_logger")

INTERFACES = {
    'I2C': 0,
    'SERIAL': 1,
    'SERIAL_1': 1,
    'SERIAL_2': 2,
    'USB': 3,
    'SPI': 4,
    'Future Use': 5,
}

MESSAGE_OFF_LIST = [
    b"\xf0", b"\xf1",       # NMEA
    b"\x01",                # UBX NAV
    b"\x02",                # receiver management messages RXM
    b"\x0A",                # receiver management messages RXM
    b"\x21",                # device logging messages LOG
    # Informational messages work differently INF
]

MESSAGE_ON_LIST = [
#   b"\xf0\x09",            # GPS - GNSS Satellite Fault Detection
    b"\xf0\x0d",            # GNS - GNSS Fix Data
#   b"\xf0\x02",            # GSA - GNSS DOP and Active Satellites
    b"\xf0\x07",            # GST - GNSS Pseudo Range Error Statistics
#   b"\xf0\x03",            # GSV - GNSS Satellites in view
#   b"\xf0\x0e",            # THS - True heading and status
    b"\xf0\x05",            # VTG - Course over ground and groundspeed
    b"\xf0\x08",            # ZDA - Time and Date
]

def parsed_data_to_dict(parsed_data) -> dict:
    """
    convert parsed_data (NMEAMessage and UBXMessage) to dictionary
    """
    # 290         stg = f"<NMEA({self._talker}{self._msgID}"
    # 291         stg += ", "
    # 292         for i, att in enumerate(self.__dict__):
    # 293             if att[0] != "_":  # only show public attributes
    # 294                 val = self.__dict__[att]
    # 295                 stg += att + "=" + str(val)
    # 296                 if i < len(self.__dict__) - 1:
    # 297                     stg += ", "
    # 298         stg += ")>"
    # 299
    # 300         return stg
    if 'NMEAMessage' in str(type(parsed_data)):
        return_value = {
            "Message_Type": "NMEA",
            "talker_identifier": parsed_data._talker,
            "sentence_formatter": parsed_data._msgID,
        }
    elif 'UBXMessage' in str(type(parsed_data)):
        # logging.info(f"{parsed_data}")
        return_value = {
            "Message_Type": "UBX",
            "umsg_name": parsed_data.identity,
        }
        if parsed_data.payload is None:
            return return_value
        if parsed_data._ubxClass == b"\x05":
            # ACK-ACK or ACK-NAK
            clsID = None
            if "clsID" in parsed_data.__dict__:
                clsID = val2bytes(parsed_data.__dict__["clsID"], ubt.U1)
                return_value["clsID"] = ubt.UBX_CLASSES[clsID]
            if "msgID" in parsed_data.__dict__ and clsID:
                msgID = val2bytes(parsed_data.__dict__["msgID"], ubt.U1)
                return_value["msgID"] = ubt.UBX_MSGIDS[clsID + msgID]
    else:
        raise ValueError(f"Unknown parsed_data type {type(parsed_data)}")

    for parsed_data_attribute in parsed_data.__dict__:
        if not parsed_data_attribute.startswith('_'):
            if parsed_data_attribute.startswith("gnssId"):
                return_value[parsed_data_attribute] = gnss2str(parsed_data.__dict__[parsed_data_attribute])
            if type(parsed_data.__dict__[parsed_data_attribute]) == bytes:
                try:
                    return_value[parsed_data_attribute] = str(parsed_data.__dict__[parsed_data_attribute].rstrip(b"\x00"), "UTF-8")
                except Exception:
                    return_value[parsed_data_attribute] = str(parsed_data.__dict__[parsed_data_attribute].rstrip(b"\x00"))
            else:
                return_value[parsed_data_attribute] = str(parsed_data.__dict__[parsed_data_attribute])

    return return_value

def turn_off_message_on_all_interfaces(io_handle:Serial, message_type:str, message_rate:int):
    """
    Give messaging configuration commands to turn off all messages on all interfaces
    """
    logging.debug(f"message_type: {message_type}: turn_off_message_on_all_interfaces")

    # gps_reader = NMEAReader(io_handle, nmeaonly=False)

    message_class = int.from_bytes(message_type[:1], "little", signed=False)
    message_id = int.from_bytes(message_type[1:2], "little", signed=False)

    msg = UBXMessage("CFG", "CFG-MSG", SET, msgClass=message_class, msgID=message_id,
                        rateDDC=message_rate, rateUART1=message_rate, rateUSB=message_rate,
                        rateSPI=message_rate)

    io_handle.write(msg.serialize())

    # (raw_data, parsed_data) = gps_reader.read()

    # logging.debug(f"{message_type}: raw_data: {raw_data}")
    # logging.debug(f"{message_type}: parsed_data: {parsed_data}")

def turn_off_inf_messages(io_handle:Serial):
    """
    Using UBX, disable all informational (INF) messages
    """
    logging.debug("turn_off_inf_messages")

    # gps_reader = NMEAReader(io_handle, nmeaonly=False)

    for protocolID in (b"\x00", b"\x01"):   # UBX and NMEA protocols
        payload = protocolID + (3 * b"\x00") + (5 * b"\x01") + b"\x00"

        msg = UBXMessage("CFG", "CFG-INF", SET, payload=payload)

        io_handle.write(msg.serialize())

        # (raw_data, parsed_data) = gps_reader.read()

        # logging.debug(f"{protocolID}: raw_data: {raw_data}")
        # logging.debug(f"{protocolID}: parsed_data: {parsed_data}")

def turn_off_all_messages_on_all_interfaces(io_handle:Serial):
    """
    Using UBX, disable all messaging for all interfaces
    """
    logging.debug("turn_off_all_messages_on_all_interfaces")
    for message_type in UBX_MSGIDS:
        if message_type[:1] in MESSAGE_OFF_LIST:
                turn_off_message_on_all_interfaces(io_handle, message_type, 0)

    turn_off_inf_messages(io_handle)

def set_base_message_rate(io_handle:Serial, measRate=1000, navRate=5, timeRef=1):
    """
    Sets the amount of time that a message_rate of 1 takes and the number of navigation
    solutions that go into each message.
    """
    logging.debug("set_base_message_rate")

    # gps_reader = NMEAReader(io_handle, nmeaonly=False)

    payload = measRate.to_bytes(2, "little") + navRate.to_bytes(2, "little") + timeRef.to_bytes(2, "little")

    msg = UBXMessage("CFG", "CFG-RATE", SET, payload=payload)

    io_handle.write(msg.serialize())

    # (raw_data, parsed_data) = gps_reader.read()

    # logging.debug(f"raw_data: {raw_data}")
    # logging.debug(f"parsed_data: {parsed_data}")

def set_port_configuration(io_handle, portID=INTERFACES['USB']):
    """
    Sets serial (UART) and USB ports.  Defaults to USB port configuration.
    """
    logging.debug("set_port_configuration")

    # gps_reader = NMEAReader(io_handle, nmeaonly=False)

    if portID in (INTERFACES['SERIAL_1'], INTERFACES['SERIAL_2']):
        msg = UBXMessage("CFG", "CFG-PRT", SET,
                                        portID=0, reserved0=0, enable=0, pol=0, pin=0,
                                        thres=0, charLen=2, parity=0, nStopBits=0,
                                        baudRate=0, inUBX=1, inNMEA=1, inRTCM=1,
                                        inRTCM3=0, outUBX=1, outNMEA=1, outRTCM3=0,
                                        extendedTxTimeout=0, reserved1=0
        )

        io_handle.write(msg.serialize())

        # (raw_data, parsed_data) = gps_reader.read()

        # logging.debug(f"raw_data: {raw_data}")
        # logging.debug(f"parsed_data: {parsed_data}")

    elif portID == INTERFACES['USB']:
        return

    else:
        raise ValueError(f"portID {portID} not supported")

def turn_on_nmea_message(io_handle:Serial, message_type:bytes, message_rate:int):
    """
    Turn NMEA message on the current port

    message_rate == 0:  Disables message flow for message type "message_type"
    message_rate == 1:  Enables message flow for message type "message_type" at every smallest interval (highest rate)
    message_rate == n:  Enables message flow for message type "message_type" at every "n" times the smallest interval

    message_rate must be less than 256 and greater than or equal to 0
    """
    logging.debug(f"message_type: {message_type}: message_rate: {message_rate}: turn_on_nmea_message")

    # gps_reader = NMEAReader(io_handle, nmeaonly=False)

    payload = message_type + message_rate.to_bytes(1, "little")

    msg = UBXMessage("CFG", "CFG-MSG", SET, payload=payload)

    logging.debug(f"turn_on_nmea_message: {msg.serialize()}")

    io_handle.write(msg.serialize())

    # (raw_data, parsed_data) = gps_reader.read()

    # logging.debug(f"raw_data: {raw_data}")
    # logging.debug(f"parsed_data: {parsed_data}")

def turn_on_nmea_messages(io_handle:Serial, message_rate:int):
    """
    Turn on subset of NMEA messages on the current port

    message_rate == 0:  Disables message flow for message type "message_type"
    message_rate == 1:  Enables message flow for message type "message_type" at every smallest interval (highest rate)
    message_rate == n:  Enables message flow for message type "message_type" at every "n" times the smallest interval

    message_rate must be less than 256 and greater than or equal to 0
    """
    logging.debug("turn_on_nmea_messages")
    for message_type in MESSAGE_ON_LIST:
        turn_on_nmea_message(io_handle, message_type, message_rate)

def gps_software_version(io_handle:Serial):
    """
    return the GPS's software version information (MON-VER)
    """
    logging.debug("gps_software_version")

    msg = UBXMessage("MON", "MON-VER", POLL, payload=b"")

    io_handle.write(msg.serialize())


def gps_hardware_version(io_handle:Serial):
    """
    return the GPS's hardware version information (MON-HW)
    """
    logging.debug("gps_hardware_version")

    msg = UBXMessage("MON", "MON-HW", POLL, payload=b"")

    io_handle.write(msg.serialize())

def get_directory(base_path)->Path:
    """Generate directory where data files go."""
    path = Path(base_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_output_file_name(base_name)->Path:
    """Create an output file name."""
    dt_now = datetime.now(tz=timezone.utc).strftime("%Y%m%d%H%M%S")
    return Path(f"{base_name}-{dt_now}-utc.json")

def get_log_file_handle(base_path:str, base_name="NMEA"):
    """return a file handle opened for writing to a log file"""
    full_path = get_directory(base_path) / get_output_file_name(base_name)
    
    logger.info(f"log file full path: {full_path}")
    
    return open(full_path, mode='w', encoding='utf-8')

