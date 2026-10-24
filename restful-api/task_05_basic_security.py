
#!/usr/bin/python3
"""API security with Basic Authentication and JWT."""

import os

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "development-only-secret-key-change-me"
)

auth = HTTPBasicAuth()
jwt = JWTManager(app)

users = {
    "user1": {
        "username": "user1",
        "password": generate_password_hash("password"),
        "role": "user"
    },
    "admin1": {
        "username": "admin1",
        "password": generate_password_hash("password"),
        "role": "admin"
    }
}


@auth.verify_password
def verify_password(username, password):
    """Verify credentials for Basic Authentication."""
    user = users.get(username)

    if user and check_password_hash(user["password"], password):
        return username

    return None


@app.route("/basic-protected", methods=["GET"])
@auth.login_required
def basic_protected():
    """Route protected by HTTP Basic Authentication."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return an access token."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid credentials"}), 401

    username = data.get("username")
    password = data.get("password")

    user = users.get(username) if isinstance(username, str) else None

    if (
        not user
        or not isinstance(password, str)
        or not check_password_hash(user["password"], password)
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({"access_token": access_token}), 200


@app.route("/jwt-protected", methods=["GET"])
@jwt_required()
def jwt_protected():
    """Route protected by a valid JWT."""
    return "JWT Auth: Access Granted"


@app.route("/admin-only", methods=["GET"])
@jwt_required()
def admin_only():
    """Allow access only to authenticated administrators."""
    username = get_jwt_identity()
    user = users.get(username)

    if not user or user["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403

    return "Admin Access: Granted"


@jwt.unauthorized_loader
def missing_token(error):
    """Handle requests with missing JWT credentials."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def invalid_token(error):
    """Handle malformed or invalid JWT tokens."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    """Handle expired JWT tokens."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    """Handle revoked JWT tokens."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token(jwt_header, jwt_payload):
    """Handle tokens that are not fresh."""
    return jsonify({"error": "Fresh token required"}), 401


@jwt.token_verification_failed_loader
def token_verification_failed(jwt_header, jwt_payload):
    """Handle tokens that fail additional verification."""
    return jsonify({"error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run()
