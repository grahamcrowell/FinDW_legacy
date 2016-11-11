import _mssql
import os, time, multiprocessing as mp, datetime
import tools


class TaskMaster(object):
	"""docstring for TaskMaster"""
	def __init__(self):
		super(TaskMaster, self).__init__()
		# conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5')
		
	def execute_download(self):
		conn = _mssql.connect(server='PC\\', user='PC\\user', password='2and2is5', database='FinDW')
		task_specs = []
		sql = 'SELECT * FROM vw_stmt_download_requests'
		conn.execute_query(sql)
		for row in conn:
			print(row)
			task_specs.append((row['CID'],row['period_cnt']))
		conn.close()
		if len(task_specs) > 0:
			pool = mp.Pool()
			res = pool.map_async(tools.download_all3,task_specs)	
			syms_cids = res.get(timeout=len(task_specs)*1.5)

	def execute_parse(self):
		html_paths = tools.get_paths(tools.stmt_html)
		if len(html_paths) > 0:
			pool = mp.Pool()
			res = pool.map_async(tools.parse_stmt,html_paths)	
			syms_cids = res.get(timeout=len(html_paths)*1.5)

if __name__ == '__main__':
	tm = TaskMaster()
	tm.execute_download()
	tm.execute_parse()