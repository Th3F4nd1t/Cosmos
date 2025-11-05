import os
from flask import Flask, request, session, redirect, url_for
from extensions import oauth
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_session import Session
import redis
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Fixed secret key (DO NOT use os.urandom in production)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    # Trust Cloudflare proxy headers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Session config for production (server-side with Redis)
    app.config.update(
        SESSION_TYPE="redis",
        SESSION_REDIS=redis.from_url(os.getenv("REDIS_URL")),  # e.g., redis://localhost:6379/0
        SESSION_COOKIE_NAME="session",
        SESSION_COOKIE_DOMAIN=os.getenv("SESSION_COOKIE_DOMAIN"),  # include subdomain or use .example.com
        SESSION_COOKIE_SAMESITE="lax",  # required for cross-site OAuth
        SESSION_COOKIE_SECURE=True,       # required for HTTPS
        SESSION_PERMANENT=False,
    )

    # Initialize server-side session
    Session(app)

    # Initialize shared OAuth instance
    oauth.init_app(app)

    # Register Google OAuth provider
    oauth.register(
        "google",
        client_id=os.getenv("OAUTH_CLIENT_ID"),
        client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # Main route
    @app.route("/")
    def index():
        user = session.get("user")
        if user:
            return f"Hello, {user['email']}!<br> <a href='/logout'>Logout</a>"
        return '<a href="/login">Login with Google</a>'
    
    # Login route
    @app.route("/login")
    def login():
        redirect_uri = url_for("auth_callback", _external=True, _scheme="https")
        return oauth.google.authorize_redirect(redirect_uri)

    # Logout route
    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect("/")

    # OAuth callback
    @app.route("/auth/callback")
    def auth_callback():
        print("Session before callback:", dict(session))
        print("Request args:", request.args)
        token = oauth.google.authorize_access_token()
        userinfo = oauth.google.get(
            "https://www.googleapis.com/oauth2/v1/userinfo"
        ).json()
        session["user"] = userinfo
        return redirect("/")

    return app

if __name__ == "__main__":
    app = create_app()
    # Use 0.0.0.0 in production if behind reverse proxy
    app.run(host="0.0.0.0", port=8080, debug=False)
