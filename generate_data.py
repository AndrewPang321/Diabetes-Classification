## JWALAPURAM PRATHYUSHA - Data Mining CI6227 - Assignment: Data Generation Script
##
## Run the script with 3 parameters: number of records for training; (will automatically generate development and testing records of size 30% of training records), e.g.:
##          > python generate_data.py 1000 
##

import sys
import sqlite3
import random

def dbcon():
	try:
		conn = sqlite3.connect("medical_records_{}.db".format(sys.argv[1]))
		
		return conn
	except:
		raise

def save_to_db(generated_records, table_name):
	try:
		connection = dbcon()
		query = "CREATE TABLE IF NOT EXISTS patient_info_{} (gender TEXT, weight FLOAT, heart_rate INT, blood_pressure_systolic INT, blood_pressure_diastolic INT, blood_sugar FLOAT, family_history TEXT, age INT, physical_activity TEXT, cholesterol INT, diagnosis TEXT)".format(table_name)
		
		connection.execute(query)
		for patient_record in generated_records:
				query = "INSERT INTO patient_info_{} VALUES(?,?,?,?,?,?,?,?,?,?,?)".format(table_name)    #12
				connection.execute(query, (patient_record['gender'], patient_record['weight'], patient_record['heart_rate'], patient_record['blood_pressure_systolic'], patient_record['blood_pressure_diastolic'], patient_record['blood_sugar'], patient_record['family_history'], patient_record['age'], patient_record['physical_activity'], patient_record['cholesterol'], patient_record['diagnosis'])) 
		connection.close()		
	except:
		raise

def set_attribute_values():
	attribute_values = {}
	attribute_values['gender'] = ['Male', 'Female', 'Other']
	attribute_values['weight'] = range(10,120) #kg
	attribute_values['heart_rate'] = range(60,130) #bpm
	attribute_values['blood_pressure_systolic'] = range(60,200) #mm Hg?
	attribute_values['blood_pressure_diastolic'] = range(50,120)
	attribute_values['blood_sugar'] = [x/10 for x in range(30,100)] #mmol/L divide by 10 to get float values 
	attribute_values['family_history'] = ['Parent', 'Grandparent', 'Sibling', 'None']
	attribute_values['age'] = range(10,100)
	attribute_values['physical_activity'] = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'None']
	attribute_values['cholesterol'] = range(100,300) #mg/dL

	return attribute_values

def set_attribute_weights(attribute_values):
	attribute_weights = {}

	for key in attribute_values.keys():
		attribute_weights[key] = {}
	
	attribute_weights['gender']['Male'] = 1.1
	attribute_weights['gender']['Female'], attribute_weights['gender']['Other'] = 1,1
	attribute_weights['heart_rate'][tuple([60,130])] = 1
	attribute_weights['family_history']['Parent'] = 1.5
	attribute_weights['family_history']['Sibling'] = 1.7
	attribute_weights['family_history']['Grandparent'] = 1.2
	attribute_weights['physical_activity']['Daily'] = 0.2
	attribute_weights['physical_activity']['Weekly'] = 0.6
	attribute_weights['physical_activity']['Monthly'] = 0.8
	attribute_weights['physical_activity']['Rarely'] = 1.2
	attribute_weights['physical_activity']['None'] = 1.8
	attribute_weights['weight'][tuple([10,75])] = 1
	attribute_weights['weight'][tuple([75,100])] = 1.5
	attribute_weights['weight'][tuple([100,120])] = 1.9
	attribute_weights['blood_pressure_systolic'][tuple([60,130])] = 1
	attribute_weights['blood_pressure_systolic'][tuple([130,150])] = 1.4
	attribute_weights['blood_pressure_systolic'][tuple([150,200])] = 1.8
	attribute_weights['blood_pressure_diastolic'][tuple([50,90])] = 1
	attribute_weights['blood_pressure_diastolic'][tuple([90,120])] = 1.5
	attribute_weights['blood_sugar'][tuple([3,5.5])] = 1
	attribute_weights['blood_sugar'][tuple([5.5,7])] = 1.3
	attribute_weights['blood_sugar'][tuple([7,10])] = 2
	attribute_weights['cholesterol'][tuple([100,200])] = 1
	attribute_weights['cholesterol'][tuple([200,240])] = 1.4
	attribute_weights['cholesterol'][tuple([240,300])] = 1.8
	attribute_weights['age'][tuple([10,35])] = 1
	attribute_weights['age'][tuple([35,60])] = 1.5
	attribute_weights['age'][tuple([60,100])] = 1.8

	return attribute_weights   


def generate_label(patient_record, attribute_weights):
	score = 1.0
	for key in patient_record.keys():
		try:
			attrib_score = attribute_weights[key][patient_record[key]]
		except KeyError:
			for limits in attribute_weights[key].keys():
				if patient_record[key] >= limits[0] and patient_record[key] < limits[1]:
					attrib_score = attribute_weights[key][limits]
					break
		score *= attrib_score
	#print(score)

	if score <=5:
		return "Not Diabetic"
	elif score >5 and score < 10:
		return "Pre-Diabetes"
	elif score >=10:
		return "Diabetic"

def generate_records(train_size, dev_size, test_size, attribute_values, attribute_weights):
	
	dataset_size = train_size + dev_size + test_size
	train_records = []
	dev_records = []
	test_records = []

	for i in range(dataset_size):
		patient_record = {}
		for attrib in attribute_values.keys():
			
			patient_record[attrib] = random.choice(attribute_values[attrib])
		
		#print(patient_record)
		
		#LABEL GENERATION
		patient_record['diagnosis'] = generate_label(patient_record, attribute_weights)
				
		if i < train_size:
			#print("train")
			train_records.append(patient_record)
			
		elif i < train_size + dev_size:
			#print("dev")
			dev_records.append(patient_record)
			
		else:
			#print("test")
			test_records.append(patient_record)
			
	
	save_to_db(train_records, "train")
	save_to_db(dev_records, "dev")
	save_to_db(test_records, "test")


if __name__ == "__main__":
	train_size = int(sys.argv[1])
	dev_size = train_size // 3
	test_size = train_size // 3

	attribute_values = set_attribute_values()	
	attribute_weights = set_attribute_weights(attribute_values)

	generate_records(train_size, dev_size, test_size, attribute_values, attribute_weights)
