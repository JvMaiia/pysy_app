import android
import android.view
from android.widget import (
    Button, EditText, LinearLayout, RelativeLayout,
    ListView, TextView, CheckBox
    )
from android.view import Gravity
from .services import api

class ButtonClick(implements=android.view.View[OnClickListener]):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onClick(self, view: android.view.View) -> void:
        self.callback(*self.args, **self.kwargs)


class MainApp:
    def __init__(self):
        self._activity = android.PythonActivity.setListener(self)
        self.token = None

    def onCreate(self):
        self.vlayout = LinearLayout(self._activity)
        self.vlayout.setOrientation(LinearLayout.VERTICAL)
        self._activity.setContentView(self.vlayout)
        if self.token:
            self.main_view()
        else:
            self.login_view()

    def login_view(self):
        self.vlayout.removeAllViews()

        self.username_text = EditText(self._activity)
        self.username_text.setHint('Username')
        self.vlayout.addView(self.username_text)

        self.password_text = EditText(self._activity)
        self.password_text.setHint('Password')
        self.password_text.setInputType(0x00000001 | 0x00000080)
        self.vlayout.addView(self.password_text)

        login_button = Button(self._activity)
        login_button.setText('Login')
        login_button.setOnClickListener(ButtonClick(self.login))
        self.vlayout.addView(login_button)

    def main_view(self):
        self.vlayout.removeAllViews()

        create_appointments = Button(self._activity)
        create_appointments.setText('Create appointments')
        create_appointments.setOnClickListener(ButtonClick(self.create_appointments))
        self.vlayout.addView(create_appointments)

        create_patients = Button(self._activity)
        create_patients.setText('Create patients')
        create_patients.setOnClickListener(ButtonClick(self.create_patients))
        self.vlayout.addView(create_patients)

        view_appointments = Button(self._activity)
        view_appointments.setText('View appointments')
        view_appointments.setOnClickListener(ButtonClick(self.view_appointments))
        self.vlayout.addView(view_appointments)

        view_doctors = Button(self._activity)
        view_doctors.setText('View doctors')
        view_doctors.setOnClickListener(ButtonClick(self.view_doctors))
        self.vlayout.addView(view_doctors)

        view_patients = Button(self._activity)
        view_patients.setText('View patients')
        view_patients.setOnClickListener(ButtonClick(self.view_patients))
        self.vlayout.addView(view_patients)

    def view_appointments(self):
        pass

    def view_doctors(self):
        pass

    def view_patients(self):
        pass

    def create_appointments(self):
        pass

    def create_patients(self):
        pass

    def login(self):
        pass

def main():
    MainApp()
