import re
from collections import defaultdict, Counter


def format_dict(d):
	name = list(d.keys())
	freq = list(d.values())
	return [name, freq]
	

def divide_data(dataframe, num_words=200, unique=True):
	positive = " ".join(dataframe[dataframe.sentiment == 1].processed_text).split()
	negative = " ".join(dataframe[dataframe.sentiment == -1].processed_text).split()
	
	# Creates a frequency dict for positive/negative words.
	positive_dict = defaultdict(int)
	negative_dict = defaultdict(int)
	for x in positive:
		positive_dict[x] += 1
	for x in negative:
		negative_dict[x] += 1
	
	# Create a list of words common in both positive/negative dict.
	common_words = list()
	if len(negative_dict) > len(positive_dict):
		for k in negative_dict.keys():
			if k in positive_dict.keys():
				common_words.append(k)
	else:
		for k in positive_dict.keys():
			if k in negative_dict.keys():
				common_words.append(k)
	
	# Removes common words from dictionary if Unique=True.
	if unique:
		for word in common_words:
			negative_dict.pop(word)
			positive_dict.pop(word)
	
	# Selects words with highest frequencies.
	common_positive = dict(Counter(positive_dict).most_common(num_words))
	common_negative = dict(Counter(negative_dict).most_common(num_words))
	
	return format_dict(common_positive), format_dict(common_negative)


def get_words(text_list, num_words=50):
	word_list = " ".join(text_list).split()
	word_list = dict(Counter(word_list).most_common(num_words))
	return format_dict(word_list)


def get_mentions(text_list, num_words=50):
	mentions = []
	re_user = r"@[A-Za-z0-9_]+"
	
	for text in text_list:
		users = re.findall(re_user, text)
		mentions.extend(users)
	
	mentions = dict(Counter(mentions).most_common(num_words))
	return format_dict(mentions)


def get_hashtags(text_list, num_words=50):
	hashtags = []
	re_hash = r"#[A-Za-z0-9-_]+"
	
	for text in text_list:
		tags = re.findall(re_hash, text)
		hashtags.extend(tags)
	
	hashtags = dict(Counter(hashtags).most_common(num_words))
	return format_dict(hashtags)
