#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author zhangshu 
# email shuzhangcourage@163.com
# get sequences 

import urllib.request as request
import re

#original url
#initial_url = 'https://www.baidu.com'
initial_url = r'http://plntfdb.bio.uni-potsdam.de/v3.0/fam_mem.php?family_id=C2H2'

#sequence family
sequence_family_regex = b'<A HREF="fam_mem.php\?family_id=C2H2&amp;sp_id=...">'

#pep_id
pep_id_regex = b'<A HREF="gene_details.php\?pep_id=......&amp;sp_id=...">'

def Grab(initial_url):
	x=0
	page = request.urlopen(initial_url)
#	code = page.getcode() usually 200
	rawdata = page.read()
	#print(rawdata)
	raw_sequences_family = re.findall(sequence_family_regex,rawdata)
	#print(sequences_family)
	sequences_family=[]
	for sequence_family in raw_sequences_family:
		sequences_family.append(sequence_family.decode('gbk'))
	for sequence_family in sequences_family:
		element = 'http://plntfdb.bio.uni-potsdam.de/v3.0/'+re.sub('amp;','',sequence_family[9:-2])
		new_page = request.urlopen(element)
		new_rawdata = new_page.read()
		#print(new_rawdata)
		#print (element)
		raw_pep_ids = re.findall(pep_id_regex,new_rawdata)
#		print(raw_pep_ids)
		pep_ids = []
		for pep_id in raw_pep_ids:
			pep_ids.append(pep_id.decode('gbk'))
#		print(pep_ids)
		for pep_id in pep_ids:
			new_element = 'http://plntfdb.bio.uni-potsdam.de/v3.0/get_seq.php?family_id=C2H2&'+pep_id.split(';')[1][0:-2]+'&'+'seqtype=protein%20sequence&model%5B%5D='+pep_id.split('&')[0][-7:]
#			print(new_element)
			x+=1
			request.urlretrieve(new_element,'./data/%s.fa'%x)
#		break
Grab(initial_url)
