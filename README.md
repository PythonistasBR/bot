# Autonomia Bot

[![Build Status](https://travis-ci.org/PythonistasBR/bot.svg?branch=master)](https://travis-ci.org/PythonistasBR/bot)
[![codecov](https://codecov.io/gh/PythonistasBR/bot/branch/master/graph/badge.svg)](https://codecov.io/gh/PythonistasBR/bot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

## Setup bot
Configure the `TELEGRAM_API_TOKEN`

```
cp env_sample .env
```

Install the dependencies and run the Autonomia Bot

```
make install-dev
make run
```

## Useful commands
```
Usage: make command
clean                          Clean all compiled python code
fmt                            Format code using iSort and Black
install-dev                    Install all dependencies
install                        Install only prod dependencies
lint                           Run flake8
run                            Run autonomia bot
test                           Run pytest
```

## License
[MIT](LICENSE)
