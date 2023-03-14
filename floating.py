import bme280
import time
import logger
import motor

sea_level_pressure = 1013.25

def cal_altitude():
  bme280.read_BaroData() # discard the first value
  time.sleep(0.1)
  data = bme280.read_BaroData()
  """
  data[0] = pressure
  data[1] = temperature
  data[2] = altitude
  
  https://keisan.casio.jp/exec/system/1257609530
  altitude = (Sea level pressure / Current pressure)**(1 / 5.257) - 1) * (Current temperature + 273.15) / 0.0065
  """
  data[2] = ((sea_level_pressure / data[0])**(1 / 5.257) - 1) * (data[1] + 273.15) / 0.0065
  print("altitude :", data[2])
  return data

if __name__ == '__main__':
    floating_log = logger.Floating_logger()
    drive = motor.Motor()
    state = 1
    logger.Floating_logger.state = 1
    print("initial altitude")
    data = cal_altitude()
    init_altitude = data[2]
    floating_log.floating_logger(data)
    print("Rising phase")
    while state != 3:
        """
        state 1 : Rising
              2 : Falling
              3 : Landing
             -1 : Error
        """
        while state == 1:
            data = cal_altitude()
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Rising")
            if altitude >= init_altitude + 10:
                state = 2
                logger.Floating_logger.state = 2
            time.sleep(0.3)
        while state == 2:
            data = cal_altitude()
            altitude = data[2]
            floating_log.floating_logger(data)
            print("Falling")
            if altitude <= init_altitude + 3:
                state = 3
                logger.Floating_logger.state = 3
            time.sleep(0.1)
        floating_log.end_of_floating_phase()
        drive.sepa_mecha() # Separation mechanism activated