(venv) PS C:\Users\Rachid\Desktop\NR\Semestre 2026_1\extensao\ceres-diagnostico\firmware\esp32_mqtt_sensor> pio run --target upload            
Processing esp32-s3-devkitc-1 (platform: espressif32; board: esp32-s3-devkitc-1; framework: arduino)
-----------------------------------------------------------------------------------------------------------------------------------------------
Verbose mode can be enabled via `-v, --verbose` option
CONFIGURATION: https://docs.platformio.org/page/boards/espressif32/esp32-s3-devkitc-1.html
PLATFORM: Espressif 32 (7.0.0) > Espressif ESP32-S3-DevKitC-1-N8 (8 MB QD, No PSRAM)
HARDWARE: ESP32S3 240MHz, 320KB RAM, 8MB Flash
DEBUG: Current (esp-builtin) On-board (esp-builtin) External (cmsis-dap, esp-bridge, esp-prog, iot-bus-jtag, jlink, minimodule, olimex-arm-usb-ocd, olimex-arm-usb-ocd-h, olimex-arm-usb-tiny-h, olimex-jtag-tiny, tumpa)
PACKAGES: 
 - framework-arduinoespressif32 @ 3.20017.241212+sha.dcc1105b 
 - tool-esptoolpy @ 2.41100.0 (4.11.0) 
 - tool-mkfatfs @ 2.0.1 
 - tool-mklittlefs @ 1.203.210628 (2.3) 
 - tool-mkspiffs @ 2.230.0 (2.30) 
 - toolchain-riscv32-esp @ 8.4.0+2021r2-patch5 
 - toolchain-xtensa-esp32s3 @ 8.4.0+2021r2-patch5
