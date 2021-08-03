# export LANG=en_US.utf-8
# export LC_ALL=en_US.utf-8

tar cvzf script.tar.gz process.py generate_index.py
scp -P 1234 script.tar.gz s1830120@localhost:/home/s1830120


# ssh -L1234:latinum:22 s1830120@ssh.liacs.nl
# ssh -p 1234 s1830120@localhost
# ssh -D 7000 s1830120@ssh.liacs.nl
# latinum