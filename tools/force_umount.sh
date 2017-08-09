#!/bin/bash

kill_stuff() {
    killall -9 nfsD 2> /dev/null
    killall -9 rpcbind 2> /dev/null
    killall -9 rpc.mountd 2> /dev/null
    killall -9 nfsd 2> /dev/null
}

if [ $# -ne 1 ] ; then
    echo "Usage: $0 <mountpoint>"
    exit 1
fi

# remove terminating / from mount point
MP=$(echo $1 | sed -E 's_/*$__')
MNT=$(mount | grep $MP | grep nfs)

if [ $? -ne 0 ] ; then
    echo "Can't find mountpoint $MP"
    exit 1
fi

IP=$(echo $MNT | awk -F : '{print $1}')

echo IP is $IP

kill_stuff

modprobe dummy
ifconfig dummy0 $IP netmask 255.255.255.255 up

which rpc.mountd >/dev/null
if [ $? -ne 0 ] ; then
    echo "rpc.mountd not found"
    echo "You should probably apt-get install nfs-kernel-server"
    exit 1
fi

rpcbind
rpc.mountd
rpc.nfsd

echo Unmounting...
sleep 1
umount -f $MP
sleep 1

for i in $(lsof 2> /dev/null | grep $MP | awk '{print $2}') ; do
    kill -9 $i
done

sleep 1
umount -f $MP

ifconfig dummy0 0.0.0.0 down

kill_stuff

MNT=$(mount | grep $MP | grep nfs)

if [ $? -eq 0 ] ; then
    echo "Damn that didn't work man..."
    exit 1
fi

echo "YEAH!"

exit 0