LDF: Library Dependency Finder -> https://bit.ly/configure-pio-ldf
LDF Modes: Finder ~ chain, Compatibility ~ soft
Found 34 compatible libraries
Scanning dependencies...
Dependency Graph
|-- PubSubClient @ 2.8.0
|-- WiFi @ 2.0.0
Building in release mode
Compiling .pio\build\esp32-s3-devkitc-1\src\main.cpp.o
Building .pio\build\esp32-s3-devkitc-1\bootloader.bin
Generating partitions .pio\build\esp32-s3-devkitc-1\partitions.bin
esptool.py v4.11.0
Creating esp32s3 image...
Merged 1 ELF section
Successfully created esp32s3 image.
Compiling .pio\build\esp32-s3-devkitc-1\lib207\PubSubClient\PubSubClient.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFi.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiAP.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiClient.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiGeneric.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiMulti.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiSTA.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiScan.cpp.o
Archiving .pio\build\esp32-s3-devkitc-1\lib207\libPubSubClient.a
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiServer.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\lib390\WiFi\WiFiUdp.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\Esp.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\FirmwareMSC.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\FunctionalInterrupt.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\HWCDC.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\HardwareSerial.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\IPAddress.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\IPv6Address.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\MD5Builder.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\Print.cpp.o
Archiving .pio\build\esp32-s3-devkitc-1\lib390\libWiFi.a
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\Stream.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\StreamString.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\Tone.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\USB.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\USBCDC.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\USBMSC.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\WMath.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\WString.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\base64.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\cbuf.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-adc.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-bt.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-cpu.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-dac.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-gpio.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-i2c-slave.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-i2c.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-ledc.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-matrix.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-misc.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-psram.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-rgb-led.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-rmt.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-sigmadelta.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-spi.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-time.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-timer.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-tinyusb.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-touch.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\esp32-hal-uart.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\firmware_msc_fat.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\libb64\cdecode.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\libb64\cencode.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\main.cpp.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\stdlib_noniso.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\wiring_pulse.c.o
Compiling .pio\build\esp32-s3-devkitc-1\FrameworkArduino\wiring_shift.c.o
Archiving .pio\build\esp32-s3-devkitc-1\libFrameworkArduino.a
Linking .pio\build\esp32-s3-devkitc-1\firmware.elf
Retrieving maximum program size .pio\build\esp32-s3-devkitc-1\firmware.elf
Checking size .pio\build\esp32-s3-devkitc-1\firmware.elf
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [=         ]  13.5% (used 44312 bytes from 327680 bytes)
Flash: [==        ]  20.9% (used 697601 bytes from 3342336 bytes)
Building .pio\build\esp32-s3-devkitc-1\firmware.bin
esptool.py v4.11.0
Creating esp32s3 image...
Merged 2 ELF sections
Successfully created esp32s3 image.
Configuring upload protocol...
AVAILABLE: cmsis-dap, esp-bridge, esp-builtin, esp-prog, espota, esptool, iot-bus-jtag, jlink, minimodule, olimex-arm-usb-ocd, olimex-arm-usb-ocd-h, olimex-arm-usb-tiny-h, olimex-jtag-tiny, tumpa
CURRENT: upload_protocol = esptool
Looking for upload port...
Using manually specified: COM5
Uploading .pio\build\esp32-s3-devkitc-1\firmware.bin
esptool.py v4.11.0
Serial port COM5
Connecting...
Chip is ESP32-S3 (QFN56) (revision v0.2)
Features: WiFi, BLE, Embedded PSRAM 8MB (AP_3v3)
Crystal is 40MHz
MAC: cc:ba:97:16:c7:b4
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Flash will be erased from 0x00000000 to 0x00003fff...
Flash will be erased from 0x00008000 to 0x00008fff...
Flash will be erased from 0x0000e000 to 0x0000ffff...
Flash will be erased from 0x00010000 to 0x000bafff...
SHA digest in image updated
Compressed 15104 bytes to 10430...
Writing at 0x00000000... (100 %)
Wrote 15104 bytes (10430 compressed) at 0x00000000 in 0.6 seconds (effective 187.7 kbit/s)...
Hash of data verified.
Compressed 3072 bytes to 146...
Writing at 0x00008000... (100 %)
Wrote 3072 bytes (146 compressed) at 0x00008000 in 0.1 seconds (effective 241.4 kbit/s)...
Hash of data verified.
Compressed 8192 bytes to 47...
Writing at 0x0000e000... (100 %)
Wrote 8192 bytes (47 compressed) at 0x0000e000 in 0.2 seconds (effective 336.0 kbit/s)...
Hash of data verified.
Compressed 697968 bytes to 458002...
Writing at 0x00010000... (3 %)
Writing at 0x0001c171... (7 %)
Writing at 0x00027932... (10 %)
Writing at 0x00031056... (14 %)
Writing at 0x0003680d... (17 %)
Writing at 0x0003c0cf... (21 %)
Writing at 0x00041749... (25 %)
Writing at 0x00046954... (28 %)
Writing at 0x0004bac9... (32 %)
Writing at 0x00050917... (35 %)
Writing at 0x00055864... (39 %)
Writing at 0x0005a6d2... (42 %)
Writing at 0x0005f79a... (46 %)
Writing at 0x00064955... (50 %)
Writing at 0x00069bdf... (53 %)
Writing at 0x0006f8bd... (57 %)
Writing at 0x00074697... (60 %)
Writing at 0x00079655... (64 %)
Writing at 0x0007e6d2... (67 %)
Writing at 0x00083b1d... (71 %)
Writing at 0x00088e54... (75 %)
Writing at 0x0008e5a3... (78 %)
Writing at 0x0009409c... (82 %)
Writing at 0x000996da... (85 %)
Writing at 0x000a1cd2... (89 %)
Writing at 0x000a9ef0... (92 %)
Writing at 0x000af22b... (96 %)
Writing at 0x000b4b8f... (100 %)
Wrote 697968 bytes (458002 compressed) at 0x00010000 in 10.6 seconds (effective 525.5 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
======================================================== [SUCCESS] Took 38.34 seconds ========================================================
(venv) PS C:\Users\Rachid\Desktop\NR\Semestre 2026_1\extensao\ceres-diagnostico\firmware\esp32_mqtt_sensor> pio device monitor
--- Terminal on COM5 | 115200 8-N-1
--- Available filters and text transformations: debug, default, direct, esp32_exception_decoder, hexlify, log2file, nocontrol, printable, send_on_enter, time
--- More details at https://bit.ly/pio-monitor-filters
--- Quit: Ctrl+C | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H
falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s
Conectando MQTT...falhou rc=-2 — tentando em 5s