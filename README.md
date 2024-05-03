# SpaceY
---

### dependencys:
- sim micropython
- dht micropython
* ##### lora github
* ##### mpu github
* ##### bmp github

### Conections
- sim:
    - gnd-gnd
    - vcc-5v
    - miso-12
    - mosi-11
    - sck-10
    - cs-13
- lora:
    - gnd-gnd
    - vcc-3v3
    - tx-1
    - rx-0
    - m0-2
    - m1-3
- mpu 6050:
    - sda-4
    - scl-5
    - gnd-gnd
    - vin-3v3
- dht 11:
    - vin-3v3
    - gnd-gnd
    - data-5
- bmp 280:
    - gnd-gnd
    - sda-4
    - scl-5
    - vin-3v3
- bn 880:
    - gnd-gnd
    - vin-3v3
    - tx-9
    - rx-8


#### ToDo:
- change pins to ones set
- code bn880
- rename to pico