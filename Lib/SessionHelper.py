def update_sessions(twitter_sessions, task_queue):
	twitter_sessions_from_db = ['1','2','3','4']
	new_twitter_sessions = [item for item in twitter_sessions_from_db if item not in twitter_sessions]
	for name in new_twitter_sessions:
		task_queue.add_tube(name)
	twitter_sessions.extend(new_twitter_sessions)
