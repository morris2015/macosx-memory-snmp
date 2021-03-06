#!/usr/bin/python

# Purpose: Output number of memory bytes derived from vm_stat. Intended as a replacement for /proc/meminfo since Mac OS X doesn't have this facility. This script can be incorporated into /etc/snmp/snmpd.conf

# Original author: drfrogsplat
# http://apple.stackexchange.com/users/1587/drfrogsplat
# http://apple.stackexchange.com/questions/4286/is-there-a-mac-os-x-terminal-version-of-the-free-command-in-linux-systems

# Author:  Mario Aeby, info@eMeidi.com
# Version: 0.2
#
# Changes
# - Added check for number of command line arguments
# - Only output selected attribute as number of bytes
#
# Home:    github.com/emeidi/macosx-memory-snmp

import sys
import subprocess
import re

if len(sys.argv) != 2:
	print 'Usage: ' + sys.argv[0] + ' [free|wired|active|inactive|used]'
	sys.exit(1)

parameter = sys.argv[1]
#print 'Parameter: ' + parameter
#sys.exit(0)

# Get process info
ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0]
vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0]

# Iterate processes
processLines = ps.split('\n')
sep = re.compile('[\s]+')
rssTotal = 0 # kB
for row in range(1,len(processLines)):
    rowText = processLines[row].strip()
    rowElements = sep.split(rowText)
    try:
        rss = float(rowElements[0]) * 1024
    except:
        rss = 0 # ignore...
    rssTotal += rss

# Process vm_stat
vmLines = vm.split('\n')
sep = re.compile(':[\s]+')
vmStats = {}
for row in range(1,len(vmLines)-2):
    rowText = vmLines[row].strip()
    rowElements = sep.split(rowText)
    vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

if parameter == 'free':
	print str(vmStats["Pages free"])

if parameter == 'wired':
	print str(vmStats["Pages wired down"])

if parameter == 'active':
	print str(vmStats["Pages active"])

if parameter == 'inactive':
	print str(vmStats["Pages inactive"])

if parameter == 'used':
	total = vmStats["Pages wired down"] + vmStats["Pages active"] + vmStats["Pages inactive"]
	print str(total)

if parameter == 'interactive':
	# Stuff left behind from the original script
	print 'Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 )
	print 'Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 )
	print 'Inactive Memory:\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 )
	print 'Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 )
	print 'Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 )

sys.exit(0);