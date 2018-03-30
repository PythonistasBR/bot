# Autonomia Bot

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
run           - Run autonomia bot
fmt           - Format code using Black
lint          - Run flake8
install-dev   - Install all dependencies
install       - Install only prod dependencies
clean         - Clean all compiled python code
```

## License
MIT
