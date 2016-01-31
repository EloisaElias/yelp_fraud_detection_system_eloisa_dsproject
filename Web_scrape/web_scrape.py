from bs4 import BeautifulSoup
from random import randint
from time import sleep
import datetime
import os
import requests
import string
import sys


debug = False

def format_filename(s):
	"""Take a string and return a valid filename constructed from the string.
	Uses a whitelist approach: any characters not present in valid_chars are
	removed. Also spaces are replaced with underscores.
	 
	Note: this method may produce invalid filenames such as ``, `.` or `..`
	When I use this method I prepend a date string like '2009_01_15_19_46_32_'
	and append a file extension like '.txt', so I avoid the potential of using
	an invalid filename.
	"""
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	filename = ''.join(c for c in s if c in valid_chars)
	filename = filename.replace(' ','_') # I don't like spaces in filenames.
	return filename

def retrieveAndSaveHtmls(urls):

	for url in urls:
		filename = format_filename(url) + ".html"
		if os.path.isfile(filename):
			print("Already saved HTML for " + url)
		else:
			print("Fetching: " + url)
			retrieveAndSaveHtml(url)
			sleep_random_duration(30,80)

def retrieveAndSaveHtml(url):

	headers = {
		'Host': 'www.yelp.com',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'http://www.yelp.com/',
		'Cookie': '',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0'
	}
	r = requests.get(url, headers=headers)
	
	if r.status_code == 200:
		filename = format_filename(url) + ".html"
		text_file = open(filename, "w")
		text_file.write(r.text)
		text_file.close()
	else:
		print("Ran into issue retrieving: " + url)


def get_all_not_recommended_reviews():
	urls = []
	#urls.append("http://www.yahoo.com")
	#for x in range(100):
	# print("urls.append(\"http://www.yelp.com/search?find_desc=Restaurants&find_loc=Pittsburgh,+PA&start=" + str(10*x) + "\")")
	# print("urls.append(\"http://www.yelp.com/search?find_desc=Restaurants&find_loc=Charlotte%2C+NC&start=" + str(10*x) + "\")")
	# print("urls.append(\"http://www.yelp.com/search?find_desc=Restaurants&find_loc=Urbana-Champaign,+IL&start=" + str(10*x) + "\")")
	# print("urls.append(\"http://www.yelp.com/search?find_desc=Restaurants&find_loc=Madison,+WI&start=" + str(10*x) + "\")")
	# print("urls.append(\"http://www.yelp.com/search?find_desc=Restaurants&find_loc=Las+Vegas,+NV&start=" + str(10*x) + "\")")
	# print("urls.append(\"http://www.yelp.com/search?find_desc=Restaurants&find_loc=Phoenix,+AZ&start=" + str(10*x) + "\")")
	
	ids = '''mon-ami-gabi-las-vegas-2
	wicked-spoon-las-vegas
	earl-of-sandwich-las-vegas
	pacos-tacos-and-tequila-charlotte-2
	mcmullans-irish-pub-las-vegas'''

	for id in ids.split("\n"):
		urls.append("http://www.yelp.com/not_recommended_reviews/" + id + "?not_recommended_start=0")

	retrieveAndSaveHtmls(urls)


def extract_business_data_ALL(directory):
	all_records = []
	for filename in list_business_data_files(directory):
		if debug:
			print("********PROCESSING: " + filename)
		records = extract_business_data(filename)
		all_records.extend(records)
	if debug:
		print("DONE. " + str(len(all_records)) + " records processed.")
	return all_records

def extract_non_recommendations_ALL(directory):
	all_records = []
	for filename in list_nonrecommendations_files(directory):
		if debug:
			print("********PROCESSING: " + filename)
		num_total_records, records = extract_non_recommended_review_data(filename)
		all_records.extend(records)
	if debug:
		print("DONE. " + str(len(all_records)) + " records processed.")
	return all_records

def generate_csv_of_non_recommendations(records, csvFilename):
	'''Fields in the CSV:
	name:              Kevin K.
	data_hovercard_id: u6xfsoqJBJg7MOKuev3OKQ
	friend_count:      0
	review_count:      2
	rating:            5.0
	rating_qualifier:  12/22/2015
	review:            reviewtext
	'''
	header = "\"name\"," \
	   "\"business_id\"," \
	   "\"data_hovercard_id\"," \
	   "\"friend_count\"," \
	   "\"rating\"," \
	   "\"rating_qualifier\"," \
	   "\"review\"\n"

	csv = open(csvFilename, 'w')
	csv.write(header)
	for r in records:
		line = "\"" + r['name'] + "\"," \
		   "\"" + r['business_id'] + "\"," \
		   "\"" + r['data_hovercard_id'] + "\"," \
		   "\"" + r['friend_count'] + "\"," \
		   "\"" + r['rating'] + "\"," \
		   "\"" + r['rating_qualifier'] + "\"," \
		   "\"" + r['review'] + "\"\n"
		csv.write(line)
	csv.close()


