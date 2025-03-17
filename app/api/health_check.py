from . import api_home


@api_home.route("/",methods=["GET"])
def check_health():
    return "ok"
