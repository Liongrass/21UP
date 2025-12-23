# Modules
import logging

def read_bus(file):
    f = open(file,"rt")
    value = int(f.readline())
    f.close
    return value

def dht11_val():
    t = h = 0
    tries = 3
    for attempt in range(tries):
        try:
            t = read_bus("/sys/bus/iio/devices/iio:device0/in_temp_input")/1000
            h = read_bus("/sys/bus/iio/devices/iio:device0/in_humidityrelative_input")/1000
        except Exception as e:
            if attempt < tries - 1:
                logging.debug(f"Reading barometer: {e} Attempt: {attempt + 1} of {tries}")
                continue
            else:
                logging.info(f"Reading barometer: {e} All attempts exhausted. Giving up.")
                t = h = "N/A"
        return t, h


def get_barometrics():        
        (t, h) = dht11_val()
        logging.info(f"Temperature {t}°C, Humidity: {h}%")
        return t