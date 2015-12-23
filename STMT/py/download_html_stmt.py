import requests
import os, time, multiprocessing as mp,datetime
import tools


data_root = 'c:/users/user/data/html/stmt2'
if not os.path.exists(data_root):
	os.makedirs(data_root)


def nasdaq_stmt_url(cid,per_cnt,stmt_code):
	return 'http://fundamentals.nasdaq.com/nasdaq_fundamentals.asp?CompanyID={}&NumPeriods={}&Duration=1&documentType={}'.format(cid,per_cnt,stmt_code)

def nasdaq_stmt_path(cid,per_cnt,stmt_code):
	return os.path.join(data_root,tools.make_stmt_filename(cid,per_cnt,stmt_code,datetime.date.today()))

def download(url,inpath):
	# print('downloading {}'.format(url))
	req = requests.get(url)
	with open(inpath,'w') as fout:
		for line in req.iter_lines():
			fout.write(line.decode("utf-8")+'\n')
	if os.path.exists(inpath):
		pass
		# print('saved {}'.format(inpath))
	else:
		print('\n\n\t* * *\nNOT saved {}'.format(inpath))
	time.sleep(0.05)

def download_all3(cid,per_cnt):
	print('downloading 3 stmts {}'.format(cid))
	for i in range(1,4,1):
		time.sleep(0.05)
		download(nasdaq_stmt_url(cid,per_cnt,i),nasdaq_stmt_path(cid,per_cnt,i))

def read_cids():
	# syms_cids = []
	cids = []
	with open('wilshire5000_cid.csv') as f:
		txt = f.read()
		lines = txt.split('\n')
		i = 0	
		n = len(lines)
		while i < n:
			tkns = lines[i].split(',')
			sym = tkns[0]
			cid = tkns[1]
			# syms_cids.append((sym,cid))
			if cid != 'None':
				cids.append(cid)
			i+=1
	return cids

def whats_missing(cids):
	missing = []
	present = []
	for cid in cids:
		for i in range(1,4,1):
			stmt = nasdaq_stmt_path(cid,80,i)
			if not os.path.exists(stmt):
				missing.append(stmt)
			if os.path.exists(stmt):
				present.append(stmt)
	print(len(missing))
	print(len(present))

	import collections
	print([item for item, count in collections.Counter(cids).items() if count > 1])

	return missing

def main():
	cids_in = read_cids()
	print('downloading following cids: ',cids_in)
	cid_cnt = len(cids_in)
	print('{} files to be downloaded'.format(cid_cnt*3))
	pool = mp.Pool()
	res = pool.map_async(download_all3,cids_in)	
	syms_cids = res.get(timeout=cid_cnt*1.5)


if __name__ == '__main__':
	# main()
	cids_in = read_cids()

	whats_missing(cids_in)
	cids_in = list(set(cids_in))
	whats_missing(cids_in)
	

# ['85096', '70147', '4200', '3640', '5895', '4375', '10221', '8528']
# "CBON",85096
# "CNXT",85096
# "CPEX",70147
# "CRED",70147
# "SF",4200
# "SFN",4200
# "AET",3640
# "HUM",3640
# "BHI",4375
# "HAL",4375
# "UBA",10221
# "UBP",10221
# "msft",8528
# "msft",8528

