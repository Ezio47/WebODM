from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return '<h1> OpenDroneMap Web Interface <h1>'

# server startup

if __name__ == '__main__':
	app.run(debug=True)

