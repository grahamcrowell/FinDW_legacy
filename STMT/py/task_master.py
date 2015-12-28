import _mssql
import download_html_stmt
import multiprocessing as mp

import requests
import os, time, multiprocessing as mp,datetime
import tools


data_root = 'c:/users/user/data/testing'
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

def download_all3(cid_period_cnt):
	print('downloading 3 stmts {}'.format(cid_period_cnt))
	for i in range(1,4,1):
		time.sleep(0.05)
		download(nasdaq_stmt_url(cid_period_cnt[0],cid_period_cnt[1],i),nasdaq_stmt_path(cid_period_cnt[0],cid_period_cnt[1],i))



class TaskMaster(object):
	"""docstring for TaskMaster"""
	def __init__(self):
		super(TaskMaster, self).__init__()
		self.task_specs = []
		# conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5')
		
	def get_tasks(self):
		conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='FinDW')

		sql = 'SELECT * FROM vw_stmt_download_requests'
		conn.execute_query(sql)
		for row in conn:
			print(row)
			self.task_specs.append((row['CID'],row['period_cnt']))
		conn.close()

	def start_tasks(self):
		pool = mp.Pool()
		res = pool.map_async(download_all3,self.task_specs)	
		syms_cids = res.get(timeout=len(self.task_specs)*1.5)

if __name__ == '__main__':
	tm = TaskMaster()
	tm.get_tasks()
	tm.start_tasks()