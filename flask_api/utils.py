from flask import jsonify, make_response

def generate_response(data: dict = None, status_code: int = 200):
    """
    Generate a response with CORS headers and logging.

    Parameters:
    data (dict, optional): The data to be JSONified and returned in the response. Defaults to None.
    status_code (int, optional): The HTTP status code for the response. Defaults to 200.

    Returns:
    Response: A Flask Response object with CORS headers.
    """
    if data is None:
        data = {}
    
    response = make_response(jsonify(data), status_code)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")    
    return response
