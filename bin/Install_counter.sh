#!/usr/bin/bash
# Install_counter.sh
#

export APP_HOME="/home/$(whoami)/telemetry-counter"
export APP_PYTHON="/home/$(whoami)/.local/bin/python3.11"
export DEBUG="True"

# Debugging support
if [ "${DEBUG}" = "True" ]
then
	# enable shell debug mode
	set -x
fi

cd ${APP_HOME}

if [ -d "${APP_HOME}/dist" ]
then
	rm -rf "${APP_HOME}/dist"
fi

${APP_PYTHON} -m build .
ls -l dist/*.whl
${APP_PYTHON} -m pip install --force-reinstall dist/*.whl


${APP_PYTHON} -m tcounter.boot_counter --help
${APP_PYTHON} -m tcounter.app_counter --help
