import xml.dom.minidom,csv,glob


def get_nctid(root):
	nct_id=root.getElementsByTagName("nct_id")
	return(nct_id[0].firstChild.data)

def get_condition(root):
	l1=[]
	condition=root.getElementsByTagName("condition")
	for i,tags in enumerate(condition):
		l1.append(condition[i].firstChild.data)
		l1.append("|")
	str1 = ''.join(map(str,l1))
	return str1

def get_sampling(root):
	if(root.getElementsByTagName("sampling_method")):
		sampling_method = root.getElementsByTagName("sampling_method")
		return(sampling_method[0].firstChild.data)
	else:
		return("NA")

def get_name(root):
	if(root.getElementsByTagName("name")):
		name = root.getElementsByTagName("name")
		return(name[0].firstChild.data)
	else:
		return("NA")

def get_city(root):
	if(root.getElementsByTagName("city")):
		city = root.getElementsByTagName("city")
		return(city[0].firstChild.data)
	else:
		return("NA")


def get_overall_status(root):
	if(root.getElementsByTagName("overall_status")):
		overall_status = root.getElementsByTagName("overall_status")
		return(overall_status[0].firstChild.data)
	else:
		return("NA")




data = []




testdata = open('classcsv.csv', 'w')
csvwriter = csv.writer(testdata)
csvwriter.writerow(["nct_id","condition","facility_name","city","sampling_method","overall_status"])

data_folder="search_result"
for filename in glob.iglob(data_folder+"/*.xml"):

	domtree = xml.dom.minidom.parse(filename)

	root = domtree.documentElement

	data.append(get_nctid(root))

	data.append(get_condition(root))

	data.append(get_name(root))

	data.append(get_city(root))

	data.append(get_sampling(root))
	data.append(get_overall_status(root))
	#data.append(ob1.get_criteria_textblock(root))


	csvwriter.writerow(data)
	#print(data)
	data.clear()



testdata.close()