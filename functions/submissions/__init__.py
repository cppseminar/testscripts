"""This is implementation of submissions. 

We support:
- GET on all submissons (you can specify offset as parameter)
- GET on specific objectID
- POST to post new data
"""
import contextlib
import datetime
import itertools
import json
import logging
import os
import urllib

import azure.functions as func

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, RELAXED_JSON_OPTIONS

from .. import shared 



def dict_response(response: [dict,list], code=200):
    return func.HttpResponse(
        json.dumps(response), status_code=code, mimetype="application/json"
    )

def error_response(response: str, code=400):
    return func.HttpResponse(
        json.dumps({"error": response, "code": code }),
         status_code=code, mimetype="application/json"
    )



def main(req: func.HttpRequest) -> func.HttpResponse:
    request_id = req.route_params.get("id", None)
    if request_id and not ObjectId.is_valid(request_id):
        return error_response("Invalid request id")

    client = MongoClient(os.environ["MyCosmosDBConnectionString"], retryWrites=False)
    db = client.get_database("development")
    collection = db.get_collection("submissions")
    

    if req.method == "POST" and not request_id:
        # Someone is adding new value
        submit = None
        try:
            request_json = req.get_json()
            request_json = dict(request_json)
            if "_id" in request_json:
                raise RuntimeError("Trying to set _id")
            # For now, this is fine
            submit = request_json
        except Exception as e:
            return dict_response({"error": "Bad json"}, code=400)
        
        result = collection.insert_one(submit)
        new_id = str(result.inserted_id)

        parsed = urllib.parse.urlparse(req.url)
        editable = list(parsed)
        
        # Fix slash on the end of uri
        uri = editable[2]
        slash = ""
        if uri and uri[-1] != "/":
            slash = "/"
        editable[2] = str(uri) + f"/{new_id}"
        # Done

        url = urllib.parse.urlunparse(editable)

        return dict_response({"link": url})

    if req.method != "GET":
        return dict_response({"error": "Unsupported protocol"}, 
                            code=501)
    if request_id:

        logging.warn({"_id": ObjectId(request_id)})
        result = collection.find_one({"_id": ObjectId(request_id)})
        if not result:
            return error_response("Not found", code=403)
        logging.info(type(result))
        return dict_response(json.loads(dumps(result, json_options=RELAXED_JSON_OPTIONS)))

    # This is get method and no request id was set, therefore we want to 
    # list something

    offset = 0
    with contextlib.suppress(TypeError):
        offset = int(req.params.get("offset", 1))
        logging.warn("offset is %s", offset)

    result = list(collection.find().limit(5).skip(offset))
    return dict_response(json.loads(dumps(result, json_options=RELAXED_JSON_OPTIONS)))



