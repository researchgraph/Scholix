
# coding: utf-8

# # Setup

# In[ ]:


import os, sys, glob, json
import pprint as pp
import requests
from requests.utils import requote_uri
import sqlite3
import codecs
# from importlib import reload
# reload(sys)
# sys.setdefaultencoding('utf8')

localDB='doi_prefixes.db'
doi_table_name = 'dois'
prefix_table_name = 'prefixes'
fld_prefix='prefix'
fld_count='cnt'
fld_org='org'
fld_file='file'
fld_doi='doi'

dois={}
prefixes={}


# ## Create DB

# In[ ]:


db = sqlite3.connect(localDB)
cur = db.cursor()  
# Creating DOIs
sql='CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1},{nf2} {ft2},{nf3} {ft3},{nf4} {ft4}, PRIMARY KEY ({nf1}, {nf2}))'            .format(tn=doi_table_name,                    nf1=fld_file, ft1='TEXT',                    nf2=fld_doi, ft2='TEXT',                    nf3=fld_prefix, ft3='TEXT',                    nf4=fld_count, ft4='INTEGER')
cur.execute(sql) 
# Creating Prefixes
sql='CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1} PRIMARY KEY, {nf2} {ft2})'            .format(tn=prefix_table_name, nf1=fld_prefix, ft1='TEXT', nf2=fld_org, ft2='TEXT')
print(sql)
cur.execute(sql) 
# Close the connection
db.commit()
db.close()


# # Process nodes

# In[ ]:


def processNode(node):  
    #pp.pprint(node['Identifier']['IDScheme'])
    if node['Identifier']['IDScheme']=='doi':
        doi=node['Identifier']['ID'].replace("'","")
        if doi in dois:
            dois[doi]=dois[doi]+1
        else:
            dois[doi]=1


# In[ ]:


def listPrefixes():
    for d in dois:
        p= d.split('/')[0]
        if p in prefixes:
            prefixes[p]= prefixes[p]+1
        else:
            prefixes[p]=1


# In[ ]:


def importDOIs(fname):
    db = sqlite3.connect(localDB)
    cur = db.cursor()   
    for doi in dois:
        p= doi.split('/')[0]
        if p in prefixes:
            prefixes[p]= prefixes[p]+1
        else:
            prefixes[p]=1        
        sql="INSERT INTO {tn} ({nf1}, {nf2}, {nf3},{nf4}) VALUES('{val1}', '{val2}', '{val3}','{val4}')"             .format(tn=doi_table_name, nf1=fld_file,nf2=fld_doi,nf3=fld_prefix,nf4=fld_count,                     val1=fname,val2=doi,val3=p,val4=dois[doi])
        cur.execute(sql)        
    db.commit()
    db.close()


# In[ ]:


def importPrefixes():
    db = sqlite3.connect(localDB)
    cur = db.cursor()   
    for prefix in prefixes:
        sql="INSERT or IGNORE INTO {tn} ({nf1}, {nf2}) VALUES('{val1}', '{val2}')"             .format(tn=prefix_table_name, nf1=fld_prefix,nf2=fld_org,                     val1=prefix,val2='-')
        cur.execute(sql)        
    db.commit()
    db.close()


# In[ ]:


def main(path):
    path = '{}/*.json'.format(path)
    for fname in glob.glob(path):
        pp.pprint(fname)
        #f= codecs.open(fname, encoding='utf-8')
        f= open(fname, 'r')
        lines = f.readlines()
        f.close()
        print ('{} lines are in {}'.format(len(lines),fname))
        for line in lines:
            data = json.loads(line)
            #pp.pprint(data)
            processNode(data['Source'])
            processNode(data['Target'])          
        importDOIs(fname)
        listPrefixes()
        importPrefixes()
        dois.clear();
        prefixes.clear();
    print('done!')


# In[ ]:


main('dump')


# In[ ]:


if __name__ == '__main__':
    main(sys.argv[1])


# In[ ]:



# urlString= 'https://api.datacite.org/prefixes'
# r = requests.get(urlString)
# for d in r.json()['data']:
#     pp.pprint('{} - {}'.format(d['id'],d[])

