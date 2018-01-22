from com.android.volley import Request
from com.android.volley import Response
from com.android.volley import toolbox
from com.android.volley.toolbox import Volley
from org.json import (
        JSONArray,
        JSONException,
        JSONObject
    )
from .server import host, port

base_url = 'http://' + str(host) + ':' + str(port) + '/api'

class OnResponse(implements=com.android.volley.Response[Listener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onResponse(self, response: java.lang.Object) -> void:
        self.callback(*self.args, **self.kwargs, res=response)

class OnError(implements=com.android.volley.Response[ErrorListener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onErrorResponse(self, error: com.android.volley.VolleyError) -> void:
        self.callback(*self.args, **self.kwargs, err=error)

class api():
    def __init__(self, activity):
        self.queue = Volley.newRequestQueue(activity)
        self.url_login = base_url + '/api-token-auth/'
        self.url_doctors = base_url + '/doctors'
        self.url_patients = base_url + '/patients'
        self.url_appointments = base_url + '/appointments'

    def login(self, username, password, listener, listenerError):
        username = str(username)
        password = str(password)

        credentials = JSONObject()
        credentials.put('username', username)
        credentials.put('password', password)

        loginrequest = toolbox.JsonObjectRequest(
            Request.Method.POST,
            self.url_login,
            credentials,
            OnResponse(listener),
            OnError(listenerError)
        )

        self.queue.add(loginrequest)
