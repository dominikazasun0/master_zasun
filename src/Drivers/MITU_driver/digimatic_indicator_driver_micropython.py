from machine import Pin
import time
import math


REQ_PIN = 20   # pin wyjściowy (REQ)
CLK_PIN = 8   # wejście CLK
DAT_PIN = 9   # wejście DAT

# Ustawienia GPIO
REQ = Pin(REQ_PIN, Pin.OUT, value=0)
CLK = Pin(CLK_PIN, Pin.IN) 
DAT = Pin(DAT_PIN, Pin.IN)

spcdata = [0] * 13

def _now_ms():
    return time.ticks_ms()

def read_frame(timeout_s=2.0):
    # Podnieś REQ aby zainicjować transmisję
    REQ.value(1)
    start = _now_ms()
    timeout_ms = int(timeout_s * 1000)

    for i in range(13):
        k = 0
        for j in range(4):
            # czekaj aż CLK pójdzie w górę (0 -> 1)
            while CLK.value() == 0:
                if time.ticks_diff(_now_ms(), start) > timeout_ms:
                    raise OSError("Timeout waiting for CLK HIGH")
                time.sleep_us(50)

            # czekaj aż CLK pójdzie w dół (1 -> 0)
            while CLK.value() == 1:
                if time.ticks_diff(_now_ms(), start) > timeout_ms:
                    raise OSError("Timeout waiting for CLK LOW")
                time.sleep_us(50)

            bit_val = DAT.value() & 0x1
            k |= (bit_val << j)

        if i == 0:
            REQ.value(0)

        spcdata[i] = k

    return spcdata[:]   

def decode_hex(data):
    return "".join("{:X}".format(x) for x in data)

def decode_human(data):
    value = 0
    for i in range(5, 11):
        value = value * 10 + int(data[i])

    decimal = int(data[11])
    value = value / (10 ** decimal)

    if int(data[4]) == 0x8:
        value *= -1
    unit = "mm"

    return "{value:.{dec}f} {unit}".format(value=value, dec=decimal, unit=unit)

try:
    while True:
        frame = read_frame(timeout_s=2.0)
        print("HEX:", decode_hex(frame))
        print("VAL:", decode_human(frame))
        time.sleep(1)

except KeyboardInterrupt:
    # wyłącz REQ i zakończ
    REQ.value(0)
    print("Przerwano. REQ ustawione na 0.")

