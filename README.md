# iCal Maker

A simple python project gets data needed from [KFUPM Registrar](https://registrar.kfupm.edu.sa/).

## Requirements

- Should download [Google Chrome](https://www.google.com/chrome/).
- Should download [Selenium WebDriver](https://chromedriver.chromium.org/downloads) **with the right version**.

## Setup (Linux)

### Github

- Clone repository

```
git clone https://github.com/Yokozuna59/ical_maker.git
```

### Chrome

- Downloading [Google Chrome](https://www.google.com/chrome/).
- Check your Chrome version

```
google-chrome --version
```

### Selenium

- Installing modules

```
pip3 install selenium
```

```
pip3 install beautifulsoup4
```

- Download the [Selenium WebDriver](https://chromedriver.chromium.org/downloads) as same as your Chrome version then unzip it.

you need **root** to do next step:

- Move the file to right place

```
mv /home/<user>/Downloads/<unzipped file> /usr/local/share/chromedriver
```

- make the file executable

```
chmod +x /usr/local/share/chromedriver
```

- Link them together

```
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
```

```
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```
