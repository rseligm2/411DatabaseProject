from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/teams/<teams>')
def teams_page(teams):
    pass





if __name__ == '__main__':
    app.run()

