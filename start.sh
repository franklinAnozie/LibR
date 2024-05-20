#!/usr/bin/bash

SCRIPT_NAME="frontend.py"
OTHER_SCRIPT="python3 -m api.v1.app"
SPID=$(pgrep -f frontend.py)
OSPID=$(pgrep -f "python3 -m api.v1.app")

if [ "$SPID" ]; then
:
else
    ./$SCRIPT_NAME >/dev/null 2>&1 &
fi
if [ "$OSPID" ]; then
:
else
    $OTHER_SCRIPT >/dev/null 2>&1 &
fi
