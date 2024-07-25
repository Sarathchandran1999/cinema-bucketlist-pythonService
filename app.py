from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)
databaseURL = 'postgres://avnadmin:AVNS_CppSWOLfQIAH-kVcpEs@pg-203e163f-itssarathchandran-17f5.i.aivencloud.com:12081/cinema?sslmode=require'
connection = psycopg2.connect(databaseURL)
CREATE_CINEMA_TABLE = """
CREATE TABLE IF NOT EXISTS cinema_bucketlist (
    id SERIAL PRIMARY KEY,
    cinema TEXT
)
"""
INSERT_INTO_CINEMA_TABLE = "INSERT INTO cinema_bucketlist (cinema) values (%s) RETURNING id"
GET_CINEMA = "SELECT * FROM cinema_bucketlist"


@app.post("/addToDatabase")
def add_cinema():
    data = request.get_json()
    print("data----->", data)
    cinema = data["cinema"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_CINEMA_TABLE)
            print("----------------------")
            cursor.execute(INSERT_INTO_CINEMA_TABLE, (cinema,))
            print("+++++++++++++++++++++++++++++++=")
            id = cursor.fetchone()[0]
    return jsonify({"id": id, "message": f"Cinema {cinema} created"}), 201


@app.get("/getCinema")
def get_cinema():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_CINEMA)
            print("==success==")
            cinemas = cursor.fetchall()
    return jsonify(cinemas), 200
