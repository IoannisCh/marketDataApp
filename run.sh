#!/bin/bash
source myenv/bin/activate
gunicorn app:app -b 0.0.0.0:8050
