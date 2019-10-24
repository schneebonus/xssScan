# SeleniumXssBruteforcer

This project develops an XSS bruteforcer. An added value of this project compared to existing bruteforcers is the use of a Firefox browser controlled by Selenium.

Since this project is a new hobby project without a roadmap, the capabilities are still limited and it is not sure whether an active further development will take place.

# Install

Tested on debian 10 but every distro should offer selenium.

- Install python3 and python3-pip ( sudo apt install python3 python3-pip )
- Install firefox or firefox-esr ( sudo apt install firefox-esr )
- Install selenium ( pip3 install selenium --user )
- Download the latest gecko driver from https://github.com/mozilla/geckodriver/releases and extract it to /usr/local/bin/geckodriver
- set owner of /usr/local/bin/geckodriver to root ( sudo chown root:root /usr/local/bin/geckodriver )
- set permissions for /usr/local/bin/geckodriver to 755 ( sudo chmod 755 /usr/local/bin/geckodriver )

# Use

XSS payloads are stored in xss.txt. Each line represents one payload.

To run a scan:

```
python3 scan.py [url]
```

Example:

```
python3 scan.py https://xss-game.appspot.com/level1/frame?query=
```
