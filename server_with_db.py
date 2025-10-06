# server_with_db.py
from flask import Flask, request, jsonify
from orm_models import DB, Student
from sqlalchemy import text

class AppServer:
    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port
        self.db = DB()  # uses students.db by default
        self.app = Flask(__name__)
        self.register_routes()

    def register_routes(self):
        app = self.app

        @app.route("/")
        def index():
            return jsonify({"message": "SoDA DB Workshop demo", "endpoints": ["/students (GET, POST)"]})

        @app.route("/students", methods=["POST"])
        def create_student():
            # JSON body: { "name": "...", "major": "...", "gpa": 3.7 }
            payload = request.get_json(force=True)
            name = payload.get("name")
            if not name:
                return jsonify({"error": "missing name"}), 400
            student = {"name": name, "major": payload.get("major"), "gpa": float(payload.get("gpa", 0.0))}
            self.db.add_students([student])
            return jsonify({"status": "created"}), 201

        @app.route("/students", methods=["GET"])
        def list_students():
            gpa_min = request.args.get("gpa_min", default=0.0, type=float)
            students = self.db.get_students_with_min_gpa(gpa_min)
            out = [{"id": s.id, "name": s.name, "major": s.major, "gpa": s.gpa} for s in students]
            return jsonify(out)

        @app.route("/raw-query", methods=["GET"])
        def raw_query_example():
            """
            Demonstrate how to run a parameterized raw SQL using SQLAlchemy text
            (good) vs an unsafe concatenation approach (bad).
            Use ?unsafe=1 to see unsafe version (for demonstration only).
            """
            unsafe = request.args.get("unsafe", default=0, type=int)
            gpa_min = request.args.get("gpa_min", default=0.0, type=float)
            engine = self.db.engine
            if unsafe:
                # DANGEROUS: do NOT use in production
                raw_sql = f"SELECT id, name, major, gpa FROM Students WHERE gpa >= {gpa_min};"
                rows = engine.execute(text(raw_sql)).fetchall()
            else:
                stmt = text("SELECT id, name, major, gpa FROM Students WHERE gpa >= :gpa_min;")
                rows = engine.execute(stmt, {"gpa_min": gpa_min}).fetchall()
            return jsonify([dict(row) for row in rows])

    def run(self):
        # Use threaded=True so concurrent requests can be served in dev server
        self.app.run(host=self.host, port=self.port, threaded=True)

if __name__ == "__main__":
    server = AppServer()
    server.run()
