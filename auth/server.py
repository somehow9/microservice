import jwt,datetime,os
from flask import Flask,request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
# server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
# server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
# server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
# server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
# server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


# server.config["MYSQL_HOST"] = "172.17.0.4"
server.config["MYSQL_HOST"] = "192.168.1.157"
server.config["MYSQL_USER"] = "root"
# server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = "auth"
# server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=["POST"])

def login():
    auth = request.authorization
    if not auth:
        return "missing credentials",401

# check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
            "select email,password from user where email=%s",(auth.username,)
            )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        if auth.username != email or auth.password != password:
            return "invalid credentials",401 
        else:
            # return createJWT(auth.username,os.getenv("JWT_SECRET"),True)
            return createJWT(auth.username,"sarcasm",True)
    else:
        return "invalid credentials",401

def createJWT(username,secret,authz):
    return jwt.encode(
            {
                "username":username,
                # "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(days=1),
                "iat": datetime.datetime.utcnow(),
                "admin": authz,
        },
        secret,
        algorithm="HS256",
         )

@server.route("/validate",methods=["POST"])
def validate():
    encode_jwt = request.headers["Authorization"]
    if not encode_jwt:
        return "missing credentials",401
    encode_jwt = encode_jwt.split(" ")[1]
    try:
        # print(os.environ.get("JWT_SERCRET"))
        decoded = jwt.decode( encode_jwt,"sarcasm",algorithms=["HS256"])

    except:
        return "not authorized",403

    return decoded,200


if __name__ == "__main__":
    server.run(host="0.0.0.0",port=5000)
    
