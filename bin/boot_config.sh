#! /usr/bin/bash
# telemetry-WittyPi4/bin/boot_config.sh

export WittyPi4_DIR="/home/$(whoami)/wittypi"
export RecoveryVoltage="4.9"
source "${WittyPi4_DIR}/utilities.sh"

# 3. Synchronize with network time
if $(has_internet)
then
    net_to_system
    system_to_rtc
fi

# 8. Set recovery voltage threshold
set_recovery_voltage_threshold "${RecoveryVoltage}"

