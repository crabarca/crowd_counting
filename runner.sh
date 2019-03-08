#bin/bash
lib/startMonitor.sh
python probemon/probemon.py -i wlp2s0mon -fsr -D -o probemon.log
lib/endMonitor.sh