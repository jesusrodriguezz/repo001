from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy 

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line

@app.route('/home')
@app.route('/')
def index():
  return render_template('home.html', title = 'Home')

@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit(): # checks if entries are valid
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home')) # if so - send to home page
  return render_template('register.html', title='Register', form=form)  

@app.route("/update_server", methods=['POST'])
def webhook():
  if request.method == 'POST':
    repo = git.Repo('/home/CHANGE_TO_PYTHON_ANYWHERE_USERNAME/CHANGE_TO_GITHUB_REPO_NAME')
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully', 200
  else:
    return 'Wrong event type', 400

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '678a911b1a871d625d4d398e853dacf2'
    app.run(debug=True, host="0.0.0.0")
