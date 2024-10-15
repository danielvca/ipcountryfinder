import os
from flask import Flask, jsonify, request, render_template
import geoip2.database
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import ipaddress

app = Flask(__name__)

# Rate limiter setup (500 requests per minute)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per minute"]
)

# Path to the MaxMind databases
db_path_country = './mdb/GeoLite2-Country.mmdb'
db_path_city = './mdb/GeoLite2-City.mmdb'
db_path_asn = './mdb/GeoLite2-ASN.mmdb'

# Readers for the MaxMind databases
country_reader = geoip2.database.Reader(db_path_country)
city_reader = geoip2.database.Reader(db_path_city)
asn_reader = geoip2.database.Reader(db_path_asn)


# API_KEY = 'U8hK29n!34DpaQv7Xtm1S@Z#9NyL6xBw'
# def check_api_key():
#     key = request.headers.get('x-api-key')
#     if key != API_KEY:
#         abort(403, description="Forbidden: Invalid API key")

# Function to get the real client IP
def get_client_ip():
    if 'CF-Connecting-IP' in request.headers:  # Cloudflare's own header for real IP
        return request.headers['CF-Connecting-IP']
    elif 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        return request.remote_addr

# Main index route (front-facing HTML page)
@app.route('/')
@limiter.limit("5 per minute")
def index():
    return render_template('index.html')  # Bootstrap frontend

# Country endpoint to get the country name
@app.route('/country', methods=['GET'])
@limiter.limit("500 per minute")
def get_country():
    ip_address = get_client_ip()
    try:
        response = country_reader.country(ip_address)
        return jsonify({"country": response.country.name})
    except geoip2.errors.AddressNotFoundError:
        return jsonify({"error": "IP address not found"}), 404

# City endpoint to get the city name
@app.route('/city', methods=['GET'])
@limiter.limit("500 per minute")
def get_city():
    ip_address = get_client_ip()
    try:
        response = city_reader.city(ip_address)
        return jsonify({"city": response.city.name})
    except geoip2.errors.AddressNotFoundError:
        return jsonify({"error": "IP address not found"}), 404

# Full JSON endpoint to get all details (IP, country, city, ASN, etc.)
@app.route('/json', methods=['GET'])
@limiter.limit("500 per minute")
def json_info():
    ip_address = get_client_ip()
    try:
        # Get country, city, and ASN data
        country_response = country_reader.country(ip_address)
        city_response = city_reader.city(ip_address)
        asn_response = asn_reader.asn(ip_address)

        # Prepare user agent info
        user_agent = request.headers.get('User-Agent', '')
        user_agent_parsed = {
            "product": "Mozilla",
            "version": "5.0",
            "comment": user_agent,
            "raw_value": user_agent
        }

        # Return the full JSON
        return jsonify({
            "ip": ip_address,
            "country": country_response.country.name,
            "country_iso": country_response.country.iso_code,
            "city": city_response.city.name,
            "region_name": city_response.subdivisions.most_specific.name,
            "region_code": city_response.subdivisions.most_specific.iso_code,
            "zip_code": city_response.postal.code,
            "latitude": city_response.location.latitude,
            "longitude": city_response.location.longitude,
            "time_zone": city_response.location.time_zone,
            "asn": asn_response.autonomous_system_number,
            "asn_org": asn_response.autonomous_system_organization,
            "user_agent": user_agent_parsed
        })
    except geoip2.errors.AddressNotFoundError:
        return jsonify({"error": "IP address not found"}), 404


# Error handling for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="Rate limit exceeded. Try again later."), 429

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
