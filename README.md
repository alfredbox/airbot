# airbot

Internet connected air quality sensor using Raspberry pi and IFTTT webhooks.

## Hardware

This project uses a [Raspberry pi](https://www.raspberrypi.org/) (model 3 tested) and a [PMS5003 particulate matter sensor](https://www.adafruit.com/product/3686) from [Adafruit](https://www.adafruit.com/product/3686). The PMS5003 connects to Raspberry pi using serial UART RX pin. Wiring instructions are provided on the Adafruit [documention page](https://learn.adafruit.com/pm25-air-quality-sensor). 

![Photo of airbot hardware.](/img/airbot_photo.png)

## Raspberry Pi Setup

Make sure the Raspberry pi is up to date.
```
sudo apt update && sudo apt upgrade
```

Make sure UART is correctly enabled. Here is a [good post](https://www.circuits.dk/setup-raspberry-pi-3-gpio-uart/) on how to do this. Here are the official [Raspberry pi docs](https://www.raspberrypi.org/forums/viewtopic.php?t=187392).

Setup an apache web server on the pi to host the dashboard.
```
sudo apt install apache2 -y
```

Then take ownership of the website directory for your user.
```
sudo chown <user>: /var/www/html
sudo chown <user>: /var/www/html/index.html
```

Finally go into this project's directory and satisfy any Python requirements
```
cd airbot
sudo pip3 install -r requirements.txt
```

## IFTTT Notifications
This project is setup to send a notification to your phone if the PM2.5 Air Quality Index (AQI) measured by the sensor rises above 99. You will need to install the [IFTTT](https://ifttt.com/) app on your phone and create and [IFTTT](https://ifttt.com/) account. The create a new [IFTTT](https://ifttt.com/) applet through the app. For the 'if' part choose [webhooks](https://ifttt.com/maker_webhooks). For the 'then' part choose notifications. You may pick any name for your webhooks 'event'. For your notifications message click 'insert ingredients' and select `Value1`. Once created navigate to your applet and click the webhooks icon, then click 'documentation'. This page should show you your unique trigger url. Save this, you will need it.

## Local intranet dashboard
This project also creates and serves a basic dashboard from the Raspberry pi. To view it simply enter the Raspberry pi's IP address into the browser of a device that is on the same network. It looks like this:

![Screenshot of airbot dashboard.](/img/airbot_dash.png)

## Config file
You need to create the following config file on the Raspberry pi's filesystem:
```
~/.config/airbot/airbot_cfg.json
```

The file must contain the following JSON formatted config:
```JSON
{
    "ifttt_url": "<your url here>",
    "webserver_dir": "/var/www/html",
    "serial_port": "/dev/ttyS0"
}
```

The `"ifttt_url"` is where you put the url you saved when you created yout applet. The `"webserver_dir"` is where the dasboard will be written. It should be as above unless you have set your website up in a special way. Finally the `"serial_port"` is where the Raspberry pi will listen for data from the sensor. It is as above on the Raspberry pi 3, but it may be different (e.g. `"/dev/ttyAMA0"`) for other models or setups.

## Run the program
Run with 
```
python3 airbot.py
```
You may want to add that to your `crontab` for persistence through restarts.


