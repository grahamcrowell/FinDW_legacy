import os, inspect, time, datetime, shutil
import requests, _mssql

def get_stmt_loading():
	stmt_loading = None
	conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='SSISDB')
	sql = "SELECT * FROM catalog.object_parameters WHERE parameter_name = 'data_src_dir'"
	conn.execute_query(sql)
	for row in conn:
		print(row['parameter_name'],row['design_default_value'])
		stmt_loading = str(row['design_default_value'].decode())
	conn.close()
	if not os.path.exists(stmt_loading):
		os.mkdir(stmt_loading)
	return stmt_loading

def get_stmt_loaded():
	stmt_loaded = None
	conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='SSISDB')
	sql = "SELECT * FROM catalog.object_parameters WHERE parameter_name = 'data_dst_dir'"
	conn.execute_query(sql)
	for row in conn:
		print(row['parameter_name'],row['design_default_value'])
		stmt_loaded = str(row['design_default_value'].decode())
	conn.close()
	if not os.path.exists(stmt_loaded):
		os.mkdir(stmt_loaded)
	return stmt_loaded

def get_stmt_html():
	stmt_html = None
	conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='SSISDB')
	sql = "SELECT * FROM catalog.object_parameters WHERE parameter_name = 'data_html_dir'"
	conn.execute_query(sql)
	for row in conn:
		print(row['parameter_name'],row['design_default_value'])
		stmt_html = str(row['design_default_value'].decode())
	conn.close()
	if not os.path.exists(stmt_html):
		os.mkdir(stmt_html)
	return stmt_html

def get_stmt_parsed():
	stmt_parsed = None
	conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='SSISDB')
	sql = "SELECT * FROM catalog.object_parameters WHERE parameter_name = 'data_parsed_dir'"
	conn.execute_query(sql)
	for row in conn:
		print(row['parameter_name'],row['design_default_value'])
		stmt_parsed = str(row['design_default_value'].decode())
	conn.close()
	if not os.path.exists(stmt_parsed):
		os.mkdir(stmt_parsed)
	return stmt_parsed

def get_stmt_html_nodata():
	stmt_html_nodata = None
	conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='SSISDB')
	sql = "SELECT * FROM catalog.object_parameters WHERE parameter_name = 'data_html_nodata_dir'"
	conn.execute_query(sql)
	for row in conn:
		print(row['parameter_name'],row['design_default_value'])
		stmt_html_nodata = str(row['design_default_value'].decode())
	conn.close()
	if not os.path.exists(stmt_html_nodata):
		os.mkdir(stmt_html_nodata)
	return stmt_html_nodata

stmt_loading = get_stmt_loading()
stmt_loaded = get_stmt_loaded()
stmt_html = get_stmt_html()
stmt_html_nodata = get_stmt_html_nodata()
stmt_parsed = get_stmt_parsed()

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

