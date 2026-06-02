#!/bin/bash
state=$(hyprctl hyprmodoro:getState 2>/dev/null | tr -d '\r\n')

if [ "$state" = "STOPPED" ] || [ -z "$state" ]; then
    hyprctl dispatch hyprmodoro:start
else
    hyprctl dispatch hyprmodoro:pause
fi
