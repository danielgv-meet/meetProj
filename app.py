from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase
# <<<<<<< Updated upstream
# =======
# # import firebase
# >>>>>>> Stashed changes

firebaseConfig = {
  "apiKey": "AIzaSyB057zr6FS31fUqXSuvPuGwTgf4CU3_MNM",
  "authDomain": "auth-lab-1349a.firebaseapp.com",
  "projectId": "auth-lab-1349a",
  "storageBucket": "auth-lab-1349a.appspot.com",
  "messagingSenderId": "916347876212",
  "appId": "1:916347876212:web:aa74c8b48d817af88fb221",
  "databaseURL": "https://project2-b06a5-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = 'super-secret-key'

@app.route("/")
def main_page():
	return render_template('main.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']	
		password = request.form['password']
		name = request.form['name']
		Y_O = request.form['school']
		user = {"name": name, "email": email, "school": Y_O}
		print(user)
		try:
			if Y_O == "Y" :
				login_session['user'] = auth.create_user_with_email_and_password(email, password)
				UID = login_session["user"]["localId"]
				db.child("Users").child(UID).set(user)
				
				return redirect(url_for("home"))
			else:
				login_session['user'] = auth.create_user_with_email_and_password(email, password)
				UID = login_session["user"]["localId"]
				db.child("user_o").child(UID).set(user)

			
		
			return redirect(url_for("home"))
		except Exception as e:
			print(e)
			return "error"
	else:
		return render_template('signup.html')

@app.route("/signin", methods=['GET', 'POST'])
def signin():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for("home"))
		except:
			print("The user does not exist")
			return render_template("error.html", error = "the user does not exist")
	else:
		return render_template('signin.html')

@app.route("/profiles", methods=["GET", "POST"])
def profiles():
	if request.method == "POST":
		users_id = request.form['id']
		return render_template('profile.html', id = users_id, users = db.child('Users').get().val())
	else:
		return render_template('profiles.html', users = db.child('Users').get().val())


@app.route("/home", methods=["GET", "POST"])
def home():
	if request.method == "POST":
		return render_template('home.html')
	else:
		return render_template('home.html')

@app.route("/your_profile")
def your_porfile():
	UID = login_session['user']['localId']
	if UID in db.child('Users').get().val():
		return render_template('profile.html', id=UID, users=db.child('Users').get().val())
	else:
		return render_template('profile.html', id=UID, users=db.child('user_o').get().val())

@app.route("/signout")
def signout():
	login_session["user"].clear()
	return redirect('/')


@app.route('/edit_profile', methods=['GET', 'GET'])
def edit_profile():
  if request.method == "POST":
    school_name = request.form['school']
    hobbies = request.form['hobbies']
    name = request.form['name']
    UID = login_session['user']['localId']
    if UID in db.child('Users'):
      if school_name == "Younited":
        db.child('Users').child(UID).update({'name': name, 'school_name': school_name, "hobbies": hobbies})
      else:
        user = db.child('Users').child(UID).get().val()
        db.child('Users').child(UID).delete()
        db.child('user_o').child(UID).set(user)
#First Pull

if __name__ == "__main__":
 	app.run(debug=True)
    