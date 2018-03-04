
# coding: utf-8

# # Get List of Data Sources

import requests, os
from requests.utils import requote_uri
urlString= 'https://api-dliservice-prototype-dli.d4science.org/v1/listDatasources'
r = requests.get(urlString)

#Create a URL encoded list of data sources
dataSources=[];
for ds in r.json():
    if len(ds.strip())>0:
        dataSources.append(requote_uri(ds))
        
        
#Print name of datasources
count=0
for ds in dataSources:
    print('{}. {}'.format(count,ds))
    count=count+1
    
print('We found {} data sources.'.format(count))


# # Download files for a given datasource

SelectedDataSources={4,8}

#Create local folder for the data sources
for i in SelectedDataSources:
    ds=dataSources[i]
    if not os.path.exists(ds):
        print ('Creating new folder: {}'.format(ds))
        os.makedirs(ds)
    else:
        print ('We found a local folder for: {}'.format(ds))


#Download
maximumPages=100

for i in SelectedDataSources:
    ds=dataSources[i]
    page=0
    statusCode=200
    while (statusCode==200 and page < maximumPages):
        urlString= 'https://api-dliservice-prototype-dli.d4science.org/v1/linksFromDatasource?datasource={}&page={}'.format(ds,page)
        r = requests.get(urlString)
        fileName='{}.json'.format(1000000+page)
        myfile = open('./{}/{}'.format(ds,fileName), 'w')
        myfile.write(r.text)
        statusCode= r.status_code
        page = page + 1
        myfile.close
        if page%100==0:
            print('We have downloaded {} files for {}'.format(page,ds))


# # END
