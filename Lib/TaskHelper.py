from Task import Task

counter = 0

def update_taskqueue(task_queue, twitter_sessions):
	global counter
	for name in twitter_sessions:
		task_queue.put(name, Task(name, counter))
		counter += 1
