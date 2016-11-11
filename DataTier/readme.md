config schema

config.DataRefresh 
each row repersents an update request.  
	- DataSource {internet,???}
	- DestinationTable
	- RequestDate
	- CompleteDate
	- CurrentStage int (-1: error, 0:cancelled, 1:in_progress, 2:in_progress, 3:complete)


config.DataRefreshInfo
	- DestinationTable
	- CurrentStage
	- 
 {download_required,parse_required,load_required}


# data_refresh:

	for each stage in 1..3
		for each source with stage
			init worker_pool(stage, source)...
			for each task with stage, source
				init task_spec(task)
				do task_task with worker_pool
		wait for all work_pools to complete
