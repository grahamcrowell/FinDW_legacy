import os, inspect, time, datetime, shutil, json
import requests, _mssql

json_path='dataFolderConfig.json'
json_file = open(json_path).read()
config=json.loads(json_file)
data_root = config['root']

def get_price_loading():
	price_loading = config['price']['downloaded']
	if not os.path.exists(price_loading):
		print('{} DNE creating...'.format(price_loading))
		os.makedirs(price_loading)
	return price_loading

def get_price_loaded():
	price_loaded = config['price']['loaded']
	if not os.path.exists(price_loaded):
		print('{} DNE creating...'.format(price_loaded))
		os.makedirs(price_loaded)
	return price_loaded

def get_stmt_loading():
	stmt_loading = config['statement']['parsed']
	if not os.path.exists(stmt_loading):
		print('{} DNE creating...'.format(stmt_loading))
		os.makedirs(stmt_loading)
	return stmt_loading

def get_stmt_loaded():
	stmt_loaded = config['statement']['loaded']
	if not os.path.exists(stmt_loaded):
		print('{} DNE creating...'.format(stmt_loaded))
		os.makedirs(stmt_loaded)
	return stmt_loaded

def get_stmt_html():
	stmt_html = config['statement']['downloaded']
	if not os.path.exists(stmt_html):
		print('{} DNE creating...'.format(stmt_html))
		os.makedirs(stmt_html)
	return stmt_html

def get_stmt_parsed():
	stmt_parsed = config['statement']['parsed']
	if not os.path.exists(stmt_parsed):
		print('{} DNE creating...'.format(stmt_parsed))
		os.makedirs(stmt_parsed)
	return stmt_parsed

# def get_stmt_html_nodata():
# 	stmt_html_nodata = None
# 	conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='SSISDB')
# 	sql = "SELECT * FROM catalog.object_parameters WHERE parameter_name = 'data_html_nodata_dir'"
# 	conn.execute_query(sql)
# 	for row in conn:
# 		print(row['parameter_name'],row['design_default_value'])
# 		stmt_html_nodata = str(row['design_default_value'].decode())
# 	conn.close()
# 	if not os.path.exists(stmt_html_nodata):
# 		os.makedirs(stmt_html_nodata)
# 	return stmt_html_nodata

price_loading = get_price_loading()
price_loaded = get_price_loaded()

stmt_loading = get_stmt_loading()
stmt_loaded = get_stmt_loaded()
stmt_html = get_stmt_html()
#stmt_html_nodata = get_stmt_html_nodata()
stmt_parsed = get_stmt_parsed()

def make_price_filename(symbol,start_date,end_date):
	return '{}_{}_{}.csv'.format(symbol,start_date,end_date)

def make_stmt_filename(cid,per_cnt,stmt_code,date_str=None):
	if date_str is None:
		date_str = str(datetime.date.today())
	return '{}_{}_{}_{}.html'.format(cid,stmt_code,date_str,per_cnt)


def nasdaq_stmt_url(cid,per_cnt,stmt_code):
	return 'http://fundamentals.nasdaq.com/nasdaq_fundamentals.asp?CompanyID={}&NumPeriods={}&Duration=1&documentType={}'.format(cid,per_cnt,stmt_code)

def nasdaq_stmt_path(cid,per_cnt,stmt_code):
	return os.path.join(stmt_html,make_stmt_filename(cid,per_cnt,stmt_code,datetime.date.today()))

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

def download_all3(cid_period_cnt):
	print('downloading 3 stmts {}'.format(cid_period_cnt))
	for i in range(1,4,1):
		time.sleep(0.05)
		download(nasdaq_stmt_url(cid_period_cnt[0],cid_period_cnt[1],i),nasdaq_stmt_path(cid_period_cnt[0],cid_period_cnt[1],i))

def parse_stmt_filename(full_path):
	# extract filename
	name = full_path.replace('\\','/').split('/')[-1]
	# return cid,per_cnt,stmt_code,date from input
	cid,stmt_code,download_date,per_cnt = name.split('_')
	return cid,per_cnt,stmt_code,download_date

def get_out_path(in_path,out_dir,new_ext=None):
	if new_ext is not None:
		return os.path.join(out_dir,os.path.splitext(os.path.split(in_path)[1])[0]+'.csv')
	return os.path.join(out_dir,os.path.split(in_path)[1])

def get_paths(in_dir,ext=None):
	full_path = lambda name: os.path.join(in_dir,name)
	ext_filter = lambda name: True
	if ext is not None:
		if ext[0] != '.':
			ext = '.'+ext
		ext_filter = lambda name: os.path.splitext(name)[1] == ext
	pths_in = list(map(full_path,filter(ext_filter,os.listdir(in_dir))))
	return pths_in