from django.shortcuts import render, redirect
from .article_query import get_queries
from .article_to_point import Articles2Points, Data2Articles
import json

# Create your views here.

def view_raw_results(request, *args, **kwargs):
	r = request.session
	if "topic" in r and "number_papers" in r and "pages" in r:
		query = r.get("topic")
		
		articles_per_page = r.get("number_papers")
		articles_per_page = min(articles_per_page, 100)
		articles_per_page = max(articles_per_page, 10)
		print(articles_per_page)
		
		pages = r.get("pages")
		pages = min(pages, 20)
		pages = max(pages, 1)
		print(pages)
		
		params = {
			'page':1,
	   		'pageSize':articles_per_page,
	   		'metadata':'true',
	   		'fulltext':'false',
	   		'citations':'false',
	   		'similar':'false',
	   		'duplicate':'false',
	   		'urls':'true',
	   		'faithfulMetadata':'false',
		}
		results = get_queries(query, pages, params)
		a2p = Articles2Points()
		articles = Data2Articles(results)
		a2p(articles)

		nodes = list(map(lambda a: a.dict, articles))

		links = []

		graph = {"nodes":nodes, "links":links}
		graph_json = json.dumps(graph)  #### data for the 3d-visual

		context = {
			"data": graph_json
		}
		
		return render(request, "vis.html", context)

	return redirect('/')

