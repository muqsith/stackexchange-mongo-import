import xml.parsers.expat
import json
from xml.sax.saxutils import escape
import subprocess
import os
import argparse
import functools
import configparser
from pymongo import MongoClient
from datetime import datetime
import shutil

#================= Load mongo-db.conf =========================
config = configparser.ConfigParser()
config.read('mongo-db.conf')
config = config['mongo']

#==============	Load config.json ==============================
json_config = None
def get_json_config():
	global json_config
	if json_config is None:
		with open('config.json','r') as f:
			json_config = json.load(f)
	return json_config
#==============================================================

#==============	Extract xml files =============================

def extract_7z_archive(archive_path):
	try:
		successful = False
		archive_name = archive_path.split(os.sep).pop()
		directory_path = archive_path.replace(os.sep+archive_name,'')
		extracted_directory = directory_path+os.sep+'d.'+archive_name
		if os.path.isdir(extracted_directory):
			shutil.rmtree(extracted_directory)
		out_bytes = \
			subprocess.check_output(['7z','x','-o' \
				+extracted_directory,archive_path])
		out_text = out_bytes.decode('utf-8')
		for l in out_text.split('\n'):
			if (l == 'Everything is Ok'):
				successful = True
				break
		if not successful:
			extracted_directory = ''
		return extracted_directory
	except:
		print("""
		 i. Please install 7zip if it is already not installed.
		 	$ sudo apt install p7zip-full
		ii. If you have installed 7zip, may be the bin folder is not in the path, please set(export) 7zip bin folder to environment path variable.
		""")
#==============================================================

def get_xml_files(dir_path):
	return [dir_path+os.sep+name for name in os.listdir(dir_path) \
		if ('.xml' in name and os.path.isfile(os.path.join(dir_path,name)))]

#==============================================================

def insert_docs(db=None, collection=None, data=None):
	doc = {}
	for key in data:
		config_object = get_json_config()[collection.name]['columns'][key]
		if config_object['type'] == 'int':
			doc[key] = int(data[key])
		elif config_object['type'] == 'datetime':
			doc[key] = datetime.strptime(data[key], \
				get_json_config()[collection.name]['columns'][key]['format'])
		else:
			d = data[key]
			s = escape(d, {'"':'&quot;'})
			s = s.replace('&amp;quot;','&quot;')
			doc[key] = s
	collection.insert_one(doc)

def insert_data(element, attrs):
	if element == 'row':
		insert_docs(data=attrs)


def insert_xml_data(xml_file, db):
	collection_name = xml_file.split(os.sep).pop().split('.')[0]
	collection = db[collection_name]
	global insert_docs
	insert_docs = functools.partial(insert_docs, \
			db=db, collection=collection)
	p = xml.parsers.expat.ParserCreate()
	p.StartElementHandler = insert_data
	with open(xml_file, 'rb') as f:
		p.ParseFile(f)


#==============================================================

def get_db_connection():
	mongo_url = 'mongodb://'+config['host']+':'+config['port']
	db = MongoClient(mongo_url)[config['database']]
	print('Connected to : ', mongo_url)
	return db

#=============== Main Function =================================

def xml2mongo(archive_path=None, xmls_dir=None):
	if archive_path:
		xmls_dir = extract_7z_archive(archive_path)
	xml_files = get_xml_files(xmls_dir)
	db = get_db_connection()
	for xml_file in xml_files:
		insert_xml_data(xml_file, db)

#==============================================================
