import requests
import os, time, multiprocessing as mp
from datetime import *
import tools

def yahoo_price_url(symbol,start_date,end_date=None):
	if end_date is None:
		end_date = date.today()
	price_param = {'symbol':symbol, 'start_day':start_date.day, 'start_month':start_date.month-1, 'start_year':start_date.year, 'end_day':end_date.day, 'end_month':end_date.month-1, 'end_year':end_date.year}
	return 'http://real-chart.finance.yahoo.com/table.csv?s={symbol}&d={start_month}&e={start_day}&f={start_year}&g=d&a={end_month}&b={end_day}&c={end_year}&ignore=.csv'.format(**price_param)

def yahoo_price_path(symbol,start_date,end_date=None):
	if end_date is None:
		end_date = date.today()
	return os.path.join(tools.data_root,tools.make_stmt_filename(cid,per_cnt,stmt_code,datetime.date.today()))

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