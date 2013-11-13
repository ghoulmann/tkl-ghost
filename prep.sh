#!/bin/bash -ex

ARCH=$(dpkg --print-architecture)
CODENAME=$(lsb_release -s -c)
SOURCEFORGE="http://downloads.sourceforge.net/project/turnkeylinux"

cd /turnkey/fab/bootstraps
wget $SOURCEFORGE/bootstrap/bootstrap-$CODENAME-$ARCH.tar.gz
wget $SOURCEFORGE/bootstrap/bootstrap-$CODENAME-$ARCH.tar.gz.sig

gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 0xA16EB94D
gpg --verify bootstrap-$CODENAME-$ARCH.tar.gz.sig

mkdir /turnkey/fab/bootstraps/$CODENAME
tar -zxf bootstrap-$CODENAME-$ARCH.tar.gz -C /turnkey/fab/bootstraps/$CODENAME

