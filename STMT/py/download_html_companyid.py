import requests, pymssql, numpy as np
import os, time
import tools


# staging_stmt_cid=c:/users/user/data/staging/cid_html
data_root = tools.params['staging_stmt_cid']
# symbol_list=c:/users/user/data/wilshire5000.csv
symbol_list = tools.params['symbol_list']

syms = []
with open(symbol_list) as f:
	txt = f.read()
	lines = txt.split('\n')
	i = 0
	n = len(lines)
	while i < n:
		name = lines[i]
		i+=1
		symbol = lines[i]
		i+=1
		syms.append(symbol)


yahoo_edgar_id_lookup_url = lambda symbol: 'http://yahoo.brand.edgar-online.com/default.aspx?ticker={}'.format(symbol.replace('.','%27'))
yahoo_edgar_id_lookup_html_path = lambda symbol: os.path.join(data_root,'{}.html'.format(symbol.replace('.','-')))

def download_companyid(specs):
	# downloads html from specs[0] and saves it to specs[1]
	url = specs[0]
	pth = specs[1]
	print(url)
	print(pth)
	req = requests.get(url)
	with open(pth,'w') as fout:
		for line in req.iter_lines():
			fout.write(line.decode("utf-8")+'\n')
	time.sleep(0.1)


download_edgar_id_html = lambda symbol: download(yahoo_edgar_id_lookup_url(symbol),yahoo_edgar_id_lookup_html_path(symbol))
sym = 'BRK.A'
download_edgar_id_html(sym)
for sym in syms:
	print(sym)
	download_edgar_id_html(sym)	
