"""This is the helper for some general stuff."""

import os

def file2list(file_path,NoDup=True):
    """Return a list converted from the given file_path, split by lines.
    """
    mylst = []
    if not os.path.exists(file_path):
        open(file_path,'w')
    lines = open(file_path).readlines()
    for line in lines:
        if line.strip()!='':
            mylst.append(line.strip())
    if NoDup:
        temp_dict = {}
        for item in mylst:
            temp_dict[item] = 0
        mylst = []
        for key in temp_dict.keys():
            mylst.append(key)
    return mylst

def randpick(pick_num,orig_list):
    """Return a list of items randomly from a list.
    """
    from random import sample
    return sample(orig_list, pick_num)

def Username2Userid(l_username):
    """Return a int indicating the id of the l_username.
    """
    import requests
    import re
    import bsddb
    import string
    db = bsddb.hashopen('name2id.db')
    l_username = l_username.decode("cp1252").encode('ascii','ignore').translate(string.maketrans("",""), ''.join(string.punctuation.split('_'))+' ')
    if l_username in db:
        if db[l_username][0] == '-':
            return abs(int(db[l_username]))
        else: 
            return unicode(db[l_username])
    l_url = 'https://twitter.com/'+l_username
    l_r = requests.get(l_url)
    m = re.search('<div class="profile-card-inner" data-screen-name=".+?" data-user-id=".+?">',l_r.text)
    if m == None:
        db[l_username] = str(-l_r.status_code)
        return l_r.status_code
    m = re.search('data-user-id=".+?"',m.group(0))
    m = m.group(0)[14:-1]
    if len(m)>0:
        db[l_username] = m
        return m
    db[l_username] = str(-l_r.status_code)
    return l_r.status_code
    
def Userid2Username(l_userid):
    from MyDict import INTEREST_NAME_DICT
    l_userid = str(l_userid)
    return INTEREST_NAME_DICT[l_userid]

def Intstid2Intstname(l_intstid):
    import bsddb
    l_intstid = str(l_intstid)
    nidb = bsddb.hashopen('name2id.db')
    indb = bsddb.hashopen('id2name.db')
    if l_intstid in indb:
        return indb[l_intstid]
    p = nidb.first()
    while 1:
        if p[1] == l_intstid:
            indb[l_intstid] = p[0]
            return p[0]
        try: p = nidb.next()
        except Exception, e: return 'unknown'

