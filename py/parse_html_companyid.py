import re, os, operator, multiprocessing as mp

def extract_symbol(pth):
	fnm = os.path.split(pth)[1]
	sym = os.path.splitext(fnm)[0]
	return sym

def parse_companyid(pth):
	sym = extract_symbol(pth)
	if not os.path.exists(pth):
		print('{} DNE'.format(pth))
		return (sym,None)
	else:
		html_file = open(pth)
		lines = list(html_file.readlines())
		re_cid = re.compile('.*companyid=([0-9]+).*')

		# store cids and their respective frequency 
		cid_dct = {}
		for i in range(len(lines)):
			m = re_cid.search(lines[i])
			if m:
				# cid found
				tmp_cid = int(m.groups(1)[0])
				if tmp_cid not in cid_dct:
					cid_dct[tmp_cid] = 1
				else:
					cid_dct[tmp_cid] += 1

		if len(cid_dct) == 0:
			# no companyid's found in HTML file
			print('{} doesnt contain any companyids'.format(pth))
			return (sym,None)
		else:
			# determine most frequent companyid
			cids_by_freq = sorted(cid_dct.items(), key=operator.itemgetter(1))
			cids_by_freq.reverse()
			cid, freq = cids_by_freq[0]
			print('{} doesnt contains {} for {}'.format(pth,cid,sym))
			return (sym,cid)

def parsemany_companyid(pths):
	out = []
	for pth in pths:
		tmp_cid = parse_companyid(pth)
		tmp_sym = extract_symbol(pth)
		out.append((tmp_cid,tmp_sym))
	return out


# pth_in = r'C:\Users\user\data\html\companyid\A.html'
# cid = parse_companyid(pth_in)
# sym = extract_symbol(pth_in)
# print(sym)
# pth_in = r'C:\Users\user\data\html\companyid\AAI.html'
# cid = parse_companyid(pth_in)
# sym = extract_symbol(pth_in)
# print(sym)
# pth_in = r"C:\Users\user\data\html\companyid\BRK-A.html"
# cid = parse_companyid(pth_in)
# sym = extract_symbol(pth_in)
# print(sym)

if __name__ == '__main__':
	dir_in = r"C:\Users\user\data\html\companyid"
	full_path = lambda name: os.path.join(dir_in,name)
	pths_in = list(map(full_path,os.listdir(dir_in)))
	# print(pths_in)

	# cids_syms = parsemany_companyid(pths_in)
	
	pool = mp.Pool()
	res = pool.map_async(parse_companyid,pths_in)	
	syms_cids = res.get(timeout=120)

	print(syms_cids)
	with open('wilshire5000_cid.csv','w') as csv:
		for sym,cid in syms_cids:
			print(cid,sym)
			csv.write('"{}","{}"\n'.format(sym,cid))


