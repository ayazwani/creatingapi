
import xml.dom.minidom,csv,glob
import os
from flask import Flask, flash, request, redirect, url_for,jsonify
from werkzeug.utils import secure_filename
import funxml

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






@app.route("/search")
def read_csv():
	csv_file_path = 'classcsv.csv'
	data={}

	with open(csv_file_path) as csvf:
		csv_reader = csv.DictReader(csvf)
		for index ,row in enumerate(csv_reader):
			nct_id = row["nct_id"]
			condition = row["condition"]
			facility_name = row["facility_name"]
			data[nct_id]={}
			data[nct_id]['condition']= condition
			data[nct_id]['facility_name']=facility_name
	return jsonify(data)


@app.route("/find1/<string:str1>")
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
				return jsonify(data)
			break
		else:
			return("hello")







if __name__ == "__main__":
	app.run(debug=True)