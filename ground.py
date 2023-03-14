import bno055
import GYSFDMAXB
import math
import time
import logger
import motor

des_lng = 130.96011666666666
des_lat = 30.374275
earth_rad = 6378.137 * 10**3

des_lng = math.radians(des_lng)
des_lat = math.radians(des_lat)

def cal_To_des_ang(gps_lng, gps_lat):
    des_ang = 90 - math.atan2(math.cos(gps_lat) * math.tan(des_lat) - math.sin(gps_lat) * math.cos(des_lng - gps_lng), math.sin(des_lng - gps_lng))* 180/math.pi
    if des_ang < 0:
        des_ang += 360
    """
    https://keisan.casio.jp/exec/system/1257670779
    PointA(lng x1, lat y1), PointB(lng x2, lat y2)
            (gps_lng, gps_lat),     (des_lng, des_lat)
    ϕ = 90 - atan2(sinΔx, cosy1tany2 - siny1cosΔx)
    Δx = x2 - x1
    """
    print("To destination angle :", des_ang)
    return des_ang

def cal_distance(x2, y2):
    while GYSFDMAXB.read_GPSData() == [0,0]:
        print("Waiting for GPS reception")
        time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    x1 = math.radians(gps[0])
    y1 = math.radians(gps[1])
    """
    https://keisan.casio.jp/exec/system/1257670779
    PointA(lng x1, lat y1), PointB(lng x2, lat y2)
        (gps_lng, gps_lat),     (des_lng, des_lat)
    d = rcos^-1(siny1siny2 + cosy1cosy2cosΔx)
    Δx = x2 - x1
    """
    return earth_rad * math.acos(math.sin(y1) * math.sin(y2) + math.cos(y1) * math.cos(y2) * math.cos(x2 - x1))

def cal_heading_ang():
    data = bno055.read_Mag_AccelData()
    """
    data = [magX, magY, magZ, accelX, accelY, accelZ, calib_mag, calib_accel]
    """
    hearding_ang = math.atan2(data[1], data[0])
    hearding_ang = math.degrees(hearding_ang)
    if hearding_ang < 0:
        hearding_ang += 360
    print("Heading angle :",hearding_ang)
    return hearding_ang, data

def is_heading_goal():
    while GYSFDMAXB.read_GPSData() == [0,0]:
        print("Waiting for GPS reception")
        time.sleep(5)
    gps = GYSFDMAXB.read_GPSData()
    gps_lng = math.radians(gps[0])
    gps_lat = math.radians(gps[1])
    To_des_ang = cal_To_des_ang(gps_lng, gps_lat)
    heading_ang, data = cal_heading_ang()
    ang_diff = abs(To_des_ang - heading_ang)
    if ang_diff < 7 or 353 < ang_diff:
        return [To_des_ang, heading_ang, ang_diff, True, "Go Straight"] + gps + data
    else:
        if ((heading_ang > To_des_ang and ang_diff < 180) or (heading_ang < To_des_ang and ang_diff > 180)):
            return [To_des_ang, heading_ang, ang_diff, False, "Turn Left"] + gps + data
        else:
            return [To_des_ang, heading_ang, ang_diff, False, "Turn Right"] + gps + data

if __name__ == '__main__':
    ground_log = logger.Ground_logger()
    logger.Ground_logger.state = 'Normal'
    drive = motor.Motor()
    while True:
        distance = cal_distance(des_lng, des_lat)
        print("distance :", distance)
        if distance < 3:
            print("end")
            drive.stop()
            ground_log.end_of_ground_phase()
            break
        data = is_heading_goal()
        ground_log.ground_logger(data, distance)
        if data[3] == True:
            print("Heading Goal!!")
            drive.forward()
        else:
            if data[4] == 'Turn Right':
                print("Turn right")
                drive.turn_right()
            elif data[4] == 'Turn Left':
                print("Turn left")
                drive.turn_left()
        time.sleep(0.8)