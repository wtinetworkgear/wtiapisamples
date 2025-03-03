#!/usr/bin/env python
import requests

# supress Unverified HTTPS request, only do this in a verified environment
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Address of the WTI device
URI             = "https://"
SITE_NAME       = "192.168.0.25"

# put in the username and password to your WTI device here
BASE_PATH = "/api/v2/status/hostname"
USERNAME  = "super"
PASSWORD  = "super"
AUTH = (USERNAME, PASSWORD)
HEADER = ""

# or if using user tokens put in the User's Token to your WTI device here
#BASE_PATH = "/api/v2/token/status/hostname"
#HEADER = {"X-WTI-API-KEY":"!m+-w-~qo0aq78n=wgyz2c54c365rknj3rnguew8!4mztzx-6j2wlwoonbh4s1cj"}
#AUTH = ""

def key_exists(json_obj, topkey, key):
	if topkey in json_obj and key in json_obj["unitid"]:
		return 1
	else:
		return 0

try:
	# early hostname API would only return 'hostname' which was the Site ID of the unit.
	iEarlyAPIQuirk = 0

	r = requests.get(URI+SITE_NAME+BASE_PATH, verify=False, auth=AUTH, headers=HEADER)

	if (r.status_code == 200):
		parsed_json = r.json()

#		Uncomment to see the JSON return by the unit
#		print (parsed_json)

		cszSiteID = cszHostname = cszLocation = cszAssetTag = cszDomain = cszTimeStamp = ""
		cszHostname = parsed_json['unitid']['hostname']
		cszTimeStamp = parsed_json['unitid']['timestamp']

		if (key_exists(parsed_json, "unitid", "siteid") == 1):
			cszSiteID = parsed_json['unitid']['siteid']
			cszLocation = parsed_json['unitid']['location']			
			cszAssetTag = parsed_json['unitid']['assettag']
			cszDomain = parsed_json['unitid']['domain']			
		else:
			# early API version bug
			cszSiteID = parsed_json['unitid']['hostname']
			iEarlyAPIQuirk = 1

		print("Current Unit Identification:")
		print("----------------------------")
		if (iEarlyAPIQuirk == 0):
			print(f"Site ID:       {cszSiteID}" )	
			print(f"Location Name: {cszLocation}" )
			print(f"Asset Tag:     {cszAssetTag}" )
			print(f"Domain:        {cszDomain}" )

		print(f"Hostname:      {cszHostname}\r\n" )	
		print(f"Calling URL:   {URI+SITE_NAME+BASE_PATH}\r\n")
	else:
		print(r.status_code)

except requests.exceptions.RequestException as e:
	print ("Exception:")
	print (e)
