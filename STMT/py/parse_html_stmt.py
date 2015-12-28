import re, os, operator, shutil, multiprocessing as mp
import tools

in_dir = os.path.join(tools.data_root,'staging/stmt/html')
out_dir = os.path.join(tools.data_root,'staging/stmt/csv')
archive_dir = os.path.join(tools.data_root,'archive/stmt/html')

def parse_stmt(path):
	cid,per_cnt,StatementIDStr,download_date = tools.parse_stmt_filename(path)
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

				csv_path = tools.get_out_path(path,tools.stmt_loading,'.csv')
				header = ['import_path','CIDStr','StatementIDStr','download_date','FiscalQuarterStr','PeriodEndDateStr','AccountStr','SubAccountStr','ValueStr']
				with open(csv_path,'w') as csv:
					tmp_line = '{},{},{},{},{},{},{},{},{}\n'.format(*header)
					csv.write(tmp_line)
					for datum in data:
						tmp_line = '"{}",{},{},{},{},{},"{}","{}",{}'.format(*datum)
						# print(tmp_line)
						csv.write(tmp_line+'\n')
			shutil.move(path,tools.get_out_path(path,tools.stmt_parsed))
			return (path,len(qtrs))
		except Exception as e:
			print(e)
			print('path: {}\nlinenum: {}\n'.format(path,html_line_num))

def parse_staged_files():
	print('parsing {} html files in staging dir: {}'.format(len(paths_in),tools.stmt_html))
	pool = mp.Pool()
	res = pool.map_async(parse_stmt,paths_in)	
	syms_cids = res.get(timeout=len(paths_in))

if __name__ == '__main__':
	parse_staged_files()
