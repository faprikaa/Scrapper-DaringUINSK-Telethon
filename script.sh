#!/bin/sh
/usr/bin/pkill -9 chrome
/usr/bin/tmux new-session -d -s ENTER
/usr/bin/tmux detach -s ENTER
sleep 3
/usr/bin/tmux send-keys -t 0 "cd /root/Thoriq/DaringScraper; /usr/bin/python3 main.py " ENTER