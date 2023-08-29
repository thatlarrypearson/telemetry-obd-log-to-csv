#!/usr/bin/bash
# gps_logger.sh
#
# Runs GPS Logger

# Sometimes it takes 30 seconds before the OS gets the time correct.
export START_DELAY
sleep ${START_DELAY}

# Need time for GPS interface recover after failure
export RESTART_DELAY=10

export APP_HOME="/home/$(whoami)/telemetry-gps"
export APP_TMP_DIR="${APP_HOME}/tmp"
export APP_BASE_PATH="${APP_HOME}/data"
export APP_LOG_FILE="telemetry-$(date '+%Y-%m-%d %H_%M_%S').log"
export APP_PYTHON=python3.10
export DEBUG="True"
export SHARED_DICTIONARY_NAME="GPS"

# Debugging support
if [ "${DEBUG}" == "True" ]
then
	# enable shell debug mode
	set -x
fi

if [ ! -d "${APP_TMP_DIR}" ]
then
	mkdir --parents "${APP_TMP_DIR}"
fi

# turn off stdin
0<&-

# redirect all stdout and stderr to file
exec &>> "${APP_TMP_DIR}/${APP_LOG_FILE}"

date '+%Y/%m/%d %H:%M:%S'

if [ ! -d "${APP_BASE_PATH}" ]
then
	mkdir --parents "${APP_BASE_PATH}"
fi

cd "${APP_HOME}"

while date '+%Y/%m/%d %H:%M:%S'
do
	${APP_PYTHON} -m gps_logger.gps_logger \
        --shared_dictionary_name "${SHARED_DICTIONARY_NAME}" \
        --log_file_directory "${APP_BASE_PATH}"

	export RtnVal="$?"
	echo gps_logger returns "${RtnVal}"
	date '+%Y/%m/%d %H:%M:%S'

	sleep "${RESTART_DELAY}"
done
