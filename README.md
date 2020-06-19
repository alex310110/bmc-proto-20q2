# bmc-proto-20q2
A Python prototype to explain ideals on OpenBMC improvements

This is created to illustrate the ideas as a running demo described in
https://lists.ozlabs.org/pipermail/openbmc/2020-June/022066.html

## Feature Examples

### Automatic Downstream Resource Detection
BmcMain.__init__() in main.py

### Sensor Polling and Readings
BmcMain.sensor_console() in main.py

### Sysfs I2C Abstraction
i2c.py

### Topology Discovery Entry
downstream/some_tray.py

### Dynamic Hardware Topology Discovery
BoardExampleA.__init__() in downstream/board_example_a.py

### Sensor Aggregation
CardExampleG.update_sensors() in downstream/card_example_g.py

### Device Initialization
CardExampleG.__init__() and CardExampleG.on_host_event() in downstream/card_example_g.py

### Device Kernel Driver Calibration
XAM2730.get_reading() in downstream/device_xam2730.py for NDA device.
XAM2734.get_reading() in device_xam2734.py for public device available upstream.
