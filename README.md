# IP Country Finder

This is a simple application that provides geolocation information based on the user's IP address. It uses the MaxMind GeoLite2 databases to lookup country, city, and ASN details.

### Features

* **Country lookup:** Returns the country name based on the user's IP address.
* **City lookup:** Returns the city name based on the user's IP address.
* **Full JSON endpoint:** Returns a comprehensive JSON object containing:
    * IP address
    * Country name and ISO code
    * City name
    * Region name and code
    * Postal code
    * Latitude and longitude
    * Time zone
    * ASN and ASN organization
    * User agent information
* **Rate limiting:** Limits requests to prevent abuse.
* **Dockerized:** Easy to deploy using Docker.
* **Frontend:** Simple HTML page using Bootstrap to display the information.

### Requirements

* Python 3.8
* Flask
* geoip2
* Flask-Limiter
* ipaddress

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/danielvca/ipcountryfinder.git

2. Download the MaxMind GeoLite2 databases:

````

GeoLite2-Country.mmdb

GeoLite2-City.mmdb

GeoLite2-ASN.mmdb
````

Create a directory called: mdb

Place the .mmdb files in the mdb directory.

3. Build the Docker image:

````
docker build -t ip-country-finder .
````

## Usage
Run the Docker container:

````
docker run -d -p 5002:5000 --name IPFinder ip-country-finder
````


Access the application in your browser at http://localhost:5002/.

# API Endpoints

````
/country: Returns the country name.

/city: Returns the city name.

/json: Returns the full JSON object.

Rate Limits:
Edit the app.py to set your own limits


````
## GeoIP/GeoLite Database (MaxMind)
You can download the relevant binary databases (.mmdb format) directly from MaxMind using the below link:

https://dev.maxmind.com/geoip/geolite2-free-geolocation-data


Please Note: You will need to create a free account in order to download the files.
This solution does not cover automatic database refresh.

## Notes
The application uses Cloudflare headers (CF-Connecting-IP) to get the real client IP address if available.

The X-Forwarded-For header is used as a fallback if the Cloudflare header is not present.

The user_agent field in the JSON response is parsed to provide basic information.

The HTML page uses JavaScript to fetch and display the data from the /json endpoint.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
