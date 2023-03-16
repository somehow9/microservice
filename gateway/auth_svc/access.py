import os,requests

def login(request):
    auth = request.authorization
    if not auth:
        return None,("missing credentials",401)

    basicAuth = (auth.username,auth.password)

     
    AUTH_SVC_ADDRESS = "192.168.1.157:5000"
    response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/login",
            # f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
            auth = basicAuth
            )

    if response.status_code == 200:
        return response.text,None
    else:
        return None,(response.text,response.status_code)

