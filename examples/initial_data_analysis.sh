# telemetry-obd-log-to-csv/examples/initial_data_analysis.sh

if [ $# -lt 1 ]
then
    echo "$0: USAGE:"
    echo "$0 telemetry-obd-output-file_1.json [telemetry-obd-output-file_2.json ... telemetry-obd-output-file_n]"
    echo "$0 Environment Variables"
    echo "$0 CONFIG_FILE: configuration file used by telemetry_obd.obd_logger to collect data."
    exit 1
fi

if [ "${CONFIG_FILE}_nothing" == "_nothing" ]
then
    echo "$0: CONFIG_FILE enviornment variable missing."
    echo "$0 CONFIG_FILE: configuration file used by telemetry_obd.obd_logger to collect data."
    exit 2
fi

export LOG_TO_CSV_DIR="../telemetry-obd-log-to-csv"
export PYTHON3="python3.8"

${PYTHON3} "${LOG_TO_CSV_DIR}"/examples/load_config_file.py --housekeeping --cycle "${CONFIG_FILE}" > ida-cfg-file-$$.tmp
export Return_Value=$?

if [ ${Return_Value} -ne 0 ]
then
    echo Following Command Failed With Code: ${Return_Value}
    echo ${PYTHON3} "${LOG_TO_CSV_DIR}"/examples/load_config_file.py --housekeeping --cycle "${CONFIG_FILE}"
    exit 3
fi

${PYTHON3} -m obd_log_to_csv.obd_log_to_csv --csv initial_data_analysis.csv --commands $(cat ida-cfg-file-$$.tmp) ${*}
export Return_Value=$?

if [ ${Return_Value} -ne 0 ]
then
    echo Following Command Failed With Code: ${Return_Value}
    echo ${PYTHON3} -m obd_log_to_csv.obd_log_to_csv --csv initial_data_analysis.csv --commands $(cat ida-cfg-file-$$.tmp) ${*}
    exit 4
fi


if [ ! -d analysis ]
then
    mkdir --parents analysis
fi

${PYTHON3} "${LOG_TO_CSV_DIR}"/examples/initial_data_analysis.py initial_data_analysis.csv
export Return_Value=$?

if [ ${Return_Value} -ne 0 ]
then
    echo Following Command Failed With Code: ${Return_Value}
    echo ${PYTHON3} "${LOG_TO_CSV_DIR}"/examples/initial_data_analysis.py initial_data_analysis.csv
    exit 5
fi



rm ida-cfg-file-$$.tmp
