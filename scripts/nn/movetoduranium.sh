# export LANG=en_US.utf-8
# export LC_ALL=en_US.utf-8

tar cvzf duranium.tar.gz nn
scp -P 1234 duranium.tar.gz s1830120@localhost:/home/s1830120


# ssh -L1234:duranium:22 s1830120@ssh.liacs.nl
# ssh -p 1234 s1830120@localhost
# ssh -D 7000 s1830120@ssh.liacs.nl
