from Task import Task
from TaskFactory import TaskFactory

def update_taskqueue(task_queue, twitter_sessions):
	for twitter_session in twitter_sessions:
		# initialize taskfactory
		factory = TaskFactory(twitter_session)
		# generate tasks
		tasks = factory.get_delete_tasks()
		tasks.extend(factory.get_create_tasks())
		# check and generate update task
		tasks.append(factory.get_local_update_task())
		# put into queue
		for task in tasks:
			task_queue.put(twitter_session, task)
