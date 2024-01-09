# Witty Pi 4 Telemetry Support Programs

UUGear's [Witty Pi 4 Realtime Clock and Power Management HAT](https://www.uugear.com/product/witty-pi-4/) for Raspberry Pi 4B is provided with configuration software to

* synchronize Real Time Clock (RTC) with Network Time
* set recovery voltage threshold

These functions must be present after the network is initialized and before other telemetry apps start.

Linux ```bash``` shell programs included in this repo provide the necessary instructions to perform Witty Pi 4 Configuration.

## **UNDER CONSTRUCTION**

## Installation

### Install Witty Pi 4

Follow the software installation instructions found in the [Witty Pi 4 User Manual](https://www.uugear.com/doc/WittyPi4_UserManual.pdf) before continuing.

### Download Repo

```bash
cd
git clone https://github.com/thatlarrypearson/telemetry-WittyPi4.git
```

### Customize

Edit ```telemetry-WittyPi4/root/bin/telemetry.rc.local.wittypi4```

* Change ```export WITTYPI4_USER="lbp"``` to ```export WITTYPI4_USER="```**<your-**```user-name```**-goes-here>**```"```.

The current ```user-name``` is displayed by the ```whoami``` command.

```bash
lbp@telemetry2:~ $ whoami
lbp
lbp@telemetry2:~ $
```

### Finish Install

```bash
cd
cd telemetry-WittyPi4
chmod 0755 bin/boot_config.sh
sudo mkdir  /root/bin
sudo cp root/bin/telemetry.rc.local.wittypi4.sh /root/bin/
sudo chown root /root/bin/telemetry.rc.local.wittypi4
sudo chmod 0755 /root/bin/telemetry.rc.local.wittypi4
```

### Test Install

```bash
sudo bash /root/bin/telemetry.rc.local.wittypi4
```

Test results are in the last ```wittypi4``` log file in ```/root/tmp/```.   ```ls -tr telemetry-wittypi4_*``` returns a matching file list in reverse date order.  That is, the newest file is last in the list.  ```tail -n 1```  prints the last line.   ```cat``` prints out a file.

```bash
sudo -i
cat $(ls -tr /root/tmp/telemetry-wittypi4_* | tail -n 1)
```

Example:

```bash
```

## License

[MIT](LICENSE.md)