def generate_csv_of_extracted_business_data(records, csvFilename):
	'''Fields in the CSV:
	search_results_index:   169
	business_name:          Yama Asian Fusion
	business_id:            yama-asian-fusion-charlotte
	data_hovercard_id:      4wqd4ijuYrRBmUF5I6tvLg
	rating:                 4.0
	review_count:           118
	price_range:            $$
	neighborhood:           South Park
	address:                720 Governor Morrison St, Charlotte, NC 28211
	phone:                  (704) 295-0905
	categories:             Japanese, Asian Fusion, Sushi Bars
	searched_city:          Charlotte
	searched_state:         NC
	'''
	header = "\"search_results_index\"," \
	   "\"business_name\"," \
	   "\"business_id\"," \
	   "\"data_hovercard_id\"," \
	   "\"rating\"," \
	   "\"review_count\"," \
	   "\"price_range\"," \
	   "\"neighborhood\"," \
	   "\"address\"," \
	   "\"phone\"," \
	   "\"categories\"," \
	   "\"searched_city\"," \
	   "\"searched_state\"\n"

	csv = open(csvFilename, 'w')
	csv.write(header)
	for r in records:
		line = "\"" + r['search_results_index'] + "\"," \
		   "\"" + r['business_name'] + "\"," \
		   "\"" + r['business_id'] + "\"," \
		   "\"" + r['data_hovercard_id'] + "\"," \
		   "\"" + r['rating'] + "\"," \
		   "\"" + r['review_count'] + "\"," \
		   "\"" + r['price_range'] + "\"," \
		   "\"" + r['neighborhood'] + "\"," \
		   "\"" + r['address'] + "\"," \
		   "\"" + r['phone'] + "\"," \
		   "\"" + r['categories'] + "\"," \
		   "\"" + r['searched_city'] + "\"," \
		   "\"" + r['searched_state'] + "\"\n"
		csv.write(line)
	csv.close()


# returns [business_list]
def extract_business_data(filepath):

	records = []

	# read in the local file
	f = open(filepath).read()
	html = BeautifulSoup(f, "html.parser")
	x = html.findAll("div", {"class":"search-results-content"})[0]

	for zz in x.findAll("div", {"class": "main-attributes"}):
		for z in zz.findAll("div", {"class": "media-story"}):
			record = {}

			# business_name, data_hovercard_id, business_id
			for r in z.findAll("a", {"class": "biz-name"}):	
				record['business_name'] = r.span.get_text()
				record['data_hovercard_id'] = r['data-hovercard-id']
				if "adredir" in r['href']:
					# special case: we will ignore ads later on
					record['business_id'] = "advertisement"
				else:
					record['business_id'] = r['href'].split("/")[2]
				#print(r['href'])
				
			# rating
			rating = z.findAll("div", {"class": "rating-large"})
			if rating:
				for r in rating:
					record['rating'] = r.i['title'].split()[0]
			else:
				record['rating'] = "(none provided)"

		 	# search results index
			for r in z.findAll("span", {"class": "indexed-biz-name"}):
				record['search_results_index'] = r.get_text().split(".")[0]

			# review count
			review_count = z.findAll("span", {"class": "rating-qualifier"})
			if review_count:
				for r in review_count:
					record['review_count'] = r.get_text().split()[0]
			else:
				record['review_count'] = "0"

			# price range
			price_range = z.findAll("span", {"class": "price-range"})	
			if price_range:
				for r in price_range:
					record['price_range'] = r.get_text().strip()
			else:
				record['price_range'] = "???"	

			# categories
			categ = z.findAll("span", {"class": "category-str-list"})
			if categ:
				for r in categ:
					categories = []
					for a in r.findAll("a"):
						categories.append(a.get_text())
					record['categories'] = ", ".join(categories)
			else:
				record['categories'] = "(none provided)"

			records.append(record)

		
	# neighborhood, address, phone
	i =0
	for r in x.findAll("div", {"class": "secondary-attributes"}):
		records[i]['phone'] = r.findAll("span", {"class": "biz-phone"})[0].get_text().strip()

		neighborhoods = r.findAll("span", {"class": "neighborhood-str-list"})
		if neighborhoods:
			records[i]['neighborhood'] = neighborhoods[0].get_text().strip()
		else:
			records[i]['neighborhood'] = "(none provided)"

		address = str(r.address).strip()
		address = address.replace("<address>", "").strip()
		address = address.replace("</address>", "").strip()
		address = address.replace("</br>", "").strip()
		address = address.replace("<br>", ", ").strip()
		records[i]['address'] = address
		if "PA" in address:
			records[i]['searched_city'] = "Pittsburgh"
			records[i]['searched_state'] = "PA"
		elif "NV" in address:
			records[i]['searched_city'] = "Las Vegas"
			records[i]['searched_state'] = "NV"
		elif "AZ" in address:
			records[i]['searched_city'] = "Phoenix"
			records[i]['searched_state'] = "AZ"
		elif "IL" in address:
			records[i]['searched_city'] = "Urbana-Champaign"
			records[i]['searched_state'] = "IL"
		elif "WI" in address:
			records[i]['searched_city'] = "Madison"
			records[i]['searched_state'] = "WI"
		elif "NC" in address:
			records[i]['searched_city'] = "Charlotte"
			records[i]['searched_state'] = "NC"
		else:
			raise
		i = i+1

	# remove all ads
	records = [r for r in records if r['business_id'] != "advertisement"]

	# print all data
	if debug:
		for record in records:
			print("search_results_index:   " + record['search_results_index'])
			print("business_name:          " + record['business_name'])
			print("business_id:            " + record['business_id'])
			print("data_hovercard_id:      " + record['data_hovercard_id'])
			print("rating:                 " + record['rating'])
			print("review_count:           " + record['review_count'])
			print("price_range:            " + record['price_range'])
			print("neighborhood:           " + record['neighborhood'])
			print("address:                " + record['address'])
			print("phone:                  " + record['phone'])
			print("categories:             " + record['categories'])
			print("searched_city:          " + record['searched_city'])
			print("searched_state:         " + record['searched_state'])
			print("")

	return records



