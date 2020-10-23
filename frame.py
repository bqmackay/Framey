import json

#define function that converts an http json response and turns it into roomy json.
def frame_roomy_from_json_response(json, class_name, package):

    top_object = {}
    top_object["name"] = class_name
    top_object["package"] = package
    top_object["baseClass"] = "*"

    members = []

    for key, value in json.items():
        if key == "success":
            continue

        object_dict = {}
        object_dict["name"] = key[0].lower() + key[1:]
        object_dict["serializedName"] = key[0].upper() + key[1:]

        if isinstance(value, dict):
            object_dict["type"] = "class"
            object_dict["class"] = "com.chatbooks.room.model.*." + key
            frame_roomy_from_json_response(value, key[0].upper() + key[1:], package)

        if isinstance(value, list):
            object_dict["type"] = "class[]"
            object_dict["class"] = "com.chatbooks.room.model.*." + key[0:-1]
            frame_roomy_from_json_response(value[0], key[0].upper() + key[1:], package)

        elif isinstance(value, int):
            if key.endswith("id"):
                object_dict["class"] = "kotlin.Long"
            else:
                object_dict["class"] = "kotlin.Int"

        elif isinstance(value, str):
            object_dict["class"] = "kotlin.String"

        elif isinstance(value, bool):
            object_dict["class"] = "kotlin.Boolean"

        else:
            print("Couldn't find type for " + key)

        members.append(object_dict)

    top_object["members"] = members

    output.insert(0, top_object)

path = input("Path to response file: ")
# path = "sub.json"
file = open(path,)
data = json.load(file)

package = input("What package will this go into? ")
# package = "groups"

# baseclass = input ("what basclass will the top object be using? ")
# baseclass = "com.chatbooks.room.model.common.SimpleResponse"

top_class_name = input ("what is the name of the top object? ")
# top_class_name = "ActiveSubscriptionsResponse"

output = []
frame_roomy_from_json_response(data, top_class_name, package)

json_output = json.dumps(output, indent = 2)

print(json_output)
