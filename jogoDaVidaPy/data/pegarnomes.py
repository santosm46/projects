import json
import urllib
import requests

SAVES_PATH = './'
filename = 'names.txt'


# where = urllib.parse.quote_plus("""
# {
#     "Name": {
#         "$exists": true
#     },
#     "Genre": {
#         "$exists": true
#     }
# }
# """)
# url = 'https://parseapi.back4app.com/classes/NamesList?limit=10000&excludeKeys=Letter&where=%s' % where
# headers = {
#     'X-Parse-Application-Id': 'zsSkPsDYTc2hmphLjjs9hz2Q3EXmnSxUyXnouj1I', # This is the fake app's application id
#     'X-Parse-Master-Key': '4LuCXgPPXXO2sU5cXm6WwpwzaKyZpo3Wpj4G4xXK' # This is the fake app's readonly master key
# }
# data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need

# with open(f"{SAVES_PATH}{filename}", 'w') as outfile:
#     json.dump(data, outfile)
# print(json.dumps(data, indent=4))


with open(f"{SAVES_PATH}{filename}", 'r+') as json_file:
    data = json.load(json_file)

# print(json.dumps(data, indent=4))
print(type(data))


# with open(f"{SAVES_PATH}{filename}", 'w') as outfile:
#     json.dump(data, outfile)

# print(len(data["results"]))