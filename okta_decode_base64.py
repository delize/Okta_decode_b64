import base64
import json
import requests
import argparse
def parse_args():
    parser = argparse.ArgumentParser(description="Process inputs for asset automation for decoding BASE64 encoded values from AD to Okta.")
    parser.add_argument('--token', type=str, default="You didn't insert a token!", help="Your API token from Okta")
    parser.add_argument('--url', type=str, default="companyname.okta.com", help="Your Okta URL, do not add https://")
    parser.add_argument('--attribute', type=str, default="attributename", help="The Okta attribute value you need decoded")
    args = parser.parse_args()
    return(args.token, args.url, args.attribute)


def GetUsers():
    user_data = []
    headers = {"Authorization": "SSWS %s" % token }
    next_user_link = 'https://'+ url +'/api/v1/users/?filter=status eq "ACTIVE"'
    while next_user_link:
        response = requests.get(next_user_link, headers=headers)
        if response.status_code not in [200, 201]:
            print(response.text)
            exit()
        user_data += response.json()
        next_user_link = None    
        response_headers = dict(response.headers)
        #print(json.dumps(response_headers))
        for link in response_headers["Link"].split(","):
            if "next" in link:
                next_user_link = link.split("<")[1].split(">")[0]
    return user_data
def UpdateUserProfile(user_id, profile_data):    
    headers = {"Authorization": "SSWS %s" % token }
    #result = requests.post("https://" + url + "/api/v1/users/%s" % user_id, json=profile_data, headers=headers)
    if result.status_code not in [200, 201]:
        print(result.text)
def UpdateUserBatch(users):
    for user in users:
        if '"'+ attribute +'"' in user["profile"].keys() and user["profile"]['"'+ attribute +'"']:
            new_attribute = base64.b64decode(user["profile"]['"'+ attribute +'"']).decode("UTF-8")
            if not new_attribute or '/' in new_attribute or len(new_attribute) < 25:
                print("got an empty token from a non-empty b64 token, or a bad output! %s" % user["profile"]['"'+ attribute +'"'])
                exit()
            user["profile"]['"'+ attribute +'"'] = new_attribute
            UpdateUserProfile(user['id'], user["profile"])
def PrintAttributeInformation(users):
    for user in users:
        if '"'+ attribute +'"' in user["profile"].keys() and user["profile"]['"'+ attribute +'"']:
            print("%s %s %s" % (user["id"], user["profile"]["login"], user["profile"]['"'+ attribute +'"']))

user_data = GetUsers()
PrintAttributeInformation(user_data)