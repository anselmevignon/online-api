# online-api
A shell-friendly python client for using online API

This script implements accessing and extracting data from the online.net API (https://console.online.net/en/api/)

## Install
    
  from the cloned repository
  pip install . --upgrade -r requirements.txt

## Configuration:

You need to write a script configuration, located by default in /etc/online.secret:

    {
        "access_token" : "YOUR_ACCESS_TOKEN"
    }

The access token is available in online.net console, under the API menu.
    
## Example Usage

Two commands are available: 
  - `get`: get a given endpoint,
  - `get_parsed`: return a jsonpathed endpoint.
  
examples

     $./online_api.py get user
     first_name: Roger
     last_name:  Rabbit
     company:    ACME Inc.
     email:      sysadmin@acme.inc
     login:      roger.rabbit
     id:         XXXXXX
    
     $./online_api.py get server/failover
     {"status": "active", "contacts": {"owner": "acme", "tech": "acme"}, "destination": "XXX.XXX.XXX.XXX", "server": {"$ref": "/api/v1/server/XXXXXX"}, "source": "XXX.XXX.XXX.XXX", "mac": null}
     {"status": "active", "contacts": {"owner": "acme", "tech": "acme"}, "destination": "XXX.XXX.XXX.XXX", "server": {"$ref": "/api/v1/server/XXXXXX"}, "source": "XXX.XXX.XXX.XXX", "mac": null}

     $./online_api.py get_parsed server/failover server.failover '$[*].contacts.owner'
     acme
     acme

for a full reference of the available endpoints, see: https://console.online.net/en/api/
for an introduction to jsonpath, see: https://github.com/json-path/JsonPath

## (not so) Advanced usage

The conf path is configurable via the `ONLINE_TOKEN_FILE` environment variable. 

## requirements:

 - fire
 - slumber
 - request
 - jsonpath_rw
