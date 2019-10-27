Pysy
====

An app to work with that api https://github.com/jvmaia/pysy

## How to run in development

Ensure that you have [Android SDK](https://developer.android.com/studio/index.html#downloads) installed.

Install the Python development requirements:

    pip install -r requirements-dev.txt

[Plug in your Android device](https://developer.android.com/training/basics/firstapp/running-app.html) or [start an emulator](https://developer.android.com/studio/run/emulator-commandline.html).

Create the file pysy/servers.py and add the two variables (host, port) with the address of your server running the pysy api

Build and run the app:

    python setup.py android --start

