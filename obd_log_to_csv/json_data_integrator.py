# telemetry-obd_log_to_csv/obd_log_to_csv/json_data_integrator.py
"""
JSON Data Integrator

Integrates telemetry JSON data from multiple sources into a single data file from
multiple data sources:
- telemetry_obd.obd_logger
- gps_logger.gps_logger
- wthr_logger.wthr_logger
- imu_logger.imu_logger
- other sources conforming to https://github.com/thatlarrypearson/telemetry-obd#telemetry-obd-logger-output-data-files

Directory Structure

DATA_PATH

- "telemetry-data"

BASE_PATH

- "~/<DATA_PATH>/data"
- "~/telemetry-data/data"

Where "~/" is the same as "${HOME}" or "<HOME>" or just the home directory.

JSON Data Directory

- "<HOME>/<DATA_PATH>/data/<HOSTNAME>"
- "~/<DATA_PATH>/data/<HOSTNAME>"
- "~/telemetry-data/data/<HOSTNAME>"
- "C:\Users\lbp/telemetry-data/data/telemetry2"

Where "<HOSTNAME>" is the hostname of the computer where the data was collected.

JSON Data File Names

Two different naming formats.

- "<HOSTNAME>-<boot_count>-<application_name>-<application_count>.json"
- "telemetry2-0000000072-gps-0000000113.json"
- "telemetry2-0000000072-gps-0000000114.json"
- "telemetry2-0000000072-imu-0000000078.json"
- "telemetry2-0000000072-wthr-0000000066.json"

Where "<application_name>" is one of "gps", "imu", "wthr", 

- "<HOSTNAME>-<boot_count>-<application_name>-<VIN>-<application_count>.json"
- "telemetry2-0000000072-obd-C4HJWCG5DL5214-0000000039.json"

Where "<VIN>" is the vehicle VIN as provided through the OBD interface and the "<application_name>" is "obd".

JSON Record Format

json_record = {
    "command_name": "WTHR_rapid_wind",
    "obd_response_value": {
        "time_epoch": 1705005028,
        "wind_speed": 5.49,
        "wind_direction": 3
    },
    "iso_ts_pre": "2024-01-12T15:29:28.675679+00:00",
    "iso_ts_post": "2024-01-12T15:29:30.944695+00:00"
}

Output Sort Order

When all three of the JSON record fields in two different records have the same values, then one of the records is a duplicate record.

- json_record["iso_ts_pre"]
- json_record["iso_ts_post"]
- json_record["command_name"]
"""
import json
from pathlib import Path
from argparse import ArgumentParser

from .__init__ import __version__
from tcounter.common import (
    BASE_PATH,
)

def write_json_data_to_integrated_file(records:list, base_path:str, hostname:str, boot_count:int, verbose=False):
    boot_count_string =  (f"{boot_count:10d}").replace(' ', '0')
    output_file_path = Path(f"{base_path}-{hostname}-{boot_count_string}-integrated.json")
    if verbose:
        print(f"writing integrated JSON data to {output_file_path.name}")

    with open(output_file_path, "w+", encoding='utf-8') as output_file:
        for record in records:
            output_file.write(json.dumps(record) + "\n")

    return output_file_path

def sort_key(json_data_record:dict):
    """
    - json_data_record["iso_ts_pre"]
    - json_data_record["iso_ts_post"]
    - json_data_record["command_name"]
    """
    return json_data_record["iso_ts_pre"] + json_data_record["iso_ts_post"] + json_data_record["command_name"]

def get_json_file_list(base_path:str, hostname:str, boot_count:int, verbose=False):
    """
    Return list of JSON data files matching the input parameters
    """
    file_list = []
    data_directory = f"{base_path}/{hostname}"
    for json_data_file_path in (Path(data_directory).glob(f"{hostname}*.json")):
        file_name_parts = json_data_file_path.name.split('-')
        if boot_count == int(file_name_parts[1]) and "integrated" not in json_data_file_path.name:
            if verbose:
                print(f"boot_count {boot_count} file {json_data_file_path.name}")
            file_list.append(json_data_file_path)
    return file_list

def command_line_options()->dict:
    parser = ArgumentParser(prog="json_data_integrator", description="Telemetry JSON Data Integrator")

    parser.add_argument(
        "--base_path",
        help=f"BASE_PATH directory variable.  Defaults to {BASE_PATH}",
        default=BASE_PATH,
    )

    parser.add_argument(
        "--hostname",
        help="The hostname of the computer where the data was collected.",
        required=True,
    )

    parser.add_argument(
        "--boot_count",
        help="""A counter used to identify the number of times the data collection computer booted since
        telemetry-counter was installed and configured.
        """,
        required=True,
        type=int,
    )

    parser.add_argument(
        "--version",
        help="Returns version and exit.",
        required=False,
    )

    parser.add_argument(
        "--verbose",
        help="Turn verbose output on. Default is off.",
        default=False,
        action='store_true'
    )

    return vars(parser.parse_args())

def main(args=None, base_path=BASE_PATH, hostname=None, boot_count=None, verbose=False):
    if args is not None:
        # Called from command line
        if args['version']:
            # return version and exit
            print(f"Version {__version__}")
            exit(0)

        base_path = args['base_path']
        hostname = args['hostname']
        boot_count = args['boot_count']
        verbose = args['verbose']

    elif hostname is None or boot_count is None:
        # External call to main, required args not provided.
        raise ValueError("boot_count and hostname must have valid values (can't be None)")

    if verbose:
        print(f"base_path {base_path}")
        print(f"hostname {hostname}")
        print(f"boot_count {boot_count}")

    for file in get_json_file_list(base_path, hostname, boot_count, verbose=verbose):
        sortable_list = []
        if verbose:
            print(f"file {file.name}")
        with open(file,  "r") as json_input:
            for line_number, json_record in enumerate(json_input, start=1):

                try:
                    input_record = json.loads(json_record)
                except json.decoder.JSONDecodeError as e:
                    # improperly closed JSON file
                    if verbose:
                        print(f"Corrupted JSON info {file.name} line {line_number}:\n{e}")
                    return

                sortable_list.append(input_record)

    # Sort using key "<iso_ts_pre><iso_ts_post><command_name>"
    if verbose:
        print(f"sorting {len(sortable_list)}")
    sortable_list.sort(key=sort_key)

    # Remove duplicate records
    if verbose:
        print(f"sorted list {len(sortable_list)} before un-duplicating")

    un_duplicate_list = {sort_key(record): record for record in sortable_list}
    un_duplicate_list = [record for k, record in un_duplicate_list.items()]

    if verbose:
        print(f"sorted list {len(un_duplicate_list)} after un-duplicating")

    # write sorted_list to file
    if verbose:
        print("writing sorted list")

    output_file_path = write_json_data_to_integrated_file(un_duplicate_list, base_path, hostname, boot_count, verbose=verbose)

    if verbose:
        print("un-duplicate sorted list written out to {output_file_path.name}")

    return

if __name__ == "__main__":
    args = command_line_options()
    main(args=args,)

