from aplus.app import create_app

# Create the app using the configuration
app = create_app('config.py')
if __name__ == "__main__":
	app.run(host='0.0.0.0')
