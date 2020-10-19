import xml.dom.minidom,csv,glob
import os
from flask import Flask, flash, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import funx as fn
import requests

app = Flask(__name__)


UPLOAD_FOLDER = '/home/ayaz/Desktop/Applied Informatics/flask/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf','json','xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp



@app.route("/search",methods=['GET'])
def read_csv():
	csv_file_path = '1.csv'

	if request.args:
		l1=[]
		d = request.args.to_dict()
		for v in d.values():
			l1.append(v)
		csv_file_path = '1.csv'
		data={}
		with open(csv_file_path) as csvf:
			csv_reader = csv.DictReader(csvf)
			for index ,row in enumerate(csv_reader):
				data.setdefault(row["nct_id"],{})
				for x in l1:
					data[row["nct_id"]].update({x:row[x]})
	else:
		
		data={}
		with open(csv_file_path) as csvf:
			csv_reader = csv.DictReader(csvf)
			for index ,row in enumerate(csv_reader):
				nct_id = row["nct_id"]
				condition = row["condition"]
				facility_name = row["facility_name"]
				city = row["city"]
				data[nct_id]={}
				data[nct_id]['condition']= condition
				data[nct_id]['facility_name']=facility_name
				data[nct_id]['city']=city
	return jsonify(data)

@app.route("/findnct/<string:str1>")
def find(str1):
	csv_file_path = 'classcsv.csv'
	with open(csv_file_path) as csvf:
		csv_reader = csv.DictReader(csvf)
		data={}
		for index ,row in enumerate(csv_reader):
			nct_id=row["nct_id"]
			if nct_id == str1:
				condition = row["condition"]
				facility_name = row["facility_name"]
				data[nct_id]={}
				data[nct_id]['condition']= condition
				data[nct_id]['facility_name']=facility_name
				break
			else:
				return jsonify({"message":"nct_id not found"})
		return jsonify(data)

@app.route("/makecsv")
def make_csv():
	l1=[]
	data=[]
	testdata = open('1.csv', 'w')
	csvwriter = csv.writer(testdata)
	csvwriter.writerow(["nct_id","condition","facility_name","city","sampling_method","overall_status"])
	data_folder="search_result"
	for filename in glob.iglob(data_folder+"/*.xml"):
		domtree = xml.dom.minidom.parse(filename)
		root = domtree.documentElement
		data.append(fn.get_nctid(root))
		data.append(fn.get_condition(root))
		data.append(fn.get_name(root))
		data.append(fn.get_city(root))
		data.append(fn.get_sampling(root))
		data.append(fn.get_overall_status(root))
		csvwriter.writerow(data)
		data.clear()
	testdata.close()
	return jsonify({"message":"csv made"})


@app.route("/append")
def append1():
	data=[]
	testdata = open('1.csv', 'a')
	csvwriter = csv.writer(testdata)
	data_folder="upload"
	for filename in glob.iglob(data_folder+"/*.xml"):
		domtree = xml.dom.minidom.parse(filename)
		root = domtree.documentElement
		data.append(fn.get_nctid(root))
		data.append(fn.get_condition(root))
		data.append(fn.get_name(root))
		data.append(fn.get_city(root))
		data.append(fn.get_sampling(root))
		data.append(fn.get_overall_status(root))
		csvwriter.writerow(data)
		data.clear()
	testdata.close()
	return jsonify({"message":"csv_appended"})
















if __name__ == "__main__":
	app.run(debug=True)