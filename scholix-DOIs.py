
# coding: utf-8

# # List DOI Prefixes

# In[ ]:


import os, sys, glob, json
import pprint as pp

dois=[]
prefixes=[]

def processNode(node):
    for i in node['identifiers']:
        if i['schema']=='doi':
            identifier=i['identifier']
            if identifier not in dois:
                dois.append(identifier)    

def listPrefixes():
    for d in dois:
        p= d.split('/')[0]
        if p not in prefixes:
            prefixes.append(p)

def main(path):
    path = '{}/*.json'.format(path)
    for fname in glob.glob(path):
        data = json.load(open(fname))
        for l in data:
            if len(dois)<1000:
                processNode(l['source'])
                processNode(l['target'])
            else:
               break
    listPrefixes()
    pp.pprint(prefixes)


# In[ ]:


if __name__ == "__main__":
     main(sys.argv[1])

