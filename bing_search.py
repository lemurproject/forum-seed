"""
Query wrapper around bing
"""

#!/usr/bin/env python

import sys
import json
import requests

SERVICE_ROOT_URL = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/"
CREDS_FILE_MAP = {}
KEYS = ["PRIMARY_ACC_KEY", "CUST_ID"]


def main(creds_file, queries_list):
	bing_id = load_credentials(creds_file)
	queries = load_queries_list(queries_list)

	for query in queries:
		collect_results(query, bing_id)

def load_credentials(creds_file):
	"""
	Loads up the ids using the file config.ini (Please store your stuff there)
	"""
	f = open(creds_file, "r")
	for new_line in f:
		return new_line

def load_queries_list(queries_list):
	results = []
	f = open(queries_list, "r")
	for new_line in f:
		results.append(new_line)
	return results[1:]

def collect_results(query, bing_id):
	"""
	Hit bing with the queries.
	collect resulting URLs (some might not be forums but w/e)
	"""
	skip_index = 0
	while True:
		url = SERVICE_ROOT_URL + build_query(query, bing_id, skip_index)
		skip_index += 50

		resps = send_to_bing(url, bing_id).json

		results_list = resps['d']['results'][0]['Web']

		for result in results_list:
			print result["Url"].encode('utf-8')
			sys.stdout.flush()

		if results_list == []:
			print "--- changing query-string ---"
			return

def send_to_bing(url, bing_id):
	"""
	hits the bing API with our queries
	"""
	return requests.get(url, auth=(bing_id, bing_id))


def build_query(query, bing_id, skip_index):
	"""
	"""
	bing_query_type = "Composite"
	bing_sources_key = "Sources"
	query_key = "Query"
	top_key = "$top"
	skip_key = "$skip"
	format_key = "$format"

	return bing_query_type + "?" + bing_sources_key + "=%27web%27" + "&" + query_key + "=%27" + query.strip().replace(" ", "%20") + "%27&" +  top_key + "=50&" + skip_key + "=" + str(skip_index) + "&" + format_key + "=json"

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])