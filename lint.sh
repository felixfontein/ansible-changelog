#!/bin/bash
flake8 --ignore=E501 ansible_changelog
pylint --disable C0116,C0103,C0301,C0114,R0913,R0914,R1702,R0912,R0205,R0903,W0703,C0115,R0902,R0915 ansible_changelog
