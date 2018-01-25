import android
import android.view
from android.widget import (
    Button, EditText, LinearLayout, RelativeLayout,
    ListView, TextView, CheckBox
    )
from android.view import Gravity
from org.json import JSONArray
from .services import api
from .lists import (
    ButtonClick, _create_layout_params,
    DoctorsListAdapter,
    PatientsListAdapter,
    AppointmentsListAdapter
    )

class MainApp:
    def __init__(self):
        self._activity = android.PythonActivity.setListener(self)
        self.api = api(self._activity)
        self.doctorsItems = None
        self.patientsItems = None
        self.appointmentsItems = None

    def onCreate(self):
        self.vlayout = LinearLayout(self._activity)
        self.vlayout.setOrientation(LinearLayout.VERTICAL)
        self._activity.setContentView(self.vlayout)
        if self.api.token:
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

        self.add_error_text()

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
        view_appointments.setOnClickListener(ButtonClick(
            self.api.getAppointments,
            listener = self.successGetAppointments,
            listenerError = self.errorGet
            ))
        self.vlayout.addView(view_appointments)

        view_doctors = Button(self._activity)
        view_doctors.setText('View doctors')
        view_doctors.setOnClickListener(ButtonClick(
            self.api.getDoctors,
            listener = self.successGetDoctors,
            listenerError = self.errorGet
            ))
        self.vlayout.addView(view_doctors)

        view_patients = Button(self._activity)
        view_patients.setText('View patients')
        view_patients.setOnClickListener(ButtonClick(
            self.api.getPatients,
            listener = self.successGetPatients,
            listenerError = self.errorGet
            ))
        self.vlayout.addView(view_patients)

    def view_appointments(self):
        self.vlayout.removeAllViews()
        self.add_return_button(view='main', bottom=False)
        
        self.appointmentsAdapter = AppointmentsListAdapter(
            self._activity,
            self.appointmentsItems,
            listener = self._dispatch_event
            )
        self.appointmentsList = ListView(self._activity)
        self.appointmentsList.setAdapter(self.appointmentsAdapter)

        self.vlayout.addView(self.appointmentsList)

    def view_doctors(self):
        self.vlayout.removeAllViews()
        self.add_return_button(view='main', bottom=False)
        
        self.doctorsAdapter = DoctorsListAdapter(self._activity, self.doctorsItems)
        self.doctorsList = ListView(self._activity)
        self.doctorsList.setAdapter(self.doctorsAdapter)

        self.vlayout.addView(self.doctorsList)

    def view_patients(self):
        self.vlayout.removeAllViews()
        self.add_return_button(view='main', bottom=False)
        
        self.patientsAdapter = PatientsListAdapter(
            self._activity,
            self.patientsItems,
            listener = self._dispatch_event
            )
        self.patientsList = ListView(self._activity)
        self.patientsList.setAdapter(self.patientsAdapter)

        self.vlayout.addView(self.patientsList)

    def details_patient(self, patient):
        self.vlayout.removeAllViews()

        name_text = TextView(self._activity)
        name_text.setText('Patient: %s' % (patient.get('complete_name')))
        name_text.setTextSize(22)
        self.vlayout.addView(name_text)

        email_text = TextView(self._activity)
        email_text.setText('\nEmail: %s' % (patient.get('email')))
        email_text.setTextSize(22)
        self.vlayout.addView(email_text)

        birthdate_text = TextView(self._activity)
        birthdate_text.setText('\nBirth date: %s' % (patient.get('birth_date')))
        birthdate_text.setTextSize(22)
        self.vlayout.addView(birthdate_text)

        number_text = TextView(self._activity)
        number_text.setText('\nNumber: %s' % (patient.get('number_for_contact1')))
        number_text.setTextSize(22)
        self.vlayout.addView(number_text)

        self.add_return_button(view='view_patients')

    def details_appointment(self, appointment):
        self.vlayout.removeAllViews()

        patient_text = TextView(self._activity)
        patient_text.setText('Patient: %s' % (appointment.get('patient')))
        patient_text.setTextSize(22)
        self.vlayout.addView(patient_text)

        doctor_text = TextView(self._activity)
        doctor_text.setText('\nDoctor: %s' % (appointment.get('doctor')))
        doctor_text.setTextSize(22)
        self.vlayout.addView(doctor_text)

        date_text = TextView(self._activity)
        date = appointment.get('date').replace('T', ' ').replace('Z', ' ')
        date_text.setText('\nDate: %s' % (date))
        date_text.setTextSize(22)
        self.vlayout.addView(date_text)

        state_text = TextView(self._activity)
        state_text.setText('\nState: %s' % (appointment.get('state')))
        state_text.setTextSize(22)
        self.vlayout.addView(state_text)

        self.add_return_button(view='view_appointments')

    def create_appointments(self):
        pass

    def create_patients(self):
        pass

    def login(self):
        username = self.username_text.getText()
        password = self.password_text.getText()
        self.api.login(username, password, self.success_login, self.error_login)
        self.error_text.setText('loading')

    def success_login(self, res):
        token = str(res.get('token'))
        self.api.setToken(token)
        self.main_view()

    def successGetDoctors(self, res):
        self.doctorsItems = JSONArray(res)
        self.view_doctors(self)

    def successGetPatients(self, res):
        self.patientsItems = JSONArray(res)
        self.view_patients(self)

    def defineDoctors(self, res=False):
        if res:
            self.doctorsItems = JSONArray(res)

        for appointmentN in range(self.appointmentsItems.length()):
            appointment = self.appointmentsItems.get(appointmentN)
            doctor_id = appointment.get('doctor')
            for doctorN in range(self.doctorsItems.length()):
                doctor = self.doctorsItems.get(doctorN)
                if doctor.get('id') == doctor_id:
                    self.appointmentsItems.get(appointmentN).put('doctor', doctor.get('complete_name'))
                    break

            self.view_appointments(self)

    def successGetAppointments(self, res):
        self.appointmentsItems = JSONArray(res)

        if self.doctorsItems == None:
            self.api.getDoctors(
                listener = self.defineDoctors,
                listenerError = self.errorGet
            )
        else:
            self.defineDoctors()

    def findDoctor(self, res):
        doctors = JSONArray(res)
        for i in range(doctors.length()):
            doctor = doctors.get(i)
            if doctor.get('id') == self.doctor_id:
                self.appointment_doctor = doctor
                break

    def errorGet(self, err):
        print(err)

    def error_login(self, err):
        print(err)
        self.error_text.setText('something is wrong')

    def _dispatch_event(self, event=None, value=None):
        if event == 'details_patient':
            self.return_view('details_patient', value=value)
        elif event == 'details_appointment':
            self.return_view('details_appointment', value=value)

    def add_error_text(self):
        self.error_text = TextView(self._activity)
        self.vlayout.addView(self.error_text)

    def add_return_button(self, view, bottom=True):
        self.return_button = Button(self._activity)
        self.return_button.setOnClickListener(ButtonClick(self.return_view, view))
        self.return_button.setText('Return')
        self.relative_rb = RelativeLayout(self._activity)
        if bottom:
            self.relative_rb.addView(self.return_button, _create_layout_params('bottom'))
        else:
            self.relative_rb.addView(self.return_button)
        self.vlayout.addView(self.relative_rb)

    def return_view(self, view, value=None):
        if view == 'main':
            self.main_view()
        elif view == 'view_patients':
            self.view_patients()
        elif view == 'view_appointments':
            self.view_appointments()
        elif view == 'details_patient':
            self.details_patient(patient=value)
        elif view == 'details_appointment':
            self.details_appointment(appointment=value)

def main():
    MainApp()
