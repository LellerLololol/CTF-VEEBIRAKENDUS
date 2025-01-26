from flask import *
import json
import os
import jwt
import dotenv
from datetime import timedelta, datetime, timezone
import sqlite3


def main():
    # File path for JSON data
    JSON_PATH = './data.json'

    # Server dir
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Go one directory up
    PROJECT_DIR = os.path.dirname(BASE_DIR)

    # Build directory:
    BUILD_DIR = os.path.join(PROJECT_DIR, 'client', 'build')

    # index.html location:
    INDEX = os.path.join(BUILD_DIR, 'index.html')

    # Load secret and algorithm from env variables for JWT tokens
    dotenv.load_dotenv()
    SECRET = os.getenv('secret')
    ALGORITHM = os.getenv('algorithm')

    # Flask app variable
    app = Flask(__name__, static_folder=os.path.join(BUILD_DIR, 'static'))
    
    
    # Route to get all offers
    @app.route('/api/getAllOffers', methods=['GET'])
    def get_offers():
        offers = read_json_data()
        return jsonify(offers), 200

    @app.route('/<path:filename>')
    def serve_file(filename):
        # Serve files from the 'client/build' directory
        
        #*DEBUGGING
        app.logger.info(f"request filename: {filename}")

        # Construct the full path to the file
        file_path = os.path.join(BUILD_DIR, filename)
        # Check if the file exists
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path)
        return "404 NOT FOUND"
    
    @app.route('/')
    def serve_index():
        return send_file(INDEX)
    
    @app.route('/Profile')
    def Profile():
        return serve_index()

    @app.route('api/Profile')
    def api_profile():
        token = request.headers.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            token = token.split(" ")[1]
            
            # Decode the token and get the user data
            user_id = decode_jwt(token)
            
            if user_id:
                # If token is valid, serve the profile (return user data)
                user_data = fetch_user_data(user_id)
                return jsonify({
                    'username': user_data.get('username'),
                    'id': user_data.get('id')
                })
            else:
                return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            app.logger.error(f"Error decoding token: {e}")
            return jsonify({"error": "An error occurred"}), 
    
    @app.route('/api/logIn', methods=['POST'])
    def api_login():
        response = request.get_json()
        username = response.get("username")
        password = response.get("password")
        if validate_login(username, password):
            user_id = execute_db_command(f"SELECT id FROM users WHERE username='{username}';")[0]
            jwt_token = create_jwt(user_id)
            app.logger.info(jwt_token)
            return jsonify({"token": jwt_token}), 200
        else:
            return jsonify({"error": "access denied"}), 401


    # Helper function to read the JSON file
    def read_json_data():
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as file:
                return json.load(file)
        else:
            return []

    # Helper functiom to gather a user's data
    def fetch_user_data(user_id):
        app.logger.info(f"sql output: {execute_db_command(f"SELECT * FROM users WHERE id='{user_id}';")}")
        return {"id": 1, "username": "test"}


    # Helper function to validate website logins
    def validate_login(username, password):
        database_output = execute_db_command(f"SELECT password FROM users WHERE username='{username}';")
        if database_output is not None and password == database_output[0]:
            return True
        return False

    # Helper function to create a JWT token for logging in
    def create_jwt(user_id=None):
        if user_id is None:
            raise ValueError("User ID must be provided.")
        payload = {
        'user_id': user_id,
        'admin': False,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=1_728_000) # expirity time is 20 days
        }
        token = jwt.encode(payload, SECRET, ALGORITHM)
        return token

    # Helper function to decode JWT tokens for authentication
    def decode_jwt(token=None):
        if token is None:
            raise ValueError("Token must be provided.")
        try:
            decoded_token = jwt.decode(token, SECRET, ALGORITHM)
            user_id = decoded_token['user_id']
            if user_id:
                return user_id
            raise ValueError("User ID not found in token.")
        except:
            raise ValueError("JWT token invalid")
    
    # Helper function to execute commands to the database
    def execute_db_command(command: str):
        # Try block to connect to database IN READ-ONLY MODE and execute a command
        # The read-only mode is really important since this means that the sql injection vuln can ONLY read from the database and not instantly nuke it
        try:
            with sqlite3.connect('file:database.db?mode=ro', uri=True) as db_connection:
                cursor = db_connection.cursor()
                cursor.execute(command)
                result = cursor.fetchone()
                return result
        except sqlite3.DatabaseError as e:
            print(f"An error occurred: {e}")
        finally:
            # Connection is closed automatically when exiting the 'with' block
            print("Connection closed properly.")


    # Run the app
    app.run(debug=True, port=80)


if __name__ == '__main__':
    main()