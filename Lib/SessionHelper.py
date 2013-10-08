"""This is the helper for :class:`Lib.TwitterSession.TwitterSession`. 
	Dealing with the operations related to TwitterSession.
"""

from TwitterAccount import TwitterAccount
from TwitterSession import TwitterSession

def update_sessions(twitter_sessions, task_queue):
	"""Update the twitter_sessions from database.
		And renew the tubes in the task_queue.
	"""
	acc_list = TwitterAccount.get_list()
	acc_list_pk_list = [acc.pk for acc in acc_list]
	twitter_sessions_acc_pk_list = [ses.account.pk for ses in twitter_sessions]
	# remove sessions from origin twitter_sessions which are no longer active
	remove_session_index_list = []
	remove_session_acc_pk_list = []
	for i in range(len(twitter_sessions_acc_pk_list)):
		if twitter_sessions_acc_pk_list[i] not in acc_list_pk_list:
			remove_session_index_list.append(i-len(acc_list))
			remove_session_acc_pk_list.append(twitter_sessions_acc_pk_list[i])
	for index in remove_session_index_list:
		twitter_sessions.remove(twitter_sessions[index])
	# refresh the account data of the existing twitter_sessions
	for twitter_session in twitter_sessions:
		twitter_session.account.refresh()
	# add sessions which are new for twitter_sessions
	new_twitter_sessions = []
	for acc in acc_list:
		if acc.pk not in twitter_sessions_acc_pk_list:
			new_session = TwitterSession(acc)
			new_twitter_sessions.append(new_session)
	twitter_sessions.extend(new_twitter_sessions)
	# update the tubes of task_queue
	for pk in remove_session_acc_pk_list:
		task_queue.remove_tube(pk)
	for session in new_twitter_sessions:
		task_queue.add_tube(session.account.pk)
