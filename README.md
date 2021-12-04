# iCal Maker

A simple python project gets data needed from [KFUPM Registrar](https://registrar.kfupm.edu.sa/).

## Requirements

- Should download [Google Chrome](https://www.google.com/chrome/).
- Should download [Selenium WebDriver](https://chromedriver.chromium.org/downloads) **with the right version**.

## Setup

### Github

1. Clone repository

```
git clone https://github.com/Yokozuna59/ical_maker.git
```

### Chrome

1. Downloading [Google Chrome](https://www.google.com/chrome/).
2. Check your Chrome version

```
google-chrome --version
```

### Selenium

1. Installing selenium module

```
pip3 install selenium
```

2. Download the [Selenium WebDriver](https://chromedriver.chromium.org/downloads) as same as your Chrome version then unzip it.

you need root to do next step:

```
mv /home/potato/Downloads/<unzipped file> /usr/local/share/chromedriver
```

1. make the file executable

```
chmod +x /usr/local/share/chromedriver
```

5. Link them together
```
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```