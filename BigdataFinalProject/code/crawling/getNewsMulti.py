from newsplease import NewsPlease
import json
from datetime import datetime
articles = None
count = 0
for i in range(290, 306):
	print('Start on file number', i)
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	articles = NewsPlease.from_file('/Users/wyw/Box/6350/Project/URLsplit0506/URLs260k'+str(i)+'.txt')
	print('Finish newsplease at')
	print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	# print (article.text)
	count = 0
	with open ('/Users/wyw/Box/6350/Project/OutputSet0506/output'+str(i)+'.json', 'w') as outfile:	
		for url in articles:
			if articles[url].text != None and len(articles[url].text) > 500:
				count += 1
				json.dump(articles[url].__dict__, outfile, default=str, sort_keys=True)
				outfile.write('\n')
		print ('File', i, 'has', count, 'articles')
		print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
