# Autonomia Bot

[![Build Status](https://travis-ci.org/PythonistasBR/bot.svg?branch=master)](https://travis-ci.org/PythonistasBR/bot)
[![codecov](https://codecov.io/gh/PythonistasBR/bot/branch/master/graph/badge.svg)](https://codecov.io/gh/PythonistasBR/bot)
[![Maintainability](https://api.codeclimate.com/v1/badges/2ab48f832b7383d5cae6/maintainability)](https://codeclimate.com/github/PythonistasBR/bot/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

## Setup bot

```
cp env_sample .env
```

#### Step 1
Get n Telegram API Token with the [Bot father](https://telegram.me/botfather)

Configure the `TELEGRAM_API_TOKEN`

#### Step 2
Install https://ngrok.com/

Run ngrok
```
ngrok http 5000
```

Configure `WEBHOOK_DOMAIN` with the given domain from ngrok

#### Step 3
Install the dependencies and run the Autonomia Bot

```
make install-dev
make run
```

## Useful commands
```
Usage: make command
clean                          Clean all compiled python code
coverage                       Run test and create HTML coverage report
fmt                            Format code using iSort and Black
install-dev                    Install all dependencies
install                        Install only prod dependencies
lint                           Run flake8
run                            Run bot using flask as server
test                           Run pytest
update_webhook                 Update telegram webhook config from settings
```

## License
[MIT](LICENSE)
