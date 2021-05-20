import os
import json
import hashlib
import requests
from . import constants

def PILupload(imgBytes) -> dict:
    """Uploads an image to imgur.
    Returns a dict containing the response."""
    
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cached_responses.json"), "r+") as f:
        file_data = json.load(f)
        
        # Hash the image in order to reduce the size when it's saved
        # A common problem with hashing images with cryptographic functions
        # is that different computers and different resolutions will make different bytes
        # and as such, different hashes. However, it runs on only one server so it's fine
        img_hashed = hashlib.md5(imgBytes).hexdigest()
        
        cachedImg = file_data.get(img_hashed, None)
        if not cachedImg:
            payload = {"image": imgBytes}
            headers = {"Authorization": f"Client-ID {constants.IMGUR_API_CLIENT_ID}"}
            response = requests.request("POST", constants.IMGUR_API_URL, headers=headers, data=payload).json()
            
            file_data.update({img_hashed: response})
            f.seek(0)
            # convert back to json.
            json.dump(file_data, f, separators=(',', ':'))
        else:
            response = cachedImg
    
    return response

def retrieve_credits():
    """Returns how many credits the app has for Imgur.
    
    If the app grows enough, we might have issues with imgur ratelimits."""
    headers = {"Authorization": f"Client-ID {constants.IMGUR_API_CLIENT_ID}"}
    response = requests.request("GET", constants.IMGUR_API_CREDITS, headers=headers)
    
    return response.json()
