import android
import android.view
import com.jvmaia.pysy.R.layout
from android.widget import (
    Button, EditText, LinearLayout, RelativeLayout,
    ListView, TextView, Spinner, NumberPicker,
    ArrayAdapter, FrameLayout
)
from android.view import Gravity
from org.json import JSONArray, JSONObject
from .services import api
from .lists import (
    ButtonClick, _create_layout_params,
    DoctorsListAdapter,
    PatientsListAdapter,
    AppointmentsListAdapter
)
from .PythonJavaJSON import dictToJsonObject, loads


class MainApp:

    def __init__(self):
        self._activity = android.PythonActivity.setListener(self)
        self.api = api(self._activity)
        self.doctorsItems = None
        self.patientsItems = None
        self.appointmentsItems = None
        self.statesItems = None
        self.actual_view = None

    def onCreate(self):
        self.vlayout = LinearLayout(self._activity)
        self.vlayout.setOrientation(LinearLayout.VERTICAL)
        self.flayout = FrameLayout(self._activity)
        self._activity.setContentView(self.vlayout)
        self.text_view = TextView(self._activity)
        if self.api.token:
            self.main_view()
        else:
            self.login_view()

    def login_view(self):
        self.actual_view = 'login'
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
        self.actual_view = 'main'
        self.flayout.removeAllViews()
        self.vlayout.removeAllViews()

        create_appointments = Button(self._activity)
        create_appointments.setText('Create appointments')
        create_appointments.setOnClickListener(
            ButtonClick(self.create_appointment_view))
        self.vlayout.addView(create_appointments)

        create_patient = Button(self._activity)
        create_patient.setText('Create patients')
        create_patient.setOnClickListener(
            ButtonClick(self.create_patient_view))
        self.vlayout.addView(create_patient)

        create_doctor = Button(self._activity)
        create_doctor.setText('Create doctors')
        create_doctor.setOnClickListener(ButtonClick(self.create_doctor_view))
        self.vlayout.addView(create_doctor)

        view_appointments = Button(self._activity)
        view_appointments.setText('View appointments')
        view_appointments.setOnClickListener(ButtonClick(
            self.api.getAppointments,
            listener=self.successGetAppointments,
            listenerError=self.errorGet
        ))
        self.vlayout.addView(view_appointments)

        view_doctors = Button(self._activity)
        view_doctors.setText('View doctors')
        view_doctors.setOnClickListener(ButtonClick(
            self.api.getDoctors,
            listener=self.successGetDoctors,
            listenerError=self.errorGet
        ))
        self.vlayout.addView(view_doctors)

        view_patients = Button(self._activity)
        view_patients.setText('View patients')
        view_patients.setOnClickListener(ButtonClick(
            self.api.getPatients,
            listener=self.successGetPatients,
            listenerError=self.errorGet
        ))
        self.vlayout.addView(view_patients)

    def view_appointments(self):
        self.actual_view = 'appointments'
        self.vlayout.removeAllViews()
        self.flayout.removeAllViews()
        self.vlayout.addView(self.flayout)

        self.appointmentsAdapter = AppointmentsListAdapter(
            self._activity,
            self.appointmentsItems,
            listener=self._dispatch_event
        )
        self.appointmentsList = ListView(self._activity)
        self.appointmentsList.setAdapter(self.appointmentsAdapter)

        self.flayout.addView(self.appointmentsList)
        self.add_return_button(view='main', flayout=True)

    def view_doctors(self):
        self.actual_view = 'doctors'
        self.vlayout.removeAllViews()
        self.flayout.removeAllViews()
        self.vlayout.addView(self.flayout)

        self.doctorsAdapter = DoctorsListAdapter(
            self._activity, self.doctorsItems)
        self.doctorsList = ListView(self._activity)
        self.doctorsList.setAdapter(self.doctorsAdapter)

        self.flayout.addView(self.doctorsList)
        self.add_return_button(view='main', flayout=True)

    def view_patients(self):
        self.actual_view = 'patients'
        self.vlayout.removeAllViews()
        self.flayout.removeAllViews()
        self.vlayout.addView(self.flayout)

        self.patientsAdapter = PatientsListAdapter(
            self._activity,
            self.patientsItems,
            listener=self._dispatch_event
        )
        self.patientsList = ListView(self._activity)
        self.patientsList.setAdapter(self.patientsAdapter)

        self.flayout.addView(self.patientsList)
        self.add_return_button(view='main', flayout=True)

    def details_patient(self, patient):
        self.actual_view = 'details_patient'
        self.vlayout.removeAllViews()
        self.patient = patient

        name_text = TextView(self._activity)
        name_text.setText('Patient: %s' % (patient['complete_name']))
        name_text.setTextSize(22)
        self.vlayout.addView(name_text)

        email_text = TextView(self._activity)
        email_text.setText('\nEmail: %s' % (patient['email']))
        email_text.setTextSize(22)
        self.vlayout.addView(email_text)

        birthdate_text = TextView(self._activity)
        birthdate_text.setText('\nBirth date: %s' %
                               (patient['birth_date']))
        birthdate_text.setTextSize(22)
        self.vlayout.addView(birthdate_text)

        number_text = TextView(self._activity)
        number_text.setText('\nNumber: %s' %
                            (patient['number_for_contact1']))
        number_text.setTextSize(22)
        self.vlayout.addView(number_text)

        number_text = TextView(self._activity)
        number_text.setText('\nNumber 2: %s' %
                            (patient['number_for_contact2']))
        number_text.setTextSize(22)
        self.vlayout.addView(number_text)

        self.add_modify_button('patient', patient)
        self.add_return_button(view='view_patients')

    def details_appointment(self, appointment):
        self.actual_view = 'details_appointment'
        self.vlayout.removeAllViews()

        patient_text = TextView(self._activity)
        patient_text.setText('Patient: %s' % (appointment['patient']))
        patient_text.setTextSize(22)
        self.vlayout.addView(patient_text)

        doctor_text = TextView(self._activity)
        doctor_text.setText('\nDoctor: %s' % (appointment['doctor']))
        doctor_text.setTextSize(22)
        self.vlayout.addView(doctor_text)

        date_text = TextView(self._activity)
        date = appointment['date'].replace('T', ' ').replace('Z', ' ')
        date_text.setText('\nDate: %s' % (date))
        date_text.setTextSize(22)
        self.vlayout.addView(date_text)

        state_text = TextView(self._activity)
        state_text.setText('\nState: %s' % (appointment['state']))
        state_text.setTextSize(22)
        self.vlayout.addView(state_text)

        self.add_return_button(view='view_appointments')

    def create_appointment_view(self):
        if self.statesItems == None or self.doctorsItems == None or self.patientsItems == None:
            return
        self.actual_view = 'create_appointment'

        self.vlayout.removeAllViews()
        self.vlayout.addView(self.flayout)
        vlayout = LinearLayout(self._activity)
        vlayout.setOrientation(LinearLayout.VERTICAL)
        self.flayout.addView(vlayout)

        horizontalPatient = LinearLayout(self._activity)
        horizontalPatient.setOrientation(LinearLayout.HORIZONTAL)
        patient_text = TextView(self._activity)
        patient_text.setText('Patient: ')
        patient_text.setTextSize(18)
        horizontalPatient.addView(patient_text)
        self.patient_spinner = Spinner(self._activity)
        patients = []
        for i in range(self.patientsItems.length()):
            patients.append(self.patientsItems[i]['complete_name'])

        patientsAdapter = ArrayAdapter(self._activity, 0x01090008, patients)
        patientsAdapter.setDropDownViewResource(0x01090009)
        self.patient_spinner.setAdapter(patientsAdapter)
        horizontalPatient.addView(self.patient_spinner)

        vlayout.addView(horizontalPatient)

        horizontalDoctor = LinearLayout(self._activity)
        horizontalDoctor.setOrientation(LinearLayout.HORIZONTAL)
        doctor_text = TextView(self._activity)
        doctor_text.setText('Doctor: ')
        doctor_text.setTextSize(18)
        self.doctor_spinner = Spinner(self._activity)
        doctors = []
        for i in range(self.doctorsItems.length()):
            doctors.append(self.doctorsItems[i]['complete_name'])
        doctorsAdapter = ArrayAdapter(self._activity, 0x01090008, doctors)
        doctorsAdapter.setDropDownViewResource(0x01090009)
        self.doctor_spinner.setAdapter(doctorsAdapter)
        horizontalDoctor.addView(doctor_text)
        horizontalDoctor.addView(self.doctor_spinner)

        vlayout.addView(horizontalDoctor)

        horizontalState = LinearLayout(self._activity)
        horizontalState.setOrientation(LinearLayout.HORIZONTAL)
        state_text = TextView(self._activity)
        state_text.setText('State: ')
        state_text.setTextSize(18)
        self.state_spinner = Spinner(self._activity)
        states = []
        for i in range(self.statesItems.length()):
            states.append(self.statesItems[i]['name'])
        statesAdapter = ArrayAdapter(self._activity, 0x01090008, states)
        statesAdapter.setDropDownViewResource(0x01090009)
        self.state_spinner.setAdapter(statesAdapter)
        horizontalState.addView(state_text)
        horizontalState.addView(self.state_spinner)

        vlayout.addView(horizontalState)

        horizontalDate = LinearLayout(self._activity)
        horizontalDate.setOrientation(LinearLayout.HORIZONTAL)
        date_text = TextView(self._activity)
        date_text.setText('Date:')
        date_text.setTextSize(18)
        horizontalDate.addView(date_text)

        self.appointmentDateD = NumberPicker(self._activity)
        self.appointmentDateD.setMinValue(1)
        self.appointmentDateD.setMaxValue(31)
        horizontalDate.addView(self.appointmentDateD)
        self.appointmentDateM = NumberPicker(self._activity)
        self.appointmentDateM.setMinValue(1)
        self.appointmentDateM.setMaxValue(12)
        horizontalDate.addView(self.appointmentDateM)
        self.appointmentDateY = NumberPicker(self._activity)
        self.appointmentDateY.setMinValue(2018)
        self.appointmentDateY.setMaxValue(2099)
        horizontalDate.addView(self.appointmentDateY)

        vlayout.addView(horizontalDate)

        horizontalTime = LinearLayout(self._activity)
        horizontalTime.setOrientation(LinearLayout.HORIZONTAL)
        time_text = TextView(self._activity)
        time_text.setText('Time:')
        time_text.setTextSize(18)
        horizontalTime.addView(time_text)

        self.appointmentTimeH = NumberPicker(self._activity)
        self.appointmentTimeH.setMinValue(6)
        self.appointmentTimeH.setMaxValue(19)
        horizontalTime.addView(self.appointmentTimeH)
        self.appointmentTimeM = NumberPicker(self._activity)
        self.appointmentTimeM.setMinValue(1)
        self.appointmentTimeM.setMaxValue(60)
        horizontalTime.addView(self.appointmentTimeM)

        vlayout.addView(horizontalTime)

        create_button = Button(self._activity)
        create_button.setOnClickListener(ButtonClick(self.create_appointment))
        create_button.setText('Create appointment')
        vlayout.addView(create_button)
        self.add_error_text()

        self.add_return_button('main')

    def create_patient_view(self):
        self.actual_view = 'create_patient'
        self.vlayout.removeAllViews()
        self.vlayout.addView(self.flayout)
        vlayout = LinearLayout(self._activity)
        vlayout.setOrientation(LinearLayout.VERTICAL)
        self.flayout.addView(vlayout)

        self.patient_name = EditText(self._activity)
        self.patient_name.setHint('Patient name')
        self.patient_name.setInputType(0x00000001)
        vlayout.addView(self.patient_name)

        self.patient_rg = EditText(self._activity)
        self.patient_rg.setHint('Patient RG')
        self.patient_rg.setInputType(0x00000002)
        vlayout.addView(self.patient_rg)

        horizontal = LinearLayout(self._activity)
        horizontal.setOrientation(LinearLayout.HORIZONTAL)

        birthdate_text = TextView(self._activity)
        birthdate_text.setText('Patient birth date:')
        birthdate_text.setTextSize(20)
        horizontal.addView(birthdate_text)

        self.birthdateD = NumberPicker(self._activity)
        self.birthdateD.setMinValue(1)
        self.birthdateD.setMaxValue(31)
        horizontal.addView(self.birthdateD)
        self.birthdateM = NumberPicker(self._activity)
        self.birthdateM.setMinValue(1)
        self.birthdateM.setMaxValue(12)
        horizontal.addView(self.birthdateM)
        self.birthdateY = NumberPicker(self._activity)
        self.birthdateY.setMinValue(1900)
        self.birthdateY.setMaxValue(2100)
        horizontal.addView(self.birthdateY)

        vlayout.addView(horizontal)

        self.patient_number1 = EditText(self._activity)
        self.patient_number1.setHint('Patient number 1')
        self.patient_number1.setInputType(0x00000002)
        vlayout.addView(self.patient_number1)

        self.patient_number2 = EditText(self._activity)
        self.patient_number2.setHint('Patient number 2')
        self.patient_number2.setInputType(0x00000002)
        vlayout.addView(self.patient_number2)

        self.patient_email = EditText(self._activity)
        self.patient_email.setHint('Patient email')
        self.patient_email.setInputType(0x00000020)
        vlayout.addView(self.patient_email)

        create_button = Button(self._activity)
        create_button.setOnClickListener(ButtonClick(self.create_patient))
        create_button.setText('Create patient')
        vlayout.addView(create_button)
        self.add_error_text()

        self.add_return_button('main')

    def create_doctor_view(self):
        self.actual_view = 'create_doctor'
        self.vlayout.removeAllViews()

        self.doctor_name = EditText(self._activity)
        self.doctor_name.setHint('Doctor name')
        self.doctor_name.setInputType(0x00000001)
        self.vlayout.addView(self.doctor_name)

        self.doctor_especialization = EditText(self._activity)
        self.doctor_especialization.setHint('Doctor especialization')
        self.doctor_especialization.setInputType(0x00000001)
        self.vlayout.addView(self.doctor_especialization)

        create_button = Button(self._activity)
        create_button.setOnClickListener(ButtonClick(self.create_doctor))
        create_button.setText('Create doctor')
        self.vlayout.addView(create_button)
        self.add_error_text()

        self.add_return_button('main')

    def login(self):
        username = self.username_text.getText()
        password = self.password_text.getText()
        self.api.login(username, password,
                       self.success_login, self.error_login)
        self.error_text.setText('loading...')

    def modify_patient_view(self, patient):
        self.actual_view = 'modify_patient'
        self.vlayout.removeAllViews()

        self.patient_name = EditText(self._activity)
        self.patient_name.setHint('Patient name')
        self.patient_name.setInputType(0x00000001)
        self.patient_name.setText(patient['complete_name'])
        self.vlayout.addView(self.patient_name)

        self.patient_rg = EditText(self._activity)
        self.patient_rg.setHint('Patient RG')
        self.patient_rg.setInputType(0x00000002)
        self.patient_rg.setText(patient['rg'])
        self.vlayout.addView(self.patient_rg)

        self.birthdate_text = EditText(self._activity)
        self.birthdate_text.setHint('Patient birth date:')
        self.birthdate_text.setTextSize(20)
        self.birthdate_text.setText(patient['birth_date'])
        self.vlayout.addView(self.birthdate_text)

        self.patient_number1 = EditText(self._activity)
        self.patient_number1.setHint('Patient number 1')
        self.patient_number1.setInputType(0x00000002)
        self.patient_number1.setText(patient['number_for_contact1'])
        self.vlayout.addView(self.patient_number1)

        self.patient_number2 = EditText(self._activity)
        self.patient_number2.setHint('Patient number 2')
        self.patient_number2.setInputType(0x00000002)
        self.patient_number2.setText(patient['number_for_contact2'])
        self.vlayout.addView(self.patient_number2)

        self.patient_email = EditText(self._activity)
        self.patient_email.setHint('Patient email')
        self.patient_email.setInputType(0x00000020)
        self.patient_email.setText(patient['email'])
        self.vlayout.addView(self.patient_email)

        modify_button = Button(self._activity)
        modify_button.setOnClickListener(
            ButtonClick(self.modify_patient)
        )
        modify_button.setText('Modify patient')
        self.vlayout.addView(modify_button)

        self.add_return_button('details_patient', model=patient)

    def success_login(self, res):
        token = str(res.get('token'))
        self.api.setToken(token)
        self.defineEverything()
        self.main_view()

    def defineEverything(self):
        self.api.getPatients(
            listener=self.definePatients,
            listenerError=self.errorGet
        )
        self.api.getDoctors(
            listener=self.defineDoctors,
            listenerError=self.errorGet
        )
        self.api.getStates(
            listener=self.defineStates,
            listenerError=self.errorGet
        )
        self.api.getAppointments(
            listener=self.defineAppointments,
            listenerError=self.errorGet
        )

    def defineStates(self, res):
        self.statesItems = loads(res)

    def defineDoctors(self, res):
        self.doctorsItems = loads(res)

    def definePatients(self, res):
        self.patientsItems = loads(res)

    def defineAppointments(self, res):
        self.appointmentsItems = loads(res)

    def successGetDoctors(self, res):
        self.doctorsItems = loads(res)
        self.view_doctors()

    def successGetPatients(self, res):
        self.patientsItems = loads(res)
        self.view_patients()

    def successGetAppointments(self, res):
        self.appointmentsItems = loads(res)
        self.view_appointments()

    def getDoctorByName(self, name):
        for doctor in self.doctorsItems:
            if doctor['complete_name'] == name:
                return doctor

    def getPatientByName(self, name):
        for patient in self.patientsItems:
            if patient['complete_name'] == name:
                return patient

    def successCreatePatient(self, res):
        print('Patient created')
        self.error_text.setText('Patient created')
        self.main_view()

    def successCreateAppointment(self, res):
        print('Appointment created')
        self.error_text.setText('Appointment created')
        self.main_view()

    def successCreateDoctor(self, res):
        print('Doctor created')
        self.error_text.setText('Doctor created')
        self.main_view()

    def errorGet(self, err):
        print(err)

    def errorCreate(self, err):
        print(err)
        self.error_text.setText('something was wrong')

    def create_patient(self):
        patient = {}

        patient['complete_name'] = self.patient_name.getText()
        patient['rg'] = self.patient_rg.getText()

        birthdate = str(self.birthdateY.getValue(
        )) + '-' + str(self.birthdateM.getValue()) + '-' + str(self.birthdateD.getValue())
        patient['birth_date'] = birthdate
        patient['number_for_contact1'] = str(self.patient_number1.getText())
        patient['number_for_contact2'] = str(self.patient_number2.getText())
        patient['email'] = str(self.patient_email.getText())
        self.api.createPatient(
            patient=dictToJsonObject(patient),
            listener=self.successCreatePatient,
            listenerError=self.errorCreate
        )
        self.error_text.setText('processing...')

    def create_appointment(self):
        appointment = {}

        patientId = str(self.getPatientByName(
            self.patient_spinner.getSelectedItem()).get('id'))
        appointment['patient'] = patientId

        doctorId = str(self.getDoctorByName(
            self.doctor_spinner.getSelectedItem()).get('id'))
        appointment['doctor'] = doctorId

        appointment['state'] = str(self.state_spinner.getSelectedItem())

        datetime = str(self.appointmentDateY.getValue()) + '-' + str(
            self.appointmentDateM.getValue()) + '-' + str(self.appointmentDateD.getValue())
        datetime += 'T' + str(self.appointmentTimeH.getValue()) + \
            ':' + str(self.appointmentTimeM.getValue()) + ':00'
        appointment['date'] = datetime

        self.api.createAppointment(
            appointment=dictToJsonObject(appointment),
            listener=self.successCreateAppointment,
            listenerError=self.errorCreate
        )
        self.error_text.setText('processing...')

    def create_doctor(self):
        doctor = {}

        doctor['complete_name'] = str(self.doctor_name.getText())
        doctor['especialization'] = str(self.doctor_especialization.getText())

        self.api.createDoctor(
            doctor=dictToJsonObject(doctor),
            listener=self.successCreateDoctor,
            listenerError=self.errorCreate
        )

    def modify_patient(self):
        patient = {}

        patient['complete_name'] = self.patient_name.getText()
        patient['rg'] = self.patient_rg.getText()
        patient['birth_date'] = self.birthdate_text.getText()
        patient['number_for_contact1'] = str(self.patient_number1.getText())
        patient['number_for_contact2'] = str(self.patient_number2.getText())
        patient['email'] = str(self.patient_email.getText())
        patient['id'] = self.patient['id']

        self.patient = patient
        self.api.modifyPatient(
            patient=dictToJsonObject(patient),
            listener=self.successModifyPatient,
            listenerError=self.errorCreate
        )
        self.api.getPatients(
            listener=self.definePatients,
            listenerError=self.errorGet
        )

    def successModifyPatient(self, res):
        print(res)
        self.details_patient(patient=self.patient)

    def error_login(self, err):
        print(err)
        self.error_text.setText('something is wrong')

    def _dispatch_event(self, event=None, value=None):
        if event == 'details_patient':
            self.return_view('details_patient', value=value)
        elif event == 'details_appointment':
            self.return_view('details_appointment', value=value)

    def add_error_text(self, flayout=False):
        self.error_text = TextView(self._activity)
        if flayout:
            self.flayout.addView(self.error_text)
        else:
            self.vlayout.addView(self.error_text)

    def add_return_button(self, view, flayout=False, model=None):
        self.return_button = Button(self._activity)
        self.return_button.setOnClickListener(
            ButtonClick(self.return_view, view, value=model)
        )
        self.return_button.setText('Return')
        self.relative_rb = RelativeLayout(self._activity)
        self.relative_rb.addView(
            self.return_button, _create_layout_params('bottom'))
        if flayout:
            self.flayout.addView(self.relative_rb)
        else:
            self.vlayout.addView(self.relative_rb)

    def add_modify_button(self, model_type, model):
        self.modify_button = Button(self._activity)
        if model_type == 'patient':
            self.modify_button.setOnClickListener(
                ButtonClick(
                    self.return_view,
                    'modify_patient',
                    value=model
                )
            )
        self.modify_button.setText('Modify')
        self.relative_mb = RelativeLayout(self._activity)
        self.relative_mb.addView(
            self.modify_button, _create_layout_params('right')
        )
        self.vlayout.addView(self.relative_mb)

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
        elif view == 'modify_patient':
            self.modify_patient_view(patient=value)


def main():
    MainApp()
