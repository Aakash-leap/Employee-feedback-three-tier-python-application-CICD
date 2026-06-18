from flask import Flask, render_template,request
import mysql.connector 
import os 

app = Flask(__name__)

db_config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        feedback = request.form["feedback"] 
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO feedback(name,feedback) VALUES (%s,%s)",
            (name, feedback)
        )
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "healthy"} , 200    

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    
    
    