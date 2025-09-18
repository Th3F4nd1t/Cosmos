
import os
from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Generate random 32 char string
app.secret_key = os.urandom(32)

# Trust Cloudflare proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Make cookies valid through HTTPS proxy
app.config.update(
    SESSION_COOKIE_NAME="session",
    SESSION_COOKIE_DOMAIN=os.getenv("SESSION_COOKIE_DOMAIN"),
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    client_kwargs={"scope": "openid email profile"},
)

@app.route("/")
def index():
    user = session.get("user")
    if user:
        return f"Hello, {user['email']}!"
    return '<a href="/login">Login with Google</a>'

@app.route("/login")
def login():
    redirect_uri = url_for("auth_callback", _external=True, _scheme="https")
    return oauth.google.authorize_redirect(redirect_uri)

@app.route("/auth/callback")
def auth_callback():
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    session["user"] = userinfo
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
