import os,inspect

data_root = 'c:/users/user/data'
steps = ['holding','staging','archive']
tabs = ['stmt','price']
exts = ['html','csv']

if not os.path.exists(data_root):
	os.mkdir(data_root)
print('data_root: {}'.format(data_root))

for step in steps:
	step_path = os.path.join(data_root,step)
	if not os.path.exists(step_path):
		os.mkdir(step_path)
	for tab in tabs:
		tab_path = os.path.join(step_path,tab)
		if not os.path.exists(tab_path):
			os.mkdir(tab_path)
		for ext in exts:
			ext_path = os.path.join(tab_path,ext)
			if not os.path.exists(ext_path):
				os.mkdir(ext_path)

def get_paths(in_dir):
	full_path = lambda name: os.path.join(in_dir,name)
	pths_in = list(map(full_path,os.listdir(in_dir)))
	return pths_in

def get_out_path(in_path,out_dir,new_ext=None):
	if new_ext is not None:
		return os.path.join(out_dir,os.path.splitext(os.path.split(in_path)[1])[0]+'.csv')
	return os.path.join(out_dir,os.path.split(in_path)[1])

def make_stmt_filename(cid,per_cnt,stmt_code,date_str=None):
	if date_str is None:
		date_str = str(datetime.date.today())
	return '{}_{}_{}_{}.html'.format(cid,stmt_code,date_str,per_cnt)

def parse_stmt_filename(full_path):
	# extract filename
	name = full_path.replace('\\','/').split('/')[-1]
	# return cid,per_cnt,stmt_code,date from input
	cid,stmt_code,download_date,per_cnt = name.split('_')
	return cid,per_cnt,stmt_code,download_date