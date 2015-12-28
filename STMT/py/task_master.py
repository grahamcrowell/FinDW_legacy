import _mssql
import os, time, multiprocessing as mp, datetime
import tools


class TaskMaster(object):
	"""docstring for TaskMaster"""
	def __init__(self):
		super(TaskMaster, self).__init__()
		self.task_specs = []
		self.pool = mp.Pool()
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
		res = self.pool.map_async(tools.download_all3,self.task_specs)	
		syms_cids = res.get(timeout=len(self.task_specs)*1.5)

	def parse_all(self):
		html_paths = tools.get_paths(tools.stmt_html)
		res = self.pool.map_async(tools.parse_stmt,html_paths)	
		syms_cids = res.get(timeout=len(self.task_specs)*1.5)

if __name__ == '__main__':
	tm = TaskMaster()
	# tm.get_tasks()
	# tm.start_tasks()
	tm.parse_all()