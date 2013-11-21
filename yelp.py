import os
import oauth2
import urllib
import urllib2
import json

from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# Set this to True for more detailed internal server messages, but remember
# to return to False for production!
app.debug = True

# Retrieve API secrets from .env file. Please see README for configuration.
keys = {"YELP_KEY"          : os.environ['YELP_KEY'],
        "YELP_SECRET"       : os.environ['YELP_SECRET'],
        "YELP_TOKEN"        : os.environ['YELP_TOKEN'],
        "YELP_TOKEN_SECRET" : os.environ['YELP_TOKEN_SECRET']}

@app.route('/')
def run():
    return render_template("omelettes.html", res=[], location="", code=-1)

@app.route('/omelettes', methods=["POST"])
def yelp_search():
    # Search term - location
    location = request.form['location']

    # Get Yelp Response
    response = basic_yelp_request(location)
    code, content = process_response(response)

    # Render template with request result
    return render_template("omelettes.html", res=content, location=location, code=code)

def yelp_business_basics(business_entry):
    """ http://www.yelp.com/developers/documentation/v2/search_api
        See Businesses structure """
    return {"name"          : business_entry.get("name"),
            "image_url"     : business_entry.get("image_url", ""),
            "url"           : business_entry.get("url", "None listed"),
            "phone"         : business_entry.get("display_phone", "None Listed"),
            "rating"        : business_entry.get("rating", "n/a"),
            "review_count"  : business_entry["review_count"],
            "address"       : " ".join(business_entry["location"]["display_address"])}

def process_response(response):
    # Check for errors
    if "error" in response:
        return 1, response["error"]["id"] + ": " + response["error"]["text"]

    # Otherwise, just return a list of names of businesses
    # This version of the demo leaves the map alone, though a future version
    # will add the Google Mapping API.
    elif "businesses" in response:
        return 0, [yelp_business_basics(b) for b in response["businesses"]]

    # If something really unexpected happens, well, that will be really sad.
    else:
        return 1, "Something went wrong, please try again."


def basic_yelp_request(location,keyword="omelette"):
    """ Adapted from Yelp API Search Example
        https://github.com/Yelp/yelp-api/blob/master/v2/python/search.py """

    # Prepare URL
    url_params = {}
    url_params['location'] = location
    url_params['term'] = keyword
    encoded_params = urllib.urlencode(url_params)
    host = 'api.yelp.com'
    path = '/v2/search'
    url = 'http://%s%s?%s' % (host, path, encoded_params)

    # Sign URL
    consumer = oauth2.Consumer(keys["YELP_KEY"], keys["YELP_SECRET"])
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': keys["YELP_TOKEN"],
                          'oauth_consumer_key': keys["YELP_KEY"]})

    token = oauth2.Token(keys["YELP_TOKEN"], keys["YELP_TOKEN_SECRET"])
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    # Connect
    try:
        conn = urllib2.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
    except urllib2.HTTPError, error:
        response = json.loads(error.read())

    return response
