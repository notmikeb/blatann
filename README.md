# Blatann

blåtann: Norwegian word for "blue tooth"

The goal of this library is to provide a high-level, object-oriented interface
for performing bluetooth operations using the Nordic nRF52 through Nordic's `pc-ble-driver-py` library
and the associated Connectivity firmware.

### Install

`pip install blatann`

#### Supported Devices/Software

This library has been tested using both the nRF52 Dev Kits, the nRF52840 USB Dongle and the [ABSniffer 528](https://blog.aprbrother.com/product/absniffer-usb-dongle-528) flashed with Connectivity Firmware

**Supported Versions:**

| Blatann Version | Python Version | SoftDevice Version | pc-ble-driver-py Version | Supported Devices                                                                                    |
|-----------------|----------------|--------------------|--------------------------|------------------------------------------------------------------------------------------------------|
| v0.2.x          | 2.7 Only       | v3                 | <=0.11.4                 | nRF52832 Dev Kit<br>ABSniffer BLE Dongle<br>nRF52840 Dev Kit/Dongle (using S132 connectivity image)* |
| v0.3+           | 3.7+           | v5                 | \>=0.12.0                | Same as above                                                                                        |

\* I have not personally tested the nRF52840 compatibility for v0.2.x, only heard second-hand accounts of it working. v0.3+ has been tested with the nRF52840 USB Dongle

When using the nRF52840, it should be flashed using the S132/SoftDevice v5 connectivity images. Both hex files and DFU packages are distributed by default
with v4.1.1 of [pc-ble-driver](https://github.com/NordicSemiconductor/pc-ble-driver/releases/tag/v4.1.1) and is also bundled with `pc-ble-driver-py` install, allowing the Dev Kit and USB Dongle to be flashed. The devices can be updated using [nRF Connect Desktop App](https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Connect-for-desktop)

### Roadmap

- [ ] Documentation
    - [ ] ReadTheDocs integration (started, needs refinement)
    - [ ] Better type hinting
- [ ] GAP
    - [X] BLE Enable parameters
    - [X] BLE Connection parameters (functional, needs some work)
    - [X] Advertising
    - [X] Data Length Extensions
    - [ ] Scanning (functional, needs some refactoring)
    - [ ] Documentation
- [ ] SMP
    - [X] Encryption/Authentication process
    - [X] MITM/Passcode pairing support
    - [X] Store bonding info
      - Currently uses pickle which is not secure
    - [X] Identity resolve
    - [X] Bonding as Peripheral
    - [ ] Bonding as Central (implemented, not tested)
    - [X] LESC pairing
    - [ ] Documentation
- [ ] GATT
    - [X] Configurable MTU
- [ ] GATT Server
    - [x] Characteristic Reads
    - [x] Characteristic Writes
    - [x] Notifications/Indications
    - [x] Long reads/writes
    - [ ] Characteristic User Description/Presentation format
    - [ ] CCCD Caching
    - [ ] Custom Read/Write authorization (#10)
    - [ ] Documentation (partial)
- [ ] GATT Client
    - [X] Database Discovery procedure
    - [X] Client reads
    - [X] Client writes
    - [X] Client long writes
    - [X] Notifications/Indications
    - [ ] CCCD Caching
    - [ ] Documentation
- [ ] Examples
    - [X] Advertiser/Broadcaster
    - [X] Scanner/Observer
    - [X] Central, Procedural
    - [X] Central, Event Driven
    - [ ] Central, Multiple Connections
    - [X] Peripheral
    - [ ] Multi-role
    - [X] Passcode Pairing
    - [X] LESC Numeric Comparison Pairing (glucose peripheral, no central example)
    - [X] Bonding (glucose peripheral, no central example)
- [ ] Bluetooth Services
    - [X] Device Info Service
    - [X] Battery Service
    - [ ] Current Time Service
       - [X] Peripheral
       - [ ] Central
    - [ ] Glucose Service
       - [X] Peripheral
       - [ ] Central (Incomplete, untested)
    - [X] Nordic UART Service
    - More TBD (or on request)
- [X] License
- [ ] Unit Tests
- [ ] Integration Tests
    - In progress. Advertising and Scanning mostly done


The library aims to support both event-driven and procedural program styles. It takes similar paradigms from C#/.NET's event function signatures,
where event handlers are passed  `object sender, EventArgs e` parameters.
Additionally, all asynchronous function calls return a `Waitable` object which can be waited on (with timeout)
until the event associated with the function call returns.

**NOTE**

This library is very much a work in progress. Interfaces, objects, method names **will** change.


### Examples

There are several example scripts which showcase different functionality of the library under `blatann/examples`.
Examples can be run using `python -m blatann.examples [example_filename] [device_comport]`.

Example usage: `python -m blatann.examples scanner COM3`

### Running Tests

The integrated tests can be ran using the builtin `unittest` runner and depends on a few environment variables to find the connected Nordic devices.

At a minimum, two nordic devices are required to run the unit tests. These are specified using environment variables:

- `BLATANN_DEV_1` - Serial port of the first Nordic device
- `BLATANN_DEV_2` - Serial port of the second Nordic device

Optionally a third `BLATANN_DEV_3` can be specified to run tests which require more than two devices. If this environment variable is not defined, tests which require 3 devices are skipped.

In order to speed up the tests, `BLATANN_TEST_QUICK=1` can be defined to skip long-running tests. Note that test cases which are defined as "long-running" is subjective and relative--the test suite will still take awhile to run (length TBD), but in general test cases which take longer than 20 seconds are skipped.

The tests can also be ran through the makefile using `make run-tests`.
