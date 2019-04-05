#!/usr/bin/env bash
################################################################################
# script run on target machine to install the gal command line utilities package
################################################################################

[ -d "/mnt/gvl/apps" ] || mkdir -p /mnt/gvl/apps # ensure /mnt/galaxy/apps exists
cd /opt/gvl
if [ -d "/opt/gvl/gvl_commandline_utilities" ]; then 
  cd /opt/gvl/gvl_commandline_utilities
  git pull https://github.com/MRC-CLIMB/gvl_commandline_utilities
else
  git clone https://github.com/MRC-CLIMB/gvl_commandline_utilities
fi
chown -R ubuntu:ubuntu /opt/gvl/gvl_commandline_utilities
sudo su - ubuntu -c "cd /opt/gvl/gvl_commandline_utilities; source run_all.sh -s"
