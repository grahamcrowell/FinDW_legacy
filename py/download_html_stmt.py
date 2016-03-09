import requests
import os, time, multiprocessing as mp
from datetime import *
import tools

def nasdaq_stmt_url(cid,per_cnt,stmt_code):
	return 'http://fundamentals.nasdaq.com/nasdaq_fundamentals.asp?CompanyID={}&NumPeriods={}&Duration=1&documentType={}'.format(cid,per_cnt,stmt_code)

def nasdaq_stmt_path(cid,per_cnt,stmt_code):
	return os.path.join(tools.data_root,tools.make_stmt_filename(cid,per_cnt,stmt_code,date.today()))

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
# html downloaded for all 3 stmt types 
HtmlDownloadParam = collections.namedtuple('HtmlDownloadParam',['CID', 'period_cnt'])

def download_all3(html_download_param):
	print('downloading 3 stmts {}'.format(html_download_param))
	for stmt_code in range(1,4,1):
		time.sleep(0.05)
		src_url = nasdaq_stmt_url(html_download_param.CID,html_download_param.period_cnt,stmt_code)
		dst_pth = nasdaq_stmt_path(html_download_param.CID,html_download_param.period_cnt,stmt_code)
		download(src_url,dst_pth)
