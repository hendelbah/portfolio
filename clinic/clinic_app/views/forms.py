"""
Module contains form classes for posting data on app's web pages.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SearchField, \
    SelectField, IntegerField, TextAreaField, TelField, DateField, TimeField

from wtforms.validators import InputRequired, Email, Length, EqualTo, Optional, NumberRange, Regexp


class CustomEmail(Email):
    """Extended email validator that in addition allows using 'root' as email."""

    def __call__(self, form, field):
        if not field.data == 'root':
            super().__call__(form, field)


pass_length = Length(min=6, max=40)
full_name = Regexp(r'^\w{2,}( \w{2,}){1,2}$')


class LoginForm(FlaskForm):
    """Form for logging users in"""
    email = StringField('Email:', validators=[CustomEmail()])
    pwd = PasswordField('Password:', validators=[InputRequired(), pass_length])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Log in')


class ChangePassForm(FlaskForm):
    """Form for changing user's password"""
    password = PasswordField('Current password:', validators=[InputRequired(), pass_length])
    new_pass = PasswordField('New password:', validators=[
        InputRequired(),
        EqualTo('confirm', message='Passwords must match'),
        pass_length])
    confirm = PasswordField('Confirm password:')
    submit = SubmitField('Submit change')


class FilterUsers(FlaskForm):
    """Form for filtering users"""
    search_email = SearchField('Search by email:', validators=[Optional(), Length(max=80)],
                               filters=[lambda x: x or None])
    submit = SubmitField('Filter')


class EditUser(FlaskForm):
    """Form for updating and creating users"""
    email = StringField('Email:', validators=[CustomEmail(), InputRequired(), Length(max=80)])
    is_admin = BooleanField('Is admin:', default=False)
    doctor_uuid = SelectField(
        'Attached doctor\'s account:',
        validators=[Optional()],
        filters=[lambda x: x or None])
    submit = SubmitField('Save changes')


class FilterDoctors(FlaskForm):
    """Form for filtering doctors"""
    search_name = SearchField('Search by full name:', validators=[Optional(), Length(max=127)],
                              filters=[lambda x: x or None])
    submit = SubmitField('Filter')


class EditDoctor(FlaskForm):
    """Form for updating and creating doctors"""
    full_name = StringField('Full name:', validators=[InputRequired(), Length(max=127), full_name])
    experience_years = IntegerField('Years of experience:',
                                    validators=[InputRequired(), NumberRange(min=0)])
    speciality = TextAreaField('Speciality:',
                               validators=[InputRequired(), Length(max=255)])
    info = TextAreaField('Info:',
                         validators=[InputRequired(), Length(max=1023)])
    submit = SubmitField('Save changes')


class FilterPatients(FlaskForm):
    """Form for filtering patients"""
    search_phone = SearchField('Search by phone number: ', validators=[Optional(), Length(max=20)],
                               filters=[lambda x: x or None])
    search_name = SearchField('Search by full name:', validators=[Optional(), Length(max=127)],
                              filters=[lambda x: x or None])
    submit = SubmitField('Filter')


class EditPatient(FlaskForm):
    """Form for updating and creating patients"""
    phone_number = TelField('Phone number:', validators=[InputRequired(), Length(max=20)])
    full_name = StringField('Full name:', validators=[InputRequired(), Length(max=127), full_name])
    birthday = DateField('Date of birth:', validators=[InputRequired()])
    submit = SubmitField('Save changes')


class FilterAppointments(FlaskForm):
    """Form for filtering appointments"""
    doctor_name = SearchField('Search by doctor\'s name:', validators=[Optional(), Length(max=127)],
                              filters=[lambda x: x or None])
    patient_name = SearchField('Search by patient\'s name:',
                               validators=[Optional(), Length(max=127)],
                               filters=[lambda x: x or None])
    date = DateField('Filter by date:', validators=[Optional()])
    submit = SubmitField('Filter')


class EditAppointment(FlaskForm):
    """Form for updating and creating appointments"""
    date = DateField('Date:', validators=[InputRequired()])
    time = TimeField('Time:', validators=[InputRequired()])
    conclusion = TextAreaField('Conclusion:', validators=[Optional(), Length(max=511)])
    prescription = TextAreaField('Prescription:', validators=[Optional(), Length(max=511)])
    bill = IntegerField('Bill:', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save changes')


class FillAppointment(FlaskForm):
    """Form for filling out appointment info"""
    conclusion = TextAreaField('Conclusion:', validators=[Optional(), Length(max=511)])
    prescription = TextAreaField('Prescription:', validators=[Optional(), Length(max=511)])
    bill = IntegerField('Bill:', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save changes')
