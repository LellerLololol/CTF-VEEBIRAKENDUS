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
        reviews = fetch_offer_reviews()
        for offer in offers:
            offer["reviews"] = reviews.get(offer["id"], [])
        return jsonify(offers), 200

    @app.route('/<path:filename>')
    def serve_file(filename):
        """Serves files from the 'client/build' directory"""
        
        #*DEBUGGING
        app.logger.info(f"request filename: {filename}")

        file_path = os.path.join(BUILD_DIR, filename)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path)
        return "404 NOT FOUND"
    
    @app.route('/')
    @app.route('/Profile')
    def serve_index():
        return send_file(INDEX)

    @app.route('/api/buy', methods=['POST'])
    def buy():
        data = request.get_json()
        app.logger.info(f"Buy offer: {data}")
        offerID = data['id']
        return 'well done', 200

    @app.route('/api/Profile')
    def profile():
        #* This function contains the idor vuln
        token = request.cookies.get('token')
        user_id = request.cookies.get('user_id')
        print(token)
        if token:            
            # Validate the token
            if decode_jwt(token, "exp") == "JWT token invalid":
                return jsonify({
                    'error': "JWT token invalid"
                })
            if user_id:
                # If token is valid, serve the profile (return user data)
                user_data = fetch_user_data(user_id) #! THIS WILL BE THE REASON FOR IDOR
                if not user_data:
                    return jsonify({"error": "User not found"})
                """
                return jsonify({
                    'username': user_data.get('username'),
                    'id': user_data.get('id')

                }) 
                """
                return jsonify(user_data)           
        return "No token found", 403
    
    @app.route('/api/logIn', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        login_result = validate_login(username, password)
        match login_result:
            case "Authenticated":
                user_id = execute_fetch_db_command(f"SELECT id FROM users WHERE username='{username}';")[0][0]
                jwt_token = create_jwt(user_id)
                app.logger.info(jwt_token)
                response = make_response("Cookies set!")
                response.set_cookie('token', jwt_token, path='/')
                response.set_cookie('user_id', str(user_id), path='/')
                return response
            case _:
                return jsonify({"error": login_result}), 401
    
    @app.route('/api/addReview', methods=['POST'])
    def add_review():
        data = request.get_json()
        offer_id = data.get("offer_id")
        review_text = data.get("review")
        if not offer_id or not review_text:
            return jsonify({"error": "Invalid input"}), 400
        sql_return_value = execute_commit_db_command(f"INSERT INTO reviews (offer_id, review_text) VALUES ({offer_id}, '{review_text}')")
        if sql_return_value is not None and sql_return_value is False:
            return jsonify({"error": "An error has occurred"}), 500
        return jsonify({"message": "Review added successfully"}), 201
    
    @app.route('/api/createOffer', methods=['POST'])
    def create_offer():
        pass
            
    
    @app.route('/api/Register', methods=['POST'])
    def register_user():
        data = request.get_json()
        new_username = data.get("username")
        new_password = data.get("password")
        if not new_username or not new_password:
            return jsonify({"error": "Invalid input"}), 400
        username_exists = lambda username: bool(execute_fetch_db_command(f"SELECT 1 FROM users WHERE username = '{username}' LIMIT 1;"))
        if username_exists(new_username):
            return jsonify({"error": "Username already exists"}), 400
        sql_return_value = execute_commit_db_command(f"INSERT INTO users (username, password) VALUES ('{new_username}', '{new_password}')")
        if sql_return_value is not None and sql_return_value is False:
            return jsonify({"error": "An error has occurred"}), 500
        return jsonify({"message": "User registered successfully"}), 200


    # Helper function to read the JSON file
    def read_json_data():
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'r') as file:
                return json.load(file)
        else:
            return []

    # Helper functiom to gather a user's data
    def fetch_user_data(user_id):
        user_data = execute_fetch_db_command(f"SELECT id, username, money FROM users WHERE id='{user_id}';")[0]
        if not bool(user_data):
            return False
        return {
            "id": user_data[0],
            "username": user_data[1],
            "money": user_data[2]
            }
        #*Debugging
        #*app.logger.info("IMPORTANT  !!!!!!     " + str(user))
        #*return {"id": 1, "username": "test"}

    # Function to fetch reviews from the database
    def fetch_offer_reviews():
        reviews = {}
        rows = execute_fetch_db_command("SELECT offer_id, review_text FROM reviews;")
        for row in rows:
            offer_id, review = row
            if offer_id not in reviews:
                reviews[offer_id] = []
            reviews[offer_id].append(review)
        return reviews

    # Helper function to validate website logins
    def validate_login(username, password):
        """
        First sql is needed to confirm if a user exists, second one is used for confirming the password.

        Yes, authentication works without the first sql query, but it is needed for the enumeration vuln to work.
        """
        if not execute_fetch_db_command(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1;"):
            app.logger.info(f"USERNAME DATABASE_OUTPUT VALUE: {execute_fetch_db_command(f"SELECT * FROM users WHERE username = '{username}' LIMIT 1;")}") #* Debugging
            return "Username does not exist"
        database_output = execute_fetch_db_command(f"SELECT password FROM users WHERE username='{username}';")
        if database_output is not None and password == database_output[0][0]:
            return "Authenticated"
        return "Wrong password"
    
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

    # Helper function to decode JWT tokens when authenticating
    def decode_jwt(token=None, dict_key=None):
        if token is None or dict_key == None or not isinstance(dict_key, str):
            raise ValueError("Token and requested namefield must both be provided.")
        try:
            decoded_token = jwt.decode(token, SECRET, ALGORITHM)
            extracted_value = decoded_token[dict_key]
            if extracted_value:
                return extracted_value
            raise ValueError
        except ValueError:
            raise ValueError("Namefield not found in token.")
        except:
            raise ValueError("JWT token invalid")
    
    # Helper function to execute commands to the database
    def execute_fetch_db_command(command: str):
        # Try block to connect to database IN READ-ONLY MODE and execute a command
        # The read-only mode is really important since this means that the sql injection vuln can ONLY read from the database and not instantly nuke it
        try:
            with sqlite3.connect('file:database.db?mode=ro', uri=True) as db_connection:
                cursor = db_connection.cursor()
                cursor.execute(command)
                result = cursor.fetchall() #* this used fetchone() before
                return result
        except sqlite3.DatabaseError as e:
            app.logger.error(f"wtf error: {e}")
        finally:
            print("Connection closed properly.")
    
    def execute_commit_db_command(command: str):
        try:
            with sqlite3.connect('database.db') as db_connection:
                cursor = db_connection.cursor()
                cursor.execute(command)
                db_connection.commit()
        except Exception as e:
            app.logger.error(f"wtf error: {e}")
            return False
        print("Connection closed properly.")


    # Run the app
    app.run(debug=True, port=80)


if __name__ == '__main__':
    main()