def parse_stmt(path):
	cid,per_cnt,StatementIDStr,download_date = parse_stmt_filename(path)
	nul_html = '<p>There is no quarterly fundamental data for this company.'
	qtr_html = '<td width="80" class="dkbluert"><b>'
	fdt_html = '<td class="dkbluert" width="80">'
	act_html = '<td class="body1" width="{0}" height="20">' #'<td class="body1" width="125" height="20">
	sub_html = '<td class="indent" width="{0}" height="20">'
	val_html = '<td class="fundnum" align="right" width="80' # a few have ... width="80px"> most have ... width="80">
	err_html = '<td width="80" class="dkbluert"><b></b></td>' # qtr missing -> guess it (cid=100394)

	html = {'err':(err_html,len(err_html)),'nul':(nul_html,len(nul_html)),'qtr':(qtr_html,len(qtr_html)),'fdt':(fdt_html,len(fdt_html)),'act':(act_html,len(act_html)),'sub':(sub_html,len(sub_html)),'val':(val_html,len(val_html))}
	if not os.path.exists(path):
		print('{} DNE'.format(path))
		return (path,None)
	else:
		try:
			qtrs = []
			fdts = []
			act = ''
			sub = ''
			index = 0
			data = []
			print(path)
			html_line_num = 0
			with open(path) as html_file:
				while 1:
					line = html_file.readline()
					html_line_num += 1
					if not line:
						break
					if line[0:html['nul'][1]] == html['nul'][0]:
						print('{} doesnt contain any statement data'.format(path))
						shutil.move(path,get_out_path(path,stmt_html_nodata))
						os.remove(path)
						return (path,None)
					elif line[0:html['err'][1]] == html['err'][0]:
						if qtr == 1:
							qtr = 4
						else:
							qtr -= 1
						qtrs.append(qtr)
					elif line[0:html['qtr'][1]] == html['qtr'][0]:
						try:
							# print(line)
							tmp = line
							line = html_file.readline()
							html_line_num+=1
							line = line.strip()
							if len(line) == 0:
								# sometimes html['qtr'][0] followed by blank line
								line = html_file.readline()
								html_line_num+=1
								line = line.strip()
							# print(line)
							qtr = int(line[0:1])
							# print('qtr = {}'.format(qtr))
							qtrs.append(qtr)
						except Exception as e:
							print('ERROR: ')
							print(tmp)
							print(path)
							print(html_line_num)
							raise Exception('\n\nERROR')
							break
					elif line[0:html['fdt'][1]] == html['fdt'][0]:
						end_pos = line.rfind('<')
						fdt = line[html['fdt'][1]:end_pos]
						# print(fdt)
						fdts.append(fdt)
					elif line[0:html['act'][1]] == html['act'][0].format(125) or line[0:html['act'][1]] == html['act'][0].format(165):
						index = 0
						sub = ''
						end_pos = line.rfind('<')
						act = line[html['act'][1]:end_pos]
						# print(act)
					elif line[0:html['sub'][1]] == html['sub'][0].format(125) or line[0:html['sub'][1]] == html['sub'][0].format(165):
						index = 0
						end_pos = line.rfind('<')
						sub = line[html['sub'][1]:end_pos]
						# print('\t'+sub)
					elif line[0:html['val'][1]] == html['val'][0]:
						line = html_file.readline()
						html_line_num += 1
						if '$' not in line:
							line = html_file.readline()
							html_line_num += 1
							if '$' not in line:
								# ERROR
								print("\n\n\nERROR\n\n\n")
						line = line.strip()
						# print(line)
						if '<' in line:	
							end_pos = line.rfind('<')
							line = line[0:end_pos]
						if '(' in line:
							line = '-'+line[2:-1]
						else:
							line = line[1:]
						line = line.replace(",","")
						val = int(line)
						# print(val)
						tmp_elem = (path,cid,StatementIDStr,download_date,qtrs[index],fdts[index],act,sub,val)
						if None in tmp_elem or '' in (qtrs[index],fdts[index],act,val):
							print('ERROR: ')
							print(tmp)
							print(path)
							print(html_line_num)
							raise Exception('\n\nERROR missing data')

						# print(tmp_elem)
						data.append(tmp_elem)
						index += 1

				csv_path = get_out_path(path,stmt_loading,'.csv')
				header = ['import_path','CIDStr','StatementIDStr','download_date','FiscalQuarterStr','PeriodEndDateStr','AccountStr','SubAccountStr','ValueStr']
				with open(csv_path,'w') as csv:
					tmp_line = '{},{},{},{},{},{},{},{},{}\n'.format(*header)
					csv.write(tmp_line)
					for datum in data:
						tmp_line = '"{}",{},{},{},{},{},"{}","{}",{}'.format(*datum)
						# print(tmp_line)
						csv.write(tmp_line+'\n')
			shutil.move(path,get_out_path(path,stmt_parsed))
			return (path,len(qtrs))
		except Exception as e:
			print(e)
			print('path: {}\nlinenum: {}\n'.format(path,html_line_num))

def get_paths(in_dir):
	full_path = lambda name: os.path.join(in_dir,name)
	pths_in = list(map(full_path,os.listdir(in_dir)))
	return pths_in