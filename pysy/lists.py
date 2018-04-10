import android
import android.view
from android.widget import (
    LinearLayout, RelativeLayout, TextView, Button
)
from android.graphics import Paint, PorterDuff


class ButtonClick(implements=android.view.View[OnClickListener]):

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def onClick(self, view: android.view.View) -> void:
        self.callback(*self.args, **self.kwargs)


def _create_layout_params(side):
    params = RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT,
                                         RelativeLayout.LayoutParams.WRAP_CONTENT)
    if side == 'right':
        params.addRule(RelativeLayout.ALIGN_PARENT_RIGHT)
    elif side == 'bottom':
        params.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM)

    return params


class DoctorItem:

    def __init__(self, context, doctor, callback=None):
        self.doctor = doctor
        self.callback = callback
        self.context = context
        self.layout = LinearLayout(self.context)

        self.text_view = TextView(self.context)
        self.text_view.setText(
            self.doctor['complete_name'] + ' | ' + self.doctor['especialization'])
        self.text_view.setTextSize(22)
        self.layout.addView(self.text_view)

    def getView(self):
        return self.layout


class DoctorsListAdapter(extends=android.widget.BaseAdapter):

    def __init__(self, context, doctors, listener=None):
        self.context = context
        self.doctors = doctors
        self.listener = listener

    def getCount(self) -> int:
        return len(self.doctors)

    def getItem(self, position: int) -> java.lang.Object:
        return self.doctors[position]

    def getItemId(self, position: int) -> long:
        return position

    def getView(self, position: int,
                view: android.view.View,
                container: android.view.ViewGroup) -> android.view.View:
        doctor = self.getItem(position)
        doctorItem = DoctorItem(self.context, doctor, callback=self.listener)
        return doctorItem.getView()


class PatientItem:

    def __init__(self, context, patient, callback=None):
        self.patient = patient
        self.callback = callback
        self.context = context
        self.layout = LinearLayout(self.context)

        self.text_view = TextView(self.context)
        self.text_view.setText(self.patient['complete_name'])
        self.text_view.setTextSize(22)
        self.layout.addView(self.text_view)

        self.details_button = Button(self.context)
        self.details_button.setOnClickListener(ButtonClick(self.view_patient))
        self.details_button.getBackground().setColorFilter(
            0xff9e9e9e, PorterDuff.Mode.MULTIPLY)
        self.details_button.setText('+')
        relative = RelativeLayout(self.context)
        relative.addView(self.details_button, _create_layout_params('right'))
        self.layout.addView(relative)

    def getView(self):
        return self.layout

    def view_patient(self):
        self.callback(event='details_patient', value=self.patient)


class PatientsListAdapter(extends=android.widget.BaseAdapter):

    def __init__(self, context, patients, listener=None):
        self.context = context
        self.patients = patients
        self.listener = listener

    def getCount(self) -> int:
        return len(self.patients)

    def getItem(self, position: int) -> java.lang.Object:
        return self.patients[position]

    def getItemId(self, position: int) -> long:
        return position

    def getView(self, position: int,
                view: android.view.View,
                container: android.view.ViewGroup) -> android.view.View:
        patient = self.getItem(position)
        patientItem = PatientItem(
            self.context, patient, callback=self.listener)
        return patientItem.getView()


class AppointmentItem:

    def __init__(self, context, appointment, callback=None):
        self.appointment = appointment
        self.callback = callback
        self.context = context
        self.layout = LinearLayout(self.context)

        self.text_view = TextView(self.context)
        first_name = self.appointment['patient'].split()[0]
        self.text_view.setText(
            first_name + ' | ' + self.appointment['state'])
        self.text_view.setTextSize(22)
        self.layout.addView(self.text_view)

        self.details_button = Button(self.context)
        self.details_button.setOnClickListener(
            ButtonClick(self.view_appointment))
        self.details_button.getBackground().setColorFilter(
            0xff9e9e9e, PorterDuff.Mode.MULTIPLY)
        self.details_button.setText('+')
        relative = RelativeLayout(self.context)
        relative.addView(self.details_button, _create_layout_params('right'))
        self.layout.addView(relative)

    def getView(self):
        return self.layout

    def view_appointment(self):
        self.callback(event='details_appointment', value=self.appointment)


class AppointmentsListAdapter(extends=android.widget.BaseAdapter):

    def __init__(self, context, appointments, listener=None):
        self.context = context
        self.appointments = appointments
        self.listener = listener

    def getCount(self) -> int:
        return len(self.appointments)

    def getItem(self, position: int) -> java.lang.Object:
        return self.appointments[position]

    def getItemId(self, position: int) -> long:
        return position

    def getView(self, position: int,
                view: android.view.View,
                container: android.view.ViewGroup) -> android.view.View:
        appointment = self.getItem(position)
        appointmentItem = AppointmentItem(
            self.context, appointment, callback=self.listener)
        return appointmentItem.getView()
