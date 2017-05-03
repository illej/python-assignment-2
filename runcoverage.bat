@echo off

coverage run --branch unittests.py
coverage report -m
coverage html

PAUSE