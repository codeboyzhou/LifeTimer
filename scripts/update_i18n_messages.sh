#!/usr/bin/env bash

pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d i18n
