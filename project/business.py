from flask import Blueprint, jsonify, Response, abort, request
from functools import wraps
import requests

bp_business = Blueprint("business", __name__)

# e fix ala pus in docker-compose
USER_API_URL = "http://user:5000/users/checkUser"
IO_API_URL = "http://io_api:4000/WanderRooms"
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        myobj = {"dummy": "dummy_v"}
        check_response = requests.post(url=USER_API_URL, 
                                    headers={"Authorization": token}, 
                                    json=myobj)
        
        if check_response.status_code != 200:
            return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401 
        j = check_response.json()
        user_id = j['user_id']
        return f(user_id ,*args, **kwargs)

    return decorated


@bp_business.route("/")
def home():
    return "Hello, Business!"

@bp_business.route("/WanderRooms/showRoomsInfo", methods=['POST'])
@token_required
def getRooms(user_id):
    payload = request.get_json(silent=True)
    if (not payload):
        payload = {}
    payload["user_id"] = user_id
    
    response = requests.post(url=IO_API_URL + "/getRooms", 
                                    json=payload)
    
    return jsonify(response.json())



@bp_business.route("/WanderRooms/reserveRoom", methods=['POST'])
@token_required
def reserveRoom(user_id):
    payload = request.get_json(silent=True)

    if (not payload):
        return {
            "message": "No given info for the reservation ",
            "data": None,
            "error": "Bad request"
        }, 400

    payload["user_id"] = user_id
    
    if not ('start_date' in payload and 'end_date' in payload):
        return {
            "message": "Please provide start_date and end_date ",
            "error": "Bad request"
        }, 400

    if not ('room_id' in payload):
        return {
            "message": "Please provide room_id ",
            "error": "Bad request"
        }, 400

    response = requests.post(url=IO_API_URL + "/reserveRoom", 
                                    json=payload)
    
    return jsonify(response.json())


@bp_business.route("/WanderRooms/cancelReservation", methods=['POST'])
@token_required
def cancelReservation(user_id):
    payload = request.get_json(silent=True)

    if (not payload):
        return {
            "message": "No given info for the reservation ",
            "data": None,
            "error": "Bad request"
        }, 400

    payload["user_id"] = user_id

    if not ('reservation_id' in payload):
        return {
            "message": "Please provide reservation_id ",
            "error": "Bad request"
        }, 400

    response = requests.post(url=IO_API_URL + "/cancelRoom", 
                                    json=payload)
    
    return jsonify(response.json())


@bp_business.route("/WanderRooms/updateReservation", methods=['PUT'])
@token_required
def updateReservation(user_id):
    payload = request.get_json(silent=True)

    if (not payload):
        return {
            "message": "No given info for the reservation ",
            "data": None,
            "error": "Bad request"
        }, 400

    payload["user_id"] = user_id

    if not ('reservation_id' in payload):
        return {
            "message": "Please provide reservation_id ",
            "error": "Bad request"
        }, 400

    response = requests.put(url=IO_API_URL + "/updateReservation", 
                                    json=payload)
    
    return jsonify(response.json())


@bp_business.route("/WanderRooms/historyCheck", methods=['POST'])
@token_required
def history_check(user_id):
    payload = request.get_json(silent=True)

    payload["user_id"] = user_id

    if not ('reservation_id' in payload):
        return {
            "message": "Please provide reservation_id ",
            "error": "Bad request"
        }, 400

    response = requests.post(url=IO_API_URL + "/getHistory", 
                                json=payload)
 
    return jsonify(response.json())