# returns [number_of_reviews, reviews_list]
def extract_non_recommended_review_data(filepath):

	records = []

	# read in the local file
	f = open(filepath).read()
	html = BeautifulSoup(f, "html.parser")
	x = html.findAll("div", {"class":"ysection not-recommended-reviews review-list-wide"})[0]

	num_reviews = x.h3.string.strip().split()[0]

	# usernames
	for r in x.findAll("li", {"class":"user-name"}):
		if r.findAll("span", {"class":"user-display-name"}):
			for t in r.findAll("span", {"class":"user-display-name"}):
				record = {}
				record['data_hovercard_id'] = t['data-hovercard-id']
				record['name'] = t.get_text()
				records.append(record)
		elif r.findAll("span", {"class": "ghost-user"}):
			for t in r.findAll("span", {"class": "ghost-user"}): 
				record = {}
				record['data_hovercard_id'] = '(none provided)'
				record['name'] = "Anonymous Qype Ghost User"
				records.append(record)

	# friend_counts
	i =0
	for r in x.findAll("li", {"class":"friend-count"}):
		records[i]['friend_count'] = r.span.b.get_text()
		i = i+1

	# review_counts
	i =0
	for r in x.findAll("li", {"class":"review-count"}):
		records[i]['review_count'] = r.span.b.get_text()
		i = i+1

	# ratings, rating qualifier
	i =0
	for z in x.findAll("div", {"class": "review-wrapper"}):
		for r in z.findAll("div", {"class":"rating-very-large"}):
			records[i]['rating'] = r.i['title'].split()[0]
		for r in x.findAll("span", {"class":"rating-qualifier"}):
			records[i]['rating_qualifier'] = r.get_text().strip()
		i = i+1

	# review
	i =0
	for r in x.findAll("div", {"class":"review-content"}):
		records[i]['review'] = r.p.get_text()
		i = i+1

	# business_id
	for record in records:
		for z in html.findAll("div", {"class": "top-return-links"}):
			record['business_id'] = z.a['href'].split("/")[2]

	# print all data
	if debug:
		for record in records:
			print("name:              " + record['name'])
			print("business_id:       " + record['business_id'])
			print("data_hovercard_id: " + record['data_hovercard_id'])
			print("friend_count:      " + record['friend_count'])
			print("review_count:      " + record['review_count'])
			print("rating:            " + record['rating'])
			print("rating_qualifier:  " + record['rating_qualifier'])
			print("review:            " + record['review'])
			print("")

	return [num_reviews, records]


def sleep_random_duration(min_seconds, max_seconds):
	seconds = randint(min_seconds,max_seconds)
	milliseconds = randint(0,999)
	total_sleep = float(seconds) + float(milliseconds)/1000.0
	if debug:
		print("Sleeping for a random duration between " + str(min_seconds) + " - " + str(max_seconds) + " seconds: " + str(total_sleep) + " seconds")
		print("   start: " + str(datetime.datetime.now().time()))
	sleep(total_sleep)
	if debug:
		print("     end: " + str(datetime.datetime.now().time()))


