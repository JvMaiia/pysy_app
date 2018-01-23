import android
import android.view
from android.widget import (
    LinearLayout, RelativeLayout
    )
from android.graphics import Paint, PorterDuff

class DoctorItem:
    def __init__(self, context, doctor, callback=None):
        self.doctor = doctor
        self.callback = callback
        self.context = context
        self.layout = LinearLayout(self.context)

        self.text_view = TextView(self.context)
        self.text_view.setText(self.doctor['complete_name'] + ' | ' + self.doctor['especialization'])
        self.text_view.setTextSize(22)
        self.layout.addView(self.text_view)

    def getView(self):
        return self.layout

class DoctorsListAdapter(extends=android.widget.BaseAdapter):
    def __init__(self, context, doctors, listener=None):
        self.context = context
        self.doctors = list(doctors)
        self.listener = listener

    def getCount(self) -> int:
        return len(self.sdoctor)

    def getItem(self, position: int) -> java.lang.Object:
        return self.sdoctor[position]

    def getItemId(self, position: int) -> long:
        return self.sdoctor[position]['id']

    def getView(self, position: int,
                view: android.view.View,
                container: android.view.ViewGroup) -> android.view.View:
        doctor = self.getItem(position)
        doctorItem = DoctorItem(doctor, self.context, callback=self.listener)
        return doctorItem.getView()
