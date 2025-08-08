#!/bin/bash
set -e

apt-get update -y
apt-get install -y libxml2-dev libxslt-dev python3-dev build-essential

pip install --upgrade pip setuptools wheel

pip install -r requirements.txt
