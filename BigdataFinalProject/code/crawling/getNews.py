from newsplease import NewsPlease
import json
i = 1
articles = NewsPlease.from_file('/Users/wyw/Box/6350/Project/URLsplit/URLs260k'+str(i)+'.txt')
# print (article.text)
count = 0
with open ('/Users/wyw/Box/6350/Project/OutputSet/output'+str(i)+'.json', 'w') as outfile:	
	for url in articles:
		if articles[url].text != None and len(articles[url].text) > 10:
			count += 1
			json.dump(articles[url].__dict__, outfile, default=str, sort_keys=True)
			outfile.write('\n')
	print (count)
