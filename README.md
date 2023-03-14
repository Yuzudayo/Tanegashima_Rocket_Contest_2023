# Tanegashima_Rocket_Contest_2023

Last Update : 2023/03/07  
Tanegashima Rocket Contest 2023 Runback Program  

キャリア搭載時にプログラムを開始し，気圧センサによって上昇と着地判定をする．センサの異常時に備え，時間経過でも着地判定をするようにしている．着地後，分離機構を作動し，地磁気センサとGPSでゴールの座標まで向かう．途中，スタックやゴールから遠ざかった場合は状況に応じた処理を行う．ゴール接近後，カメラによる画像処理を開始し，ゴールに到達と判断した場合にプログラムを終了する．

## Software Configuration

Language : Python 3.9.2  
OS       : Raspberry Pi OS Lite (32-bit)  
           Raspbian GNU/Linux 11 (bullseye)  
Kernel   : Ver.5.15  
OpenCV   : Ver.4.7.0  

## Hardware Configuration

Microcomputer              : Raspberry pi Zero WH  
GPS                        : GYSFDMAXB  
9-axis sensor              : bno055  
Barometric pressure sensor : bme280  
Camera                     : Raspi Camera v2.1  
Motor Driver               : BD6231F  
GPIO Expander              : MCP23017  

## Program Configuration

- main.py
    Main program. Also performs stack processing and error handling.
- logger.py
    Logging class. Generate files for each phase.
- floating.py
    A class that obtains altitude, determines landing, and activates the separation mechanism.
- ground.py
    Determine the distance between two points and whether the CanSat is facing the goal.
- bme280.py
    Barometric pressure sensor class. Get barometric pressure and temperature.
- GYSFDMAXB.py
    GPS class. Get GPS in daemon thread and return data.
- bno055.py
    9-axis sensor class. Acquire geomagnetic and acceleration sensors. Each sensor value is automatically calibrated and its degree can be monitored.
- img_proc.py
    Image processing class. Take pictures, judge and label red cones.
- motor.py
    Class to move tires. Controls the operation of the body and separation mechanism.


## Set Up 

/boot/config.txt
```
dtoverlay=dwc2
enable_uart=1
dtoverlay=pps-gpio,gpiopin=18,assert_falling_edge=true
#dtoverlay=imx219
#dtoverlay=vc4-fkms-v3d
```

/boot/cmdline.txt
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait modules-load=dwc2,g_ether
```

/etc/default/gpsd/
```
START_DAEMON="true"
DEVICES="/dev/ttyS0 /dev/pps0"
GPSD_OPTIONS="-n"
```

/etc/modules
```
pps-gpio
i2c-bcm2708 
```

/etc/systemd/timesyncd.conf
```
NTP=ntp.jst.mfeed.ad.jp ntp.nict.jp
FallbackNTP=time.google.com
```

Enable NTP
```
$sudo timedatectl set-ntp true
```

Install python3-smbus
```
$sudo apt install python3-smbus
```

Install pip
```
$sudo apt install -y python3 python3-pip
```

Install multimedia packager GPAC
```
$sudo apt install -y gpac
```

Install bno055 library
```
$pip3 install adafruit-circuitpython-bno055
```

Install OpenCV dependency library
```
$sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
$sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
$sudo apt-get install libatlas-base-dev
$sudo apt-get install libjasper-dev
```

Install OpenCV
```
$pip3 install opencv-python --verbose
```

Install OpenCV including extension modules
```
$sudo pip3 install opencv-contrib-python --verbose
``` 
 
Install OpenCV linear algebra calculation package
```
$sudo apt install libatlas3-base
```

Install picamera library
```
$sudo apt install python3-picamera
```

Install picamera2 library
```
$sudo apt install python3-picamera2
```
Set up for picamera2
```
$sudo apt install -y python3-libcamera python3-kms++
$sudo apt install -y python3-prctl libatlas-base-dev ffmpeg libopenjp2-7 python3-pyqt5
$pip3 install numpy --upgrade
$NOGUI=1 pip3 install picamera2
```

Install libcamera apps
```
$sudo apt install libcamera-apps
```

Install pigpio
```
$sudo apt install pigpio python3-pigpio
```

Auto start pigpiod daemon on boot
```
$sudo systemctl enable pigpiod
```

Install mcp230xx library
```
$sudo pip install adafruit-circuitpython-mcp230xx
```

Install git
```
$sudo apt install git
```

Install fbi
```
$sudo apt install fbi
```

Install I2C related tools
```
$sudo apt install i2c-tools
```

Install GPS related tools
```
$sudo apt install gpsd gpsd-clients pps-tools -y
```

Install micropyGPS module
```
$git clone https://github.com/inmcm/micropyGPS
```

Disable serial console
```
$sudo systemctl stop serial-getty@ttyS0.service
$sudo systemctl disable serial-getty@ttyS0.service
```

Activation gpsd.socket
```
$sudo systemctl enable gpsd.socket
```


## Troubleshooting & Commands 

Change settings
```
$sudo raspi-config
```

Reboot
```
$sudo reboot
```

Confirmation of devices connected by I2C
```
$i2cdetect -y 1
```

Display time and time zone
```
$timedatectl
```

Confirmation of time synchronization service
```
$sudo systemctl status systemd-timesyncd
```

Start the pigpiod daemon
```
$sudo pigpiod
```

Network environment status check and settings
```
$ifconfig
```

Check IP address
```
$arp -a
```

Check Wi-Fi connection
```
$ping hostname.local
```

Check SSH connection
```
$ssh username@hostname.local
```

Check OS version
```
$lsb_release -a
```

Check kernel version
```
$uname -a
```

SSH connection to Raspberry Pi from command prompt
```
>ssh username@hostname.local
```

Password hashing
```
$echo -n password | iconv -t utf16le | openssl md4
```

Confirm pin assign
```
$pinout
```

Confirm gpio state
```
$raspi-gpio get
```

Check packages installed with pip
```
$pip list
```

Update package list
```
$sudo apt update
```

Upgrade OS
```
$sudo apt full-upgrade -y
$sudo rpi-update hash value
```
hash value : https://github.com/Hexxeh/rpi-firmware/commits/master

Update pip
```
$sudo python -m pip install --upgrade pip
```

Update numpy
```
sudo pip install -U numpy 
```

Shows what the GPS is receiving
```
$sudo ppstest /dev/pps0
```

Displays signals from satellites, etc.
```
$gpsmon
$cgps -s
```

Check if the camera module is properly connected
```
$libcamera-still --list-cameras
$vcgencmd get_camera(Not recommend)
```

Camera not recognized
Check camera connection -> update & upgrade apt

Take a picture
```
$libcamera-still -n -o imgname.jpg
$sudo raspistill -o imgname(Not recommend)
```

Take a video
```
$sudo raspivid -t millisec -o vidoname.h264
```

Convert h264 to mp4
```
$MP4Box -add filename.h264 filename.mp4
```


## Comment 

製作の遅れによって、プログラムの細かな調整(エラー処理やスタック判定など)ができなかった。また、種子島では、GPSの精度が悪かった。
