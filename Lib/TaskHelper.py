from Task import Task
from TaskFactory import TaskFactory

def update_taskqueue(task_queue, twitter_sessions):
	for twitter_session in twitter_sessions:
		factory = TaskFactory(twitter_session)
		tasks = factory.get_delete_tasks()
		tasks.extend(factory.get_create_tasks())
		tasks.append(factory.get_local_update_task())
		for task in tasks:
			task_queue.put(twitter_session, task)
