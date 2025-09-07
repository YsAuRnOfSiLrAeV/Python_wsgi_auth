from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from storage import save_to_json, load_from_json
import json

FILENAME = "userInfo.json"

def handling_requests(environ, start_response):
    method = environ["REQUEST_METHOD"]
    path = environ.get("PATH_INFO", "/")

    if method == "OPTIONS":
        headers = [
            ("Access-Control-Allow-Origin", "*"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
            ("Access-Control-Allow-Headers", "Content-Type"),
        ]
        start_response("200 OK", headers)
        return [b""]

    if method == "POST" and path == "/register":
        try:
            length = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            length = 0

        body = environ["wsgi.input"].read(length).decode("utf-8")
        data = json.loads(body)

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        age = data.get("age")

        if not all([name, email, password, age]):
            response = {"error": "Missing fields"}
            resp_bytes = json.dumps(response).encode("utf-8")
            headers = [
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("400 Bad Request", headers)
            return [resp_bytes]

        users = load_from_json(FILENAME)

        if any(u["email"] == email for u in users):
            response = {"error": "User already exists"}
            resp_bytes = json.dumps(response).encode("utf-8")
            headers = [
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("400 Bad Request", headers)
            return [resp_bytes]

        users.append({"name": name, "email": email, "password": password, "age": age})
        save_to_json(FILENAME, users)

        response = {"status": "ok", "message": "User registered"}
        resp_bytes = json.dumps(response).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", "*"),
        ]
        start_response("200 OK", headers)
        return [resp_bytes]

    elif method == "POST" and path == "/login":
        try:
            length = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            length = 0

        body = environ["wsgi.input"].read(length).decode("utf-8")
        data = parse_qs(body)

        email = data.get("email", [""])[0]
        password = data.get("password", [""])[0]

        users = load_from_json(FILENAME)
        user = next((u for u in users if u["email"] == email and u["password"] == password), None)

        if user:
            response = {"status": "ok", "user": {"name": user["name"], "email": user["email"], "age": user["age"]}}
            resp_bytes = json.dumps(response).encode("utf-8")
            headers = [
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("200 OK", headers)
            return [resp_bytes]
        else:
            response = {"error": "Invalid email or password"}
            resp_bytes = json.dumps(response).encode("utf-8")
            headers = [
                ("Content-Type", "application/json"),
                ("Access-Control-Allow-Origin", "*"),
            ]
            start_response("401 Unauthorized", headers)
            return [resp_bytes]

    else:
        response = {"error": "Not Found"}
        resp_bytes = json.dumps(response).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", "*"),
        ]
        start_response("404 Not Found", headers)
        return [resp_bytes]


with make_server("", 8000, handling_requests) as server:
    print("Serving on http://127.0.0.1:8000 ...")
    server.serve_forever()
