#!/usr/bin/python

# K L Nasveschuk
# klnasveschuk@gmail.com
# 2016-05-03

# Nagios plugin to return adapter, logical drive and physical drive status
# for LSI MegaRaid based adapters (Dell PERCs included)

# Changelog
# 2016-05-03
# Initial

from os import popen,close
import re,sys

# Must define the MegaCli to use here:
megacli = '/opt/MegaRAID/MegaCli/MegaCli64'

ld_result = ''
pd_result = ''
m = 0
status = 'OK'

###############################################
def get_ldcount(m):
	cmd = megacli + ' -LDGetNum -a' + str(m)
	p = popen(cmd,'r')
	for k in p:
		if re.search('Number of Virtual',k,re.I):
			tmp = k.rstrip().split(':')
			ldcount = int(tmp[1].rstrip('.'))
	p.close()
	return ldcount

def get_ldinfo(m,ld):
	result = ''
	cmd = megacli + ' -LDInfo  -L' + str(ld) + ' -a' + str(m)
	p = popen(cmd,'r')
	for j in p:
		if re.match('^Size',j,re.I):
			size = j.rstrip().split(':')
		if re.match('^RAID',j,re.I):
			raid = j.rstrip().split(':')
		if re.match('^Number Of Drives',j):
			drives = j.rstrip().split(':')
		if re.match('^State',j,re.I):
			state = j.rstrip().split(':')
			if 'Optimal' not in state[1]:
				check_state('CRITICAL')
	result = 'RAID:' + raid[1] + ',drives:' + drives[1] + ',size:' + size[1] + ',state:' + state[1]
	p.close()
	return result

def get_enc_info(m):
	enc = []
	cmd = megacli + ' -EncInfo -a' + str(m)
	p = popen(cmd,'r')
	for j in p:
		if re.match('Device ID',j,re.I):
			enc_id = j.rstrip().split(':')
			enc = enc.append(enc_id)
	p.close()
	return enc

def get_pd_count(m):
	cmd = megacli + ' -PDGetNum -a' + str(m)
	p = popen(cmd,'r')
	for k in p:
		if re.search('Number of Physical',k,re.I):
			tmp = k.rstrip().split(':')
			pdcount = int(tmp[1].rstrip('.'))
	p.close()
	return pdcount

def get_pdinfo(m,enc,pd):
	result = ''
	for i in enc:
		cmd = megacli + ' -pdInfo  -PhysDrv[' + str(i) + ' -a' + str(m)
		p = popen(cmd,'r')
		for j in p:
			if re.match('^Size',j,re.I):
				size = j.rstrip().split(':')
			if re.match('^RAID',j,re.I):
				raid = j.rstrip().split(':')
			if re.match('^Number Of Drives',j):
				drives = j.rstrip().split(':')
			if re.match('^State',j,re.I):
				state = j.rstrip().split(':')
				if 'Optimal' not in state[1]:
					check_state('CRITICAL')
	result = 'RAID:' + raid[1] + ',drives:' + drives[1] + ',size:' + size[1] + ',state:' + state[1]
	p.close()
	return result


def get_pdinfo(a):
	result = ''
	media = 0
	other = 0
	predict = 0
	cmd =  megacli + ' -PDList' + ' -a' + str(a)
	p = popen(cmd,'r')
	for j in p:
		if re.match('^Media Error',j,re.I):
			c1 = j.rstrip().split(':')
			media += int(c1[1])
			if media > 0:
				check_state('WARNING')
		if re.match('^Predictive Failure',j,re.I):
			c2 = j.rstrip().split(':')
			predict += int(c2[1])
			if predict > 0:
				check_state('WARNING')
		if re.match('^Other',j,re.I):
			c3 = j.strip().split(':')
			other += int(c3[1])
			if other > 0:
				check_state('WARNING')
	if result:
		result = result + ' Adapter:' + str(a) + ' Media errors:' + str(media) + ' Predictive failure:' + str(predict) + ' Other errors:' + str(other)
	else:
		result = 'Adapter:' + str(a) + ' Media errors:' + str(media) + ' Predictive failure:' + str(predict) + ' Other errors:' + str(other)
	p.close()
	return result

def check_state(compare):
	global status
	if status == 'OK' and compare == 'CRITICAL':
		status = 'CRITICAL'
	if status == 'CRITICAL' and compare == 'WARNING':
		pass
	if status == 'CRITICAL' and compare == 'CRITICAL':
		pass
	if status == 'OK' and compare == 'WARNING':
		status = 'WARNING'
	if status == 'WARNING' and compare == 'WARNING':
		pass
	if status == 'WARNING' and compare == 'CRITICAL':
		status = 'CRITICAL'

cmd = megacli + ' -ADPCount'
p = popen(cmd,'r')
for k in p:
	if re.search('Controller Count',k,re.I):
		tmp = k.rstrip().split(':')
		count = int(tmp[1].rstrip('.'))
p.close()

if count > 0:
	while m < count:
		n = 0
		ld = get_ldcount(m)
		
		while n < ld:
			if ld_result:
				ld_result = ld_result + ';' +  get_ldinfo(m,n)
			else:
				ld_result = get_ldinfo(m,n)
			n += 1
	
		if pd_result:
			pd_result = pd_result + ';' + get_pdinfo(m)
		else:
			pd_result = get_pdinfo(m)
		m += 1
else:
	status = 'CRITICAL'
	ld_result = 'NO controllers found'

if status == 'CRITICAL':
	e = 2
elif status == 'WARNING':
		e = 1
elif status == 'OK':
		e = 0
else:
	e = 2
status = status + ': ' + ld_result + ' ' + pd_result
print status
sys.exit(e)
