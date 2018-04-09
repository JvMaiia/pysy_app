from org.json import JSONObject, JSONArray


def getKeysObject(jsonObject):
    keys = []
    keysIterator = jsonObject.keySet().iterator()
    while keysIterator.hasNext():
        keys.append(keysIterator.next())

    return keys


def getKeysArray(jsonArray):
    length = jsonArray.length()
    keys = [i for i in range(length)]
    return keys


def jsonObjToDict(json):
    keys = getKeysObject(json)
    json_dict = {}
    for key in keys:
        if json.isNull(key):
            value = None
        else:
            try:
                value = jsonObjToDict(json.getJSONObject(key))
            except:
                try:
                    value = jsonArrayToDict(json.getJSONArray(key))
                except:
                    value = json.get(key)
        json_dict[key] = value

    return json_dict


def jsonArrayToDict(json):
    keys = getKeysArray(json)
    json_array = []
    for key in keys:
        value = json.get(key)
        try:
            value = jsonObjToDict(value)
        except:
            try:
                value = jsonArrayToDict(json.getJSONArray(key))
            except:
                value = json.get(key)

        json_array.append(value)

    return json_array


def loads(s):
    if s.startswith('{'):
        objJson = JSONObject(s)
        python_json = jsonObjToDict(objJson)
    else:
        arrayjson = JSONArray(s)
        python_json = jsonArrayToDict(arrayjson)

    return python_json


def dictToJsonObject(d):
    json = JSONObject()
    for key in d:
        value = d[key]
        if value is None:
            value = JSONObject.NULL
        elif isinstance(value, dict):
            value = dictToJsonObject(value)
        elif isinstance(value, list):
            value = listToJsonArray(value)
        json.put(key, value)

    return json


def listToJsonArray(d):
    json = JSONArray()
    for item in d:
        if isinstance(item, dict):
            value = dictToJsonObject(item)
        else:
            value = listToJsonArray(item)
        json.put(value)

    return json


def dumps(obj):
    if isinstance(obj, dict):
        json = dictToJsonObject(obj)
    else:
        json = listToJsonArray(obj)

    json_string = json.toString()
    return json_string
