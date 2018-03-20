from flask import Flask, jsonify
from flask import request as rq
import random
import MySQLdb, json

app = Flask(__name__)

db = MySQLdb.connect("localhost","root", "root", "sayr-sapata")
cursor = db.cursor()

def make_packet(_status, _response):
	return jsonify(status = _status, response = _response)

@app.route('/set_guide_gps',methods=['POST','GET'])
def get_guide_gps():
	data = rq.get_json()
	
	already_available = False	
	cursor.execute("SELECT * FROM location WHERE gid=%s", (data['gid']))
	rows = cursor.fetchall()
	if len(rows) == 1:
		already_available = True

	try:

		if already_available:
			cursor.execute("UPDATE location SET lat=%s, lng=%s WHERE gid=%s",(str(data['gid']),str(data['lat']),str(data['lng'])))
			db.commit()
		else:
			cursor.execute("INSERT INTO location VALUES(%s,%s,%s)",(str(data['gid']),str(data['lat']),str(data['lng'])))
			db.commit()
	except Exception, err:
		db.rollback()
		return make_packet("ERROR", "Some Error Occurred!")

	return make_packet("SUCCESS", "OK")
	
@app.route('/get_guide_gps',methods=['POST','GET'])
def fetch_guide_gps():
	data = rq.get_json()
	
	cursor.execute("SELECT * FROM location")
	rows = cursor.fetchall()
	
	data = []
	for row in rows:
		data.append({'gid': row[0], 'lat': row[1], 'lng': row[2]})

	return make_packet("SUCCESS", data)	
	

if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0")
