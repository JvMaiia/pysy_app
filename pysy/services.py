from com.android.volley import Request
from com.android.volley import Response
from com.android.volley import toolbox
from com.android.volley.toolbox import Volley

class api():
    def __init__(self, activity):
        self.queue = Volley.newRequestQueue(activity)
