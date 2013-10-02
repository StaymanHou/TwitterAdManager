"""This is the helper for :class:`Lib.Task.Task`. 
	Dealing with the operations related to Tasks.
"""

from Task import Task
from TaskFactory import TaskFactory
import DateTimeHelper
from datetime import datetime, timedelta

def update_taskqueue(task_queue, twitter_sessions):
	"""Update the task_queue. In following order:
		\n\t:func:`Lib.TaskFactory.TaskFactory.get_delete_tasks`
		\n\t:func:`Lib.TaskFactory.TaskFactory.get_create_tasks`
		\n\tThen, if it is another hour, :func:`Lib.TaskFactory.TaskFactory.get_local_update_task`
	"""
	for twitter_session in twitter_sessions:
		# initialize taskfactory
		factory = TaskFactory(twitter_session)
		# generate tasks
		tasks = factory.get_delete_tasks()
		tasks.extend(factory.get_create_tasks())
		# check and generate update task
		flag_hour_finished = twitter_session.account.monitor_finished_hour
		if flag_hour_finished == None:
			flag_hour_finished = DateTimeHelper.floorbyhour(datetime.now())-DateTimeHelper.onehour
		if datetime.now() >= flag_hour_finished+DateTimeHelper.onehour+DateTimeHelper.oneminute:
			tasks.append(factory.get_local_update_task(flag_hour_finished))
			twitter_session.account.set_monitor_finished_hour(flag_hour_finished+DateTimeHelper.onehour)
		# put into queue
		for task in tasks:
			task_queue.put(twitter_session.account.pk, task)
