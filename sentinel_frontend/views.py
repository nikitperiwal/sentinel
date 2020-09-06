from django.shortcuts import render
from django.http import HttpResponse
from twitter_sentiment.tweets import TweetClass

t = TweetClass()


def dashboard(request):
	if request.method == "POST":
		keywords = request.POST['keywords']
		exclude = request.POST['excludeWords']
		startDate = request.POST['startDate']
		endDate = request.POST['endDate']
		dailyNum = request.POST['dailyNum']
		t.scrape_tweets(keywords, exclude, startDate, endDate, dailyNum)
		
	context = t.get_context()
	return render(request, "dashboard.html", context)


def tweets(request):
	context = dict()
	context['tweetDF'] = t.tweet_df
	return render(request, "tweets.html", context)


def analytics(request):
	context = t.get_context()
	return render(request, "analytics.html", context)


def visualclouds(request):
	context = dict()
	return render(request, "visualclouds.html", context)


def support(request):
	return render(request, "support.html")


def download_data(request):
	resp = HttpResponse(content_type='text/csv')
	resp['Content-Disposition'] = 'attachment; filename=tweetData.csv'
	t.tweet_df.to_csv(path_or_buf=resp, sep=',', index=False)
	return resp