def list_files(directory_path):
	from os import listdir
	from os.path import isfile, join
	only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
	return only_files

def list_business_data_files(directory_path):
	business_data_files = [f for f in list_files(directory_path) if ("search" in os.path.basename(f))]
	return business_data_files

def list_nonrecommendations_files(directory_path):
	nonrecommendations_files = [f for f in list_files(directory_path) if ("not_recommended_reviews" in os.path.basename(f))]
	return nonrecommendations_files


#===================================================================
# MAIN SCRIPT
#===================================================================

if len(sys.argv) > 1:

	if sys.argv[len(sys.argv)-1] == "debug":
		debug = True

	if sys.argv[1] == "1":
		filename = sys.argv[2]
		num_records, records = extract_non_recommended_review_data(filename)
		generate_csv_of_non_recommendations(records, "/tmp/test.csv")

	if sys.argv[1] == "2":
		filename = sys.argv[2]
		records = extract_business_data(filename)
		generate_csv_of_extracted_business_data(records, "/tmp/test.csv")
	
	if sys.argv[1] == "3":
		min_seconds = int(sys.argv[2])
		max_seconds = int(sys.argv[3])
		sleep_random_duration(min_seconds, max_seconds)

	if sys.argv[1] == "4":
		get_all_not_recommended_reviews()

	if sys.argv[1] == "5":
		directory = sys.argv[2]
		print("\n".join(list_business_data_files(directory)))

	if sys.argv[1] == "6":
		directory = sys.argv[2]
		print("\n".join(list_nonrecommendations_files(directory)))

	if sys.argv[1] == "7":
		directory = sys.argv[2]
		extract_business_data_ALL(directory)

	if sys.argv[1] == "8":
		directory = sys.argv[2]
		csvFilename = sys.argv[3]
		records = extract_business_data_ALL(directory)
		generate_csv_of_extracted_business_data(records, csvFilename)

	if sys.argv[1] == "9":
		directory = sys.argv[2]
		records = extract_business_data_ALL(directory)
		for r in records:
			print(r['review_count'] + "   " + r['business_id'])

	if sys.argv[1] == "10":
		directory = sys.argv[2]
		extract_non_recommendations_ALL(directory)

	if sys.argv[1] == "11":
		directory = sys.argv[2]
		csvFilename = sys.argv[3]
		records = extract_non_recommendations_ALL(directory)
		generate_csv_of_non_recommendations(records, csvFilename)

	if sys.argv[1] == "12":
		t = 0
		directory = sys.argv[2]
		for filename in list_nonrecommendations_files(directory):
			if debug:
				print("********PROCESSING: " + filename)
			num_total_records, records = extract_non_recommended_review_data(filename)
			print(str(num_total_records) + "   " + records[0]['business_id'])
			t = t + int(num_total_records)
		print(t)

	if sys.argv[1] == "13":
		import math
		directory = sys.argv[2]
		for filename in list_nonrecommendations_files(directory):
			if debug:
				print("********PROCESSING: " + filename)
			num_total_records, records = extract_non_recommended_review_data(filename)
			id = records[0]['business_id']
			print("# " + str(num_total_records) + "   " + id)
			for j in range(int(math.floor((int(num_total_records)-1)/10.0))):
				print("urls.append(\"http://www.yelp.com/not_recommended_reviews/" + id + "?not_recommended_start=" + str(10*(j+1)) + "\")")
else:
	print()
	print("python web_scrape.py 1  <local_html_filepath> [debug]         extract non_recommended_review data")
	print("python web_scrape.py 2  <local_html_filepath> [debug]         extract business data")
	print("python web_scrape.py 3  <min_seconds> <max_seconds> [debug]   sleep a random number of seconds")
	print("python web_scrape.py 4  [debug]                               fetch URLs and save HTML to local files")
	print("python web_scrape.py 5  <directory> [debug]                   list business HTML files in directory")
	print("python web_scrape.py 6  <directory> [debug]                   list not-recommended reviews HTML files in directory")
	print("python web_scrape.py 7  <directory> [debug]                   extract ALL business data")
	print("python web_scrape.py 8  <directory> <csv_filename> [debug]    extract ALL business data and generate CSV file")
	print("python web_scrape.py 9  <directory> [debug]                   extract ALL business data, but only print business_id and review_count")
	print("python web_scrape.py 10 <directory> [debug]                   extract ALL non-recommendations")
	print("python web_scrape.py 11 <directory> <csv_filename> [debug]    extract ALL non-recommendations and generate CSV file")
	print("python web_scrape.py 12 <directory> [debug]                   count non-recommendations for each business_id")
	print("python web_scrape.py 13 <directory> [debug]                   generate links for non-recommendations HTML")
	print()

