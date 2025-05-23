set -m 
python3 ieee_sp_ranking.py & pid1=$!
python3 usenix_ranking.py & pid2=$!
python3 ccs_ranking.py & pid3=$!
python3 combined_ranking.py & pid4=$!

# this script spawns subprocesses that need to be closed when this script closes
trap "kill $pid1 $pid2 $pid3 $pid4" EXIT
wait