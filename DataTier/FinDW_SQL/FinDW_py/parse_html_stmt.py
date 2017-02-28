import re, os, operator, shutil, collections, itertools, multiprocessing as mp
import tools

in_dir = tools.stmt_loading
out_dir = tools.stmt_loading
archive_dir = tools.stmt_parsed

HtmlParseParam = collections.namedtuple('HtmlParseParam',['html_src_path', 'html_dst_dir', 'csv_dst_dir'])

class StatementRecord:
	__account = ''
	__sub_account = ''
	__fiscal_period = ''
	__sub_account_name = ''
	__fiscal_period_end_date = ''
	__money_amount = ''

	__statement_number = ''
	__cid = ''
	__download_date = ''

	def __init__(self):
		pass
	def get_header(self):
		return ''
	def get_csv(self):
		return ''

def parse_stmt(html_parse_param):
	# single named tuple parameter to allow calling from multiprocessing.map
	html_src_path = html_parse_param.html_src_path
	html_dst_dir = html_parse_param.html_dst_dir
	csv_dst_dir = html_parse_param.csv_dst_dir
	
	cid,per_cnt,StatementIDStr,download_date = tools.parse_stmt_filename(html_src_path)
	nul_html = '<p>There is no quarterly fundamental data for this company.'
	qtr_html = '<td width="80" class="dkbluert"><b>'
	fdt_html = '<td class="dkbluert" width="80">' # fiscal date
	act_html = '<td class="body1" width="{0}" height="20">' #'<td class="body1" width="125" height="20">
	sub_html = '<td class="indent" width="{0}" height="20">'
	val_html = '<td class="fundnum" align="right" width="80' # a few have ... width="80px"> most have ... width="80">
	err_html = '<td width="80" class="dkbluert"><b></b></td>' # qtr missing -> guess it (cid=100394)

	html = {'err':(err_html,len(err_html)),'nul':(nul_html,len(nul_html)),'qtr':(qtr_html,len(qtr_html)),'fdt':(fdt_html,len(fdt_html)),'act':(act_html,len(act_html)),'sub':(sub_html,len(sub_html)),'val':(val_html,len(val_html))}
	if not os.path.exists(html_src_path):
		print('{} DNE'.format(html_src_path))
		return (html_src_path,None)
	else:
		try:
			qtrs = []
			fdts = []
			act = ''
			sub = ''
			index = 0
			data = []
			qtr = None
			html_line_num = 0
			print('parsing: '+html_src_path)
			with open(html_src_path) as html_file:
				while 1:
					line = html_file.readline()
					html_line_num += 1
					if not line:
						break
					if line[0:html['nul'][1]] == html['nul'][0]:
						print('{} doesnt contain any statement data moving to {}'.format(html_src_path, html_dst_dir))
						html_file.close()
						shutil.move(html_src_path,html_dst_dir)
						return (html_src_path,None)
					elif line[0:html['err'][1]] == html['err'][0]:
						# qtr is missing
						qtrs.append('')
							
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
							print(html_src_path)
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
								print("\n\n\nERROR (no $ found)\n\n\n")
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
						tmp_elem = (html_src_path,cid,StatementIDStr,download_date,qtrs[index],fdts[index],act,sub,val)
						if None in tmp_elem or '' in (fdts[index],act,val):
							print('WARNING: missing data')
							print(tmp)
							print(html_src_path)
							print(html_line_num)
							# raise Exception('\n\nERROR ')

						# print(tmp_elem)
						data.append(tmp_elem)
						index += 1

				csv_path = tools.get_out_path(html_src_path,csv_dst_dir,'.csv')
				header = ['import_path','CIDStr','StatementIDStr','download_date','FiscalQuarterStr','PeriodEndDateStr','AccountStr','SubAccountStr','ValueStr']
				with open(csv_path,'w') as csv:
					tmp_line = '{},{},{},{},{},{},{},{},{}\n'.format(*header)
					csv.write(tmp_line)
					for datum in data:
						tmp_line = '"{}",{},{},{},{},{},"{}","{}",{}'.format(*datum)
						# print(tmp_line)
						csv.write(tmp_line+'\n')
			shutil.move(html_src_path,html_dst_dir)
			return (html_src_path,len(qtrs))
		except Exception as e:
			print(e)
			print('path: {}\nlinenum: {}\n'.format(html_src_path,html_line_num))

def parse_staged_files():
	html_paths = tools.get_paths(tools.stmt_html,'html')[0:1]
	path_setter = lambda path_in: HtmlParseParam(path_in,tools.stmt_loaded,tools.stmt_loading)
	html_parse_params = map(path_setter, html_paths)
	
	# html_parse_param = HtmlParseParam(html_paths[0],tools.stmt_parsed,tools.stmt_loading)
	# parse_stmt(html_parse_param)
	
	print('parsing {} html files with {} thread pool in staging dir: {}'.format(len(html_paths),mp.cpu_count(),tools.stmt_html))
	pool = mp.Pool(mp.cpu_count())
	res = pool.map_async(parse_stmt,html_parse_params)
	syms_cids = res.get(timeout=len(html_paths))

if __name__ == '__main__':
	parse_staged_files()
