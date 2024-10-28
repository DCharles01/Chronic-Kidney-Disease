import argparse
from api.create_app import create_app

# Set up argument parser
parser = argparse.ArgumentParser(description="Run the Flask application.")
parser.add_argument('--env', choices=['prod', 'test', 'dev'], default='prod', help="Environment to run the app in: prod, test, or dev")
args = parser.parse_args()

# Create the app with the specified environment
app = create_app(args.env)

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=(args.env != 'prod'))
