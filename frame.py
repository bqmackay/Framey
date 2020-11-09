import json
import sys

DEBUG = True

def print_debug(value):
    if DEBUG:
        print(value)

#define function that converts an http json response and turns it into roomy json.
def frame_roomy_from_json_response(json, class_name, package):

    top_object = {}
    top_object["name"] = class_name
    top_object["package"] = package
    top_object["baseClass"] = "*"

    members = []

    if isinstance(json, list):
        transformed_dict = {"objects": json}
        json = transformed_dict

    for key, value in json.items():
        if key == "success":
            continue

        object_dict = {}
        object_dict["name"] = key[0].lower() + key[1:]
        object_dict["serializedName"] = key

        if isinstance(value, dict):
            print_debug("%s is a dict: %s" % (key, value))
            object_dict["type"] = "class"
            object_dict["class"] = "com.chatbooks.room.model.*." + key
            if bool(dict):
                frame_roomy_from_json_response(value, key[0].upper() + key[1:], package)

        if isinstance(value, list):
            print_debug("%s is a list: %s" % (key, value))
            object_dict["type"] = "class[]"
            object_dict["class"] = "com.chatbooks.room.model.*." + key[0:-1]
            new_key = key[0].upper() + key[1:]
            if len(value) > 0 and isinstance(value[0], dict):
                frame_roomy_from_json_response(value[0], new_key, package)

        elif isinstance(value, bool):
            print_debug("%s is a bool: %s" % (key, value))
            object_dict["class"] = "kotlin.Boolean"

        elif isinstance(value, int):
            if key.lower().endswith("id"):
                print_debug("%s is a long: %s" % (key, value))
                object_dict["class"] = "kotlin.Long"
            else:
                print_debug("%s is a int: %s" % (key, value))
                object_dict["class"] = "kotlin.Int"

        elif isinstance(value, str):
            print_debug("%s is a string: %s" % (key, value))
            object_dict["class"] = "kotlin.String"

        else:
            print("Couldn't find type for %s" % key)

        members.append(object_dict)

    top_object["members"] = members
    top_object["gson"] = True
    top_object["parcelable"] = True

    output.insert(0, top_object)

if len(sys.argv) < 2:
    path = input("Path to response file: ")
else:
    path = sys.argv[1]
# path = "sub.json"
file = open(path,)
data = json.load(file)

if len(sys.argv) < 3:
    package = input("What package will this go into? ")
else:
    package = sys.argv[2]

# package = "groups"

# baseclass = input ("what basclass will the top object be using? ")
# baseclass = "com.chatbooks.room.model.common.SimpleResponse"

if len(sys.argv) < 4:
    top_class_name = input ("what is the name of the top object? ")
else:
    top_class_name = sys.argv[3]

# top_class_name = "ActiveSubscriptionsResponse"

output = []
frame_roomy_from_json_response(data, top_class_name, package)

json_output = json.dumps(output, indent = 2)

print(json_output)
