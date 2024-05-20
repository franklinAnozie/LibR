#!/usr/bin/bash


SPID=$(pgrep -f frontend.py)
OSPID=$(pgrep -f "python3 -m api.v1.app")

if [ "$SPID" ]; then
    for pid in $SPID; do
        kill "$pid"
    done
fi

if [ "$OSPID" ]; then
    for pid in $OSPID; do
        kill "$pid"
    done
fi
