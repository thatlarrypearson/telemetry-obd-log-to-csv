# ```obd_log_evaluation``` of Frematics OBD-II Emulator Output


|command|mode|pid|count|no response|data type|units|
|---|---|---|---|---|---|---|
|ABSOLUTE_LOAD|0x01|0x43|27|0|float|percent|
|ACCELERATOR_POS_D|0x01|0x49|27|0|float|percent|
|ACCELERATOR_POS_E|0x01|0x4A|27|0|float|percent|
|ACCELERATOR_POS_F|0x01|0x4B|27|0|float|percent|
|AFTERTREATMENT_STATUS|0x01|0x8B|26|26|||
|AIR_STATUS|0x01|0x12|27|0|string||
|ALTERNATIVE_FUEL|0x01|0xAB|26|26|||
|AMBIANT_AIR_TEMP|0x01|0x46|27|0|integer|degC|
|AUXILIARY_IN_OUT_STATUS|0x01|0x65|27|27|||
|AUX_INPUT_STATUS|0x01|0x1E|27|0|integer||
|BAROMETRIC_PRESSURE|0x01|0x33|27|0|integer|kilopascal|
|BOOST_PRESSURE|0x01|0x70|27|27|||
|CACT|0x01|0x77|27|27|||
|CALIBRATION_ID|0x09|0x04|27|0|string||
|CALIBRATION_ID_MESSAGE_COUNT|0x09|0x03|27|0|integer|count|
|CATALYST_TEMP_B1S1|0x01|0x3C|27|0|float|degC|
|CATALYST_TEMP_B1S2|0x01|0x3E|27|0|float|degC|
|CATALYST_TEMP_B2S1|0x01|0x3D|27|0|float|degC|
|CATALYST_TEMP_B2S2|0x01|0x3F|27|0|float|degC|
|COMMANDED_DIESEL_AIR_INTAKE|0x01|0x6A|27|27|||
|COMMANDED_EGR|0x01|0x2C|27|0|float|percent|
|COMMANDED_EGR_2|0x01|0x69|27|27|||
|COMMANDED_EQUIV_RATIO|0x01|0x44|27|0|float|ratio|
|CONTROL_MODULE_VOLTAGE|0x01|0x42|27|0|float|volt|
|COOLANT_TEMP|0x01|0x05|27|0|integer|degC|
|CRANKCASE_VENTILATION|0x01|0xAD|26|26|||
|CVN|0x09|0x06|27|0|string||
|CVN_MESSAGE_COUNT|0x09|0x05|27|0|integer|count|
|CYLENDER_FUEL_RATE|0x01|0xA2|26|26|||
|DEF_DOSING|0x01|0xA5|26|26|||
|DEF_SENSOR|0x01|0x9B|26|26|||
|DISTANCE_SINCE_DTC_CLEAR|0x01|0x31|27|0|float|kilometer|
|DISTANCE_W_MIL|0x01|0x21|27|0|float|kilometer|
|DPF_BANK_1|0x01|0x7A|27|27|||
|DPF_BANK_2|0x01|0x7B|27|27|||
|DPF_TEMP|0x01|0x7C|27|27|||
|ECU_NAME|0x09|0x0A|26|0|string||
|ECU_NAME_MESSAGE_COUNT|0x09|0x09|26|0|integer|count|
|EGR_AIR_FLOW|0x01|0xAF|26|26|||
|EGR_ERROR|0x01|0x2D|27|0|float|percent|
|EGR_TEMP|0x01|0x6B|27|27|||
|EGT_BANK_1_TEMP|0x01|0x78|27|27|||
|EGT_BANK_2_TEMP|0x01|0x79|27|27|||
|EMISSION_REQ|0x01|0x5F|27|27|||
|ENGINE_COOLANT_TEMPERATURE|0x01|0x67|27|27|||
|ENGINE_EXHAUST_FLOW_RATE|0x01|0x9E|26|26|||
|ENGINE_FRICTION_PERCENT_TORQUE|0x01|0x8E|26|26|||
|ENGINE_LOAD|0x01|0x04|27|0|float|percent|
|ENGINE_RUN_TIME|0x01|0x7F|27|27|||
|ENGINE_RUN_TIME_AECD_1|0x01|0x81|27|27|||
|ENGINE_RUN_TIME_AECD_2|0x01|0x82|27|27|||
|ENGINE_RUN_TIME_AECD_3|0x01|0x89|26|26|||
|ENGINE_RUN_TIME_AECD_4|0x01|0x8A|26|26|||
|ESN|0x09|0x0D|26|26|||
|ESN_COUNT|0x09|0x0C|26|26|||
|ETHANOL_PERCENT|0x01|0x52|27|0|float|percent|
|EVAPORATIVE_PURGE|0x01|0x2E|27|0|float|percent|
|EVAP_PURGE_PRESSURE|0x01|0xAE|26|26|||
|EVAP_SYS_VAPOR_PRESSURE|0x01|0xA3|26|26|||
|EVAP_VAPOR_PRESSURE|0x01|0x32|27|0|float|pascal|
|EVAP_VAPOR_PRESSURE_ABS|0x01|0x53|27|0|float|kilopascal|
|EVAP_VAPOR_PRESSURE_ALT|0x01|0x54|27|0|integer|pascal|
|EXHAUST_GAS_TEMP_BANK_1|0x01|0x98|26|26|||
|EXHAUST_GAS_TEMP_BANK_2|0x01|0x99|26|26|||
|EXHAUST_PRESSURE|0x01|0x73|27|27|||
|FREEZE_DTC|0x01|0x02|27|0|list||
|FREEZE_DTC-00|0x01|0x02|27|0|string||
|FREEZE_DTC-01|0x01|0x02|27|0|string||
|FUEL_INJECT_TIMING|0x01|0x5D|27|0|float|degree|
|FUEL_LEVEL|0x01|0x2F|27|0|float|percent|
|FUEL_PRESSURE|0x01|0x0A|27|0|integer|kilopascal|
|FUEL_PRESSURE_CONTROL|0x01|0x6D|27|27|||
|FUEL_RAIL_PRESSURE_ABS|0x01|0x59|27|0|float|kilopascal|
|FUEL_RAIL_PRESSURE_DIRECT|0x01|0x23|27|0|float|kilopascal|
|FUEL_RAIL_PRESSURE_VAC|0x01|0x22|27|0|float|kilopascal|
|FUEL_RATE|0x01|0x5E|27|0|float|lph|
|FUEL_RATE_2|0x01|0x9D|26|26|||
|FUEL_STATUS|0x01|0x03|27|27|||
|FUEL_SYSTEM|0x01|0x9F|26|26|||
|FUEL_SYSTEM_STATUS|0x01|0x92|26|26|||
|FUEL_TYPE|0x01|0x51|27|0|string||
|HYBRID_BATTERY_REMAINING|0x01|0x5B|27|0|float|percent|
|HYBRID_EV_DATA|0x01|0x9A|26|26|||
|HYDROCARBON_DOSER|0x01|0x96|26|26|||
|INJECTION_PRESSURE_CONTROL|0x01|0x6E|27|27|||
|INTAKE_AIR_TEMPERATURE_SENSOR|0x01|0x68|27|27|||
|INTAKE_MANIFOLD_PRESSURE|0x01|0x87|26|26|||
|INTAKE_PRESSURE|0x01|0x0B|27|0|integer|kilopascal|
|INTAKE_TEMP|0x01|0x0F|27|0|integer|degC|
|LONG_FUEL_TRIM_1|0x01|0x07|27|0|float|percent|
|LONG_FUEL_TRIM_2|0x01|0x09|27|0|float|percent|
|LONG_O2_TRIM_B1|0x01|0x56|27|0|float|percent|
|LONG_O2_TRIM_B2|0x01|0x58|27|0|float|percent|
|MAF|0x01|0x10|27|0|float|gps|
|MANIFOLD_TEMP|0x01|0x84|26|26|||
|MASS_AIR_FLOW_SENSOR|0x01|0x66|27|27|||
|MAX_DEF_RATE|0x01|0xAC|26|26|||
|MAX_MAF|0x01|0x50|27|0|integer|gps|
|MAX_VALUES|0x01|0x4F|27|27|||
|MOTORCYCLE_IO_STATUS|0x01|0xA9|26|26|||
|NOX_CONTROL_INFO|0x01|0x94|26|26|||
|NOX_EMISSION_RATE|0x01|0x97|26|26|||
|NOX_NTE_STATUS|0x01|0x7D|27|27|||
|NOX_SENSOR|0x01|0x83|26|26|||
|NOX_SENSOR_2|0x01|0xA7|26|26|||
|NOX_SENSOR_CORRECTED|0x01|0xA1|26|26|||
|NOX_SENSOR_CORRECTED_2|0x01|0xA8|26|26|||
|NOX_SYSTEM|0x01|0x85|26|26|||
|O2_B1S1|0x01|0x14|27|0|float|volt|
|O2_B1S2|0x01|0x15|27|0|float|volt|
|O2_B1S3|0x01|0x16|27|0|float|volt|
|O2_B1S4|0x01|0x17|27|0|float|volt|
|O2_B2S1|0x01|0x18|27|0|float|volt|
|O2_B2S2|0x01|0x19|27|0|float|volt|
|O2_B2S3|0x01|0x1A|27|0|float|volt|
|O2_B2S4|0x01|0x1B|27|0|float|volt|
|O2_S1_WR_CURRENT|0x01|0x34|27|0|float|milliampere|
|O2_S1_WR_VOLTAGE|0x01|0x24|27|0|float|volt|
|O2_S2_WR_CURRENT|0x01|0x35|27|0|float|milliampere|
|O2_S2_WR_VOLTAGE|0x01|0x25|27|0|float|volt|
|O2_S3_WR_CURRENT|0x01|0x36|27|0|float|milliampere|
|O2_S3_WR_VOLTAGE|0x01|0x26|27|0|float|volt|
|O2_S4_WR_CURRENT|0x01|0x37|27|0|float|milliampere|
|O2_S4_WR_VOLTAGE|0x01|0x27|27|0|float|volt|
|O2_S5_WR_CURRENT|0x01|0x38|27|0|float|milliampere|
|O2_S5_WR_VOLTAGE|0x01|0x28|27|0|float|volt|
|O2_S6_WR_CURRENT|0x01|0x39|27|0|float|milliampere|
|O2_S6_WR_VOLTAGE|0x01|0x29|27|0|float|volt|
|O2_S7_WR_CURRENT|0x01|0x3A|27|0|float|milliampere|
|O2_S7_WR_VOLTAGE|0x01|0x2A|27|0|float|volt|
|O2_S8_WR_CURRENT|0x01|0x3B|27|0|float|milliampere|
|O2_S8_WR_VOLTAGE|0x01|0x2B|27|0|float|volt|
|O2_SENSORS|0x01|0x13|27|0|list||
|O2_SENSORS-00|0x01|0x13|27|0|integer||
|O2_SENSORS-01|0x01|0x13|27|0|integer||
|O2_SENSORS-02|0x01|0x13|27|0|integer||
|O2_SENSORS-03|0x01|0x13|27|0|integer||
|O2_SENSORS-04|0x01|0x13|27|0|integer||
|O2_SENSORS-05|0x01|0x13|27|0|integer||
|O2_SENSORS-06|0x01|0x13|27|0|integer||
|O2_SENSORS-07|0x01|0x13|27|0|integer||
|O2_SENSORS_ALT|0x01|0x1D|27|0|list||
|O2_SENSORS_ALT-00|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-01|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-02|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-03|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-04|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-05|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-06|0x01|0x1D|27|0|integer||
|O2_SENSORS_ALT-07|0x01|0x1D|27|0|integer||
|O2_SENSOR_WIDE|0x01|0x8C|26|26|||
|O2_SENSOR_WIDE_RANGE|0x01|0x9C|26|26|||
|OBD_COMPLIANCE|0x01|0x1C|27|0|string||
|ODOMETER|0x01|0xA6|26|26|||
|OIL_TEMP|0x01|0x5C|27|0|integer|degC|
|PARTICULATE_MATTER|0x01|0x86|26|26|||
|PERCENT_TORQUE|0x01|0x64|27|0|list||
|PERCENT_TORQUE-Engine_Point_1|0x01|0x64|27|0|integer|percent|
|PERCENT_TORQUE-Engine_Point_2|0x01|0x64|27|0|integer|percent|
|PERCENT_TORQUE-Engine_Point_3|0x01|0x64|27|0|integer|percent|
|PERCENT_TORQUE-Engine_Point_4|0x01|0x64|27|0|integer|percent|
|PERCENT_TORQUE-Idle|0x01|0x64|27|0|integer|percent|
|PERF_TRACKING_COMPRESSION|0x09|0x0b|26|26|||
|PERF_TRACKING_MESSAGE_COUNT|0x09|0x07|26|0|integer|count|
|PERF_TRACKING_SPARK|0x09|0x08|26|0|string||
|PIDS_9A|0x09|0x00|27|0|list||
|PIDS_9A-00|0x09|0x00|27|0|integer||
|PIDS_9A-01|0x09|0x00|27|0|integer||
|PIDS_9A-02|0x09|0x00|27|0|integer||
|PIDS_9A-03|0x09|0x00|27|0|integer||
|PIDS_9A-04|0x09|0x00|27|0|integer||
|PIDS_9A-05|0x09|0x00|27|0|integer||
|PIDS_9A-06|0x09|0x00|27|0|integer||
|PIDS_9A-07|0x09|0x00|27|0|integer||
|PIDS_9A-08|0x09|0x00|27|0|integer||
|PIDS_9A-09|0x09|0x00|27|0|integer||
|PIDS_9A-10|0x09|0x00|27|0|integer||
|PIDS_9A-11|0x09|0x00|27|0|integer||
|PIDS_9A-12|0x09|0x00|27|0|integer||
|PIDS_9A-13|0x09|0x00|27|0|integer||
|PIDS_9A-14|0x09|0x00|27|0|integer||
|PIDS_9A-15|0x09|0x00|27|0|integer||
|PIDS_9A-16|0x09|0x00|27|0|integer||
|PIDS_9A-17|0x09|0x00|27|0|integer||
|PIDS_9A-18|0x09|0x00|27|0|integer||
|PIDS_9A-19|0x09|0x00|27|0|integer||
|PIDS_9A-20|0x09|0x00|27|0|integer||
|PIDS_9A-21|0x09|0x00|27|0|integer||
|PIDS_9A-22|0x09|0x00|27|0|integer||
|PIDS_9A-23|0x09|0x00|27|0|integer||
|PIDS_9A-24|0x09|0x00|27|0|integer||
|PIDS_9A-25|0x09|0x00|27|0|integer||
|PIDS_9A-26|0x09|0x00|27|0|integer||
|PIDS_9A-27|0x09|0x00|27|0|integer||
|PIDS_9A-28|0x09|0x00|27|0|integer||
|PIDS_9A-29|0x09|0x00|27|0|integer||
|PIDS_9A-30|0x09|0x00|27|0|integer||
|PIDS_9A-31|0x09|0x00|27|0|integer||
|PIDS_9A-32|0x09|0x00|27|0|integer||
|PIDS_9A-33|0x09|0x00|27|0|integer||
|PIDS_9A-34|0x09|0x00|27|0|integer||
|PIDS_9A-35|0x09|0x00|27|0|integer||
|PIDS_9A-36|0x09|0x00|27|0|integer||
|PIDS_9A-37|0x09|0x00|27|0|integer||
|PIDS_9A-38|0x09|0x00|27|0|integer||
|PIDS_9A-39|0x09|0x00|27|0|integer||
|PIDS_A|0x01|0x00|27|0|list||
|PIDS_A-00|0x01|0x00|27|0|integer||
|PIDS_A-01|0x01|0x00|27|0|integer||
|PIDS_A-02|0x01|0x00|27|0|integer||
|PIDS_A-03|0x01|0x00|27|0|integer||
|PIDS_A-04|0x01|0x00|27|0|integer||
|PIDS_A-05|0x01|0x00|27|0|integer||
|PIDS_A-06|0x01|0x00|27|0|integer||
|PIDS_A-07|0x01|0x00|27|0|integer||
|PIDS_A-08|0x01|0x00|27|0|integer||
|PIDS_A-09|0x01|0x00|27|0|integer||
|PIDS_A-10|0x01|0x00|27|0|integer||
|PIDS_A-11|0x01|0x00|27|0|integer||
|PIDS_A-12|0x01|0x00|27|0|integer||
|PIDS_A-13|0x01|0x00|27|0|integer||
|PIDS_A-14|0x01|0x00|27|0|integer||
|PIDS_A-15|0x01|0x00|27|0|integer||
|PIDS_A-16|0x01|0x00|27|0|integer||
|PIDS_A-17|0x01|0x00|27|0|integer||
|PIDS_A-18|0x01|0x00|27|0|integer||
|PIDS_A-19|0x01|0x00|27|0|integer||
|PIDS_A-20|0x01|0x00|27|0|integer||
|PIDS_A-21|0x01|0x00|27|0|integer||
|PIDS_A-22|0x01|0x00|27|0|integer||
|PIDS_A-23|0x01|0x00|27|0|integer||
|PIDS_A-24|0x01|0x00|27|0|integer||
|PIDS_A-25|0x01|0x00|27|0|integer||
|PIDS_A-26|0x01|0x00|27|0|integer||
|PIDS_A-27|0x01|0x00|27|0|integer||
|PIDS_A-28|0x01|0x00|27|0|integer||
|PIDS_A-29|0x01|0x00|27|0|integer||
|PIDS_A-30|0x01|0x00|27|0|integer||
|PIDS_A-31|0x01|0x00|27|0|integer||
|PIDS_B|0x01|0x20|27|0|list||
|PIDS_B-00|0x01|0x20|27|0|integer||
|PIDS_B-01|0x01|0x20|27|0|integer||
|PIDS_B-02|0x01|0x20|27|0|integer||
|PIDS_B-03|0x01|0x20|27|0|integer||
|PIDS_B-04|0x01|0x20|27|0|integer||
|PIDS_B-05|0x01|0x20|27|0|integer||
|PIDS_B-06|0x01|0x20|27|0|integer||
|PIDS_B-07|0x01|0x20|27|0|integer||
|PIDS_B-08|0x01|0x20|27|0|integer||
|PIDS_B-09|0x01|0x20|27|0|integer||
|PIDS_B-10|0x01|0x20|27|0|integer||
|PIDS_B-11|0x01|0x20|27|0|integer||
|PIDS_B-12|0x01|0x20|27|0|integer||
|PIDS_B-13|0x01|0x20|27|0|integer||
|PIDS_B-14|0x01|0x20|27|0|integer||
|PIDS_B-15|0x01|0x20|27|0|integer||
|PIDS_B-16|0x01|0x20|27|0|integer||
|PIDS_B-17|0x01|0x20|27|0|integer||
|PIDS_B-18|0x01|0x20|27|0|integer||
|PIDS_B-19|0x01|0x20|27|0|integer||
|PIDS_B-20|0x01|0x20|27|0|integer||
|PIDS_B-21|0x01|0x20|27|0|integer||
|PIDS_B-22|0x01|0x20|27|0|integer||
|PIDS_B-23|0x01|0x20|27|0|integer||
|PIDS_B-24|0x01|0x20|27|0|integer||
|PIDS_B-25|0x01|0x20|27|0|integer||
|PIDS_B-26|0x01|0x20|27|0|integer||
|PIDS_B-27|0x01|0x20|27|0|integer||
|PIDS_B-28|0x01|0x20|27|0|integer||
|PIDS_B-29|0x01|0x20|27|0|integer||
|PIDS_B-30|0x01|0x20|27|0|integer||
|PIDS_B-31|0x01|0x20|27|0|integer||
|PIDS_C|0x01|0x40|27|0|list||
|PIDS_C-00|0x01|0x40|27|0|integer||
|PIDS_C-01|0x01|0x40|27|0|integer||
|PIDS_C-02|0x01|0x40|27|0|integer||
|PIDS_C-03|0x01|0x40|27|0|integer||
|PIDS_C-04|0x01|0x40|27|0|integer||
|PIDS_C-05|0x01|0x40|27|0|integer||
|PIDS_C-06|0x01|0x40|27|0|integer||
|PIDS_C-07|0x01|0x40|27|0|integer||
|PIDS_C-08|0x01|0x40|27|0|integer||
|PIDS_C-09|0x01|0x40|27|0|integer||
|PIDS_C-10|0x01|0x40|27|0|integer||
|PIDS_C-11|0x01|0x40|27|0|integer||
|PIDS_C-12|0x01|0x40|27|0|integer||
|PIDS_C-13|0x01|0x40|27|0|integer||
|PIDS_C-14|0x01|0x40|27|0|integer||
|PIDS_C-15|0x01|0x40|27|0|integer||
|PIDS_C-16|0x01|0x40|27|0|integer||
|PIDS_C-17|0x01|0x40|27|0|integer||
|PIDS_C-18|0x01|0x40|27|0|integer||
|PIDS_C-19|0x01|0x40|27|0|integer||
|PIDS_C-20|0x01|0x40|27|0|integer||
|PIDS_C-21|0x01|0x40|27|0|integer||
|PIDS_C-22|0x01|0x40|27|0|integer||
|PIDS_C-23|0x01|0x40|27|0|integer||
|PIDS_C-24|0x01|0x40|27|0|integer||
|PIDS_C-25|0x01|0x40|27|0|integer||
|PIDS_C-26|0x01|0x40|27|0|integer||
|PIDS_C-27|0x01|0x40|27|0|integer||
|PIDS_C-28|0x01|0x40|27|0|integer||
|PIDS_C-29|0x01|0x40|27|0|integer||
|PIDS_C-30|0x01|0x40|27|0|integer||
|PIDS_C-31|0x01|0x40|27|0|integer||
|PIDS_D|0x01|0x60|27|0|list||
|PIDS_D-00|0x01|0x60|27|0|integer||
|PIDS_D-01|0x01|0x60|27|0|integer||
|PIDS_D-02|0x01|0x60|27|0|integer||
|PIDS_D-03|0x01|0x60|27|0|integer||
|PIDS_D-04|0x01|0x60|27|0|integer||
|PIDS_D-05|0x01|0x60|27|0|integer||
|PIDS_D-06|0x01|0x60|27|0|integer||
|PIDS_D-07|0x01|0x60|27|0|integer||
|PIDS_D-08|0x01|0x60|27|0|integer||
|PIDS_D-09|0x01|0x60|27|0|integer||
|PIDS_D-10|0x01|0x60|27|0|integer||
|PIDS_D-11|0x01|0x60|27|0|integer||
|PIDS_D-12|0x01|0x60|27|0|integer||
|PIDS_D-13|0x01|0x60|27|0|integer||
|PIDS_D-14|0x01|0x60|27|0|integer||
|PIDS_D-15|0x01|0x60|27|0|integer||
|PIDS_D-16|0x01|0x60|27|0|integer||
|PIDS_D-17|0x01|0x60|27|0|integer||
|PIDS_D-18|0x01|0x60|27|0|integer||
|PIDS_D-19|0x01|0x60|27|0|integer||
|PIDS_D-20|0x01|0x60|27|0|integer||
|PIDS_D-21|0x01|0x60|27|0|integer||
|PIDS_D-22|0x01|0x60|27|0|integer||
|PIDS_D-23|0x01|0x60|27|0|integer||
|PIDS_D-24|0x01|0x60|27|0|integer||
|PIDS_D-25|0x01|0x60|27|0|integer||
|PIDS_D-26|0x01|0x60|27|0|integer||
|PIDS_D-27|0x01|0x60|27|0|integer||
|PIDS_D-28|0x01|0x60|27|0|integer||
|PIDS_D-29|0x01|0x60|27|0|integer||
|PIDS_D-30|0x01|0x60|27|0|integer||
|PIDS_D-31|0x01|0x60|27|0|integer||
|PIDS_E|0x01|0x80|27|27|||
|PIDS_F|0x01|0xA0|26|26|||
|PIDS_G|0x01|0xC0|26|26|||
|PM_NTE_STATUS|0x01|0x7E|27|27|||
|PM_SENSOR_OUTPUT|0x01|0x8F|26|26|||
|REFERENCE_TORQUE|0x01|0x63|27|0|float|meter|
|RELATIVE_ACCEL_POS|0x01|0x5A|27|0|float|percent|
|RELATIVE_THROTTLE_POS|0x01|0x45|27|0|float|percent|
|RPM|0x01|0x0C|27|0|float|revolutions_per_minute|
|RUN_TIME|0x01|0x1F|27|0|float|second|
|RUN_TIME_MIL|0x01|0x4D|27|0|float|minute|
|SCR_CATALYST_STORAGE|0x01|0x95|26|26|||
|SCR_INDUCEMENT_SYSTEM|0x01|0x88|26|26|||
|SHORT_FUEL_TRIM_1|0x01|0x06|27|0|float|percent|
|SHORT_FUEL_TRIM_2|0x01|0x08|27|0|float|percent|
|SHORT_O2_TRIM_B1|0x01|0x55|27|0|float|percent|
|SHORT_O2_TRIM_B2|0x01|0x57|27|0|float|percent|
|SPEED|0x01|0x0D|27|0|float|kph|
|SPEED_LIMITER|0x01|0xAA|26|26|||
|STATUS|0x01|0x01|27|0|list||
|STATUS-00|0x01|0x01|27|0|string||
|STATUS-01|0x01|0x01|27|0|string||
|STATUS-02|0x01|0x01|27|0|string||
|STATUS_DRIVE_CYCLE|0x01|0x41|27|0|list||
|STATUS_DRIVE_CYCLE-00|0x01|0x41|27|0|string||
|STATUS_DRIVE_CYCLE-01|0x01|0x41|27|0|string||
|STATUS_DRIVE_CYCLE-02|0x01|0x41|27|0|string||
|THROTTLE|0x01|0x6C|27|27|||
|THROTTLE_ACTUATOR|0x01|0x4C|27|0|float|percent|
|THROTTLE_POS|0x01|0x11|27|0|float|percent|
|THROTTLE_POSITION_G|0x01|0x8D|26|26|||
|THROTTLE_POS_B|0x01|0x47|27|0|float|percent|
|THROTTLE_POS_C|0x01|0x48|27|0|float|percent|
|TIME_SINCE_DTC_CLEARED|0x01|0x4E|27|0|float|minute|
|TIMING_ADVANCE|0x01|0x0E|27|0|float|degree|
|TORQUE|0x01|0x62|27|0|integer|percent|
|TORQUE_DEMAND|0x01|0x61|27|0|integer|percent|
|TRANSMISSION_ACTUAL_GEAR|0x01|0xA4|26|26|||
|TURBO_A_TEMP|0x01|0x75|27|27|||
|TURBO_B_TEMP|0x01|0x76|27|27|||
|TURBO_INLET_PRESSURE|0x01|0x6F|27|27|||
|TURBO_RPM|0x01|0x74|27|27|||
|VG_TURBO_CONTROL|0x01|0x71|27|27|||
|VIN|0x09|0x02|27|0|string||
|VIN_MESSAGE_COUNT|0x09|0x01|27|0|integer|count|
|WARMUPS_SINCE_DTC_CLEAR|0x01|0x30|27|0|float|count|
|WASTEGATE_CONTROL|0x01|0x72|27|27|||
|WWH_OBD_ECU_INFO|0x01|0x91|26|26|||
|WWH_OBD_SYSTEM_INFO|0x01|0x90|26|26|||
|WWH_OBD_VEHICLE_INFO|0x01|0x93|26|26|||





