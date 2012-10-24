"""
Scrapes the big-boards site for a list of forums and annotates a forum
with the ontology
"""

#!/usr/bin/env python

from bs4 import BeautifulSoup

import ast
import sys
import urllib
import urllib2


DIRECTORY_BIG_BOARDS_URL = "http://directory.big-boards.com"
BIG_BOARDS_URL = "http://big-boards.com"


def traverse(link_list):
	"""
	Visits links, pulls forums and stuff
	"""

	ontology_links_map = {}

	for item in link_list:
		ontology_links_map[item[0].contents[0]] = {}

		our_dict = ontology_links_map[item[0].contents[0]]

		for sub_items in item[1:]:
			our_dict[sub_items.contents[0]] = DIRECTORY_BIG_BOARDS_URL +  sub_items['href']

	return ontology_links_map

def collect_forum_links(ontology):
	new_ontology = {}

	for top_level_ontology in ontology.keys():
		new_ontology[top_level_ontology] = {}
		for l2 in ontology[top_level_ontology].keys():
			new_ontology[top_level_ontology][l2] = {}
			ranking_url = ontology[top_level_ontology][l2]
			rankings_page = urllib.urlopen(ranking_url)
			soup = BeautifulSoup(rankings_page.read())
			
			out_id_to_link_map = fetch_id_link_map(soup)
			rankings_table = soup.find("div", {"id": "rankings"}).find("table")

			outlinks = rankings_table.findAll("a", id=lambda x: x and x.startswith("out"))

			for outlink in outlinks:
				try:
					new_ontology[top_level_ontology][l2][outlink.contents[0]] = out_id_to_link_map[int(outlink['id'].replace("out", ""))]
				except IndexError:
					new_ontology[top_level_ontology][l2]["NONAME"] = out_id_to_link_map[int(outlink['id'].replace("out", ""))]

	return new_ontology

def fetch_id_link_map(soup):
	tbf = soup.findAll("script")[-1].contents[0]
	tbf = tbf.replace("<!--\n", "")
	tbf = tbf.replace("\n-->", "")
	tbf = tbf.replace("urls=", "")

	return ast.literal_eval(tbf)

def print_links(ontology):

	for l1 in ontology.keys():
		for l2 in ontology[l1].keys():
			for forum in ontology[l1][l2].keys():

				try:
					sys.ontology_links.write(l1 + "\t" + l2 + "\t" + forum + "\t" + ontology[l1][l2][forum] + "\n")
					sys.just_links.write(ontology[l1][l2][forum] + "\n")

					sys.ontology_links.flush()
					sys.just_links.flush()

				except:
					sys.fuck_ups.write(ontology[l1][l2][forum] + "\n")


if __name__ == "__main__":
	dir_bboard = urllib.urlopen(DIRECTORY_BIG_BOARDS_URL)
	soup = BeautifulSoup(dir_bboard.read())

	rows = soup.findAll("tr")

	full_ontology = []

	for row in rows:
		cells = row.findAll("td")
		for cell in cells:
			links = cell.findAll("a")
			full_ontology.append(links)

	sys.ontology_links = open("ontology_and_link.txt", "w")
	sys.just_links = open("links.txt", "w")
	sys.fuck_ups = open("fuck_ups.txt", "w")

	print_links(
		collect_forum_links(
			traverse(
				full_ontology
			)
		)
	)