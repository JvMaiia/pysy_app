package android;

import com.android.volley.Response;
import com.android.volley.Response.ErrorListener;
import com.android.volley.Response.Listener;

import java.util.HashMap;

public class PythonVolleyStringRequest extends com.android.volley.toolbox.StringRequest {
    private HashMap<String, String> mHeaders;

    public PythonVolleyStringRequest(int method, String url, Listener<String> listener,
            ErrorListener errorListener, HashMap<String, String> headers) {
        super(method, url, listener, errorListener);
        mHeaders = headers;
    }

    public void setHeaders(HashMap<String, String> headers) {
        mHeaders = headers;
    }

    public HashMap<String, String> getHeaders() {
        return mHeaders;
    }
}
