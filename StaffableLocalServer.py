import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask, jsonify, request, render_template
from random import randint



app = Flask(__name__)


cred = credentials.Certificate('/Users/toddyu/Desktop/Projects/CalHacks2019/calhacks2019-8abc9-1b7b3a6e83fa.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


# @app.route('/directory', methods = ['GET'])
# def retrieve():
# 	data = {'items': items}
# 	return jsonify(data)



@app.route('/test', methods = ['GET','POST'])
def render():
	return render_template('test.html')


@app.route('/new_user', methods = ['GET', 'POST'])
def add_new_user():
	"""adds a new user to Firebase"""
	new_user = request.args.get('name')
	address = request.args.get('address')
	email = request.args.get('email')
	password = request.args.get('password')
	
	data = {
		'name': new_user,
		'email': email,
		'password': password,
		'reviews': {},
		'rating': randint(1,5)
	}


	new_set = db.collection('users').document(new_user.lower())
	new_set.set(data)
	return 'Success!'


@app.route('/new_company', methods = ['GET', 'POST'])
def add_new_company():
	"""adds a new company to Firebase"""
	new_company = request.args.get('company')
	address = request.args.get('address')
	email = request.args.get('email')
	password = request.args.get('password')
	pay = request.args.get('pay')


	data = {
		'name' : new_company,
		'rating': randint(1,5),
		'positions': {},
		'email': email,
		'password': password,
		'reviews': {},
		'pay': pay,
		'keywords': None
	}
	new_set = db.collection('companies').document(new_company.lower())
	new_set.set(data)
	return 'Success!'


@app.route('/update_company', methods = ['GET', 'POST'])
def update_company():
	company = request.args.get('company').lower()
	pay = request.args.get('pay')
	positions = request.args.get('positions')
	keywords = request.args.get('keywords')

	data = {
		'pay': pay,
		'positions': positions,
		'keywords': keywords
	}

	new_set = db.collection('companies').document(company)
	new_set.set(data, merge = True)
	return "Success!"


@app.route('/retrieve_user', methods = ['GET', 'POST'])
def get_user():
	"""get method for retreiving user info"""
	user = request.args.get('user').lower()
	doc_ref = db.collection('users').document(user)
	doc = doc_ref.get()
	return jsonify({user: doc.to_dict()})


@app.route('/retrieve_company', methods = ['GET', 'POST'])
def get_company():
	"""get method for retreiving company info"""
	company = request.args.get('company').lower()
	doc_ref = db.collection('companies').document(company)
	doc = doc_ref.get()
	return jsonify({company: doc.to_dict()})


@app.route('/auth', methods = ['GET'])
def auth():
	"""login method for both users and companies through email and password"""
	email = request.args.get('email')
	password = request.args.get('password')
	docs1 = db.collection('companies').stream() 
	docs2 = db.collection('users').stream()

	for doc in docs1:
		if email and password in doc.to_dict().values():
			return 'company'
	for doc in docs2:
		if email and password in doc.to_dict().values():
			return 'user'
	return 'False'


@app.route('/search_employees', methods = ['GET'])
def employee_search():
	"""Generate json of employee profiles"""
	keywords = request.args.get('keyword')
	final_dict = {}
	docs = db.collection('users').stream()
	result = []
	if keywords:
		for doc in docs:
			if keywords in doc.to_dict().values:
				final_dict[doc.id] = doc.to_dict()
	if final_dict:
		result = [db.collection('users').document(u).get().to_dict() for u in final_dict]

	for doc in docs:
		user_dictionary = doc.to_dict()
		final_dict[doc.id] = user_dictionary

	return jsonify({'top_user_emails': result + [db.collection('users').document(u).get().to_dict() for u in final_dict if not keywords or keywords not in db.collection('users').document(u).get().to_dict().values()]})


@app.route('/search_employers', methods = ['GET'])
def employer_search():
	"""Generate json of employer profiles"""
	keywords = request.args.get('keyword')
	final_dict = {}
	docs = db.collection('companies').stream()
	result = []
	if keywords:
		for doc in docs:
			if keywords in doc.to_dict().values:
				final_dict[doc.id] = doc.to_dict()
	if final_dict:
		result = [db.collection('companies').document(u).get().to_dict() for u in final_dict]
	for doc in docs:
		user_dictionary = doc.to_dict()
		final_dict[doc.id] = user_dictionary

	return jsonify({'top_companies': result + [db.collection('companies').document(u).get().to_dict() for u in final_dict if not keywords or keywords not in db.collection('users').document(u).get().to_dict().values()]})



if __name__ == '__main__':
	app.run(debug = True)
