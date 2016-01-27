from flask import Flask, request, render_template, jsonify
from main import main

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_form():
	return render_template('form.html')

@app.route('/results', methods=['POST'])
def results():
	req = dict(request.form)
	for elem in req:
		if req[elem][0] == '':
			req[elem] = None
		else:
			req[elem] = req[elem][0]

	if req['domains']:
		req['domains'] = req['domains'].split(',')
	else:
		req['domains'] = []

	results = {'results': main(first_name=req['firstname'], last_name=req['lastname'],
		middle_name=req['middlename'], linkedin_url=req['linkedin'], twitter_url=req['twitter'],
		angellist_url=req['angellist'], github_url=req['github'], domains=req['domains'])}
	return jsonify(results)

if __name__ == '__main__':
	app.run(debug=True)