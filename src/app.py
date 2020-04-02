from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/teams/<teams>')
def teams_page(teams):
    pass


@app.route('/login', endpoint='login')
def login():
    return render_template('login.html')


@app.route('/signup', endpoint="signup")
def signup():
    return render_template('signup.html')


@app.route('/contact', endpoint="contact")
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)

