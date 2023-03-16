import os,requests

def token(request):
    if "Authorization" not in request.headers:
        return None,("missing credientials",401)
    
    token = request.headers["Authorization"]

    if not token:
        return None,("miss credientials",401)

    AUTH_SVC_ADDRESS = "192.168.1.157:5000"
    response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/validate",
            # f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
            headers = {"Authorization":token},
            )

    if response.status_code == 200:
        return response.text,None
    else:
        return None,(response.text,response.status_code)
