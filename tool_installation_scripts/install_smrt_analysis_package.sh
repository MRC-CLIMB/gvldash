#!/bin/bash
###############################################################
# script run on target machine to install smrt_analysis package
###############################################################

[ -d "/mnt/gvl/apps" ] || mkdir -p /mnt/gvl/apps # ensure /mnt/galaxy/apps exists
cd /opt/gvl
if [ -d "/opt/gvl/gvl.ansible.smrt_analysis" ]; then
  cd /opt/gvl/gvl.ansible.smrt_analysis 
  git pull https://github.com/MRC-CLIMB/gvl.ansible.smrt_analysis
else
  git clone https://github.com/MRC-CLIMB/gvl.ansible.smrt_analysis
fi
cd /opt/gvl/gvl.ansible.smrt_analysis
ansible-playbook -i inventory/builders playbook.yml
