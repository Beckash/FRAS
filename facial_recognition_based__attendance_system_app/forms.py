from django import forms
from django.forms import Form
from .models import MLModel, Users, Students, BatchInfo, SessionYearModel, Colleges, \
    Departments
from .FacialRecognition.mainOrginal import MainClass
from django.core.validators import MaxValueValidator, MinValueValidator
from .FacialRecognition.mainOrginal import MainClass



class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    id = forms.CharField(label="Student ID", max_length=60,
                         widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Batches
    # try:
    #     courses = Courses.objects.all()
    #     course_list = []
    #     for course in courses:
    #         single_course = (course.id, course.course_name)
    #         course_list.append(single_course)
    # except:
    #     course_list = []

    try:
        batchinfos = BatchInfo.objects.all()
        print(batchinfos)
        batch_list = []
        batch_name_list = []
        for batch in batchinfos:
            if batch.batch_name not in batch_name_list:
                single_batch = (batch.batch_name, batch.batch_name)
                batch_list.append(single_batch)
                batch_name_list.append(batch.batch_name)
    except:
        batch_list = []

    try:
        colleges = Colleges.objects.all()
        college_list = []
        for college in colleges:
            single_college = (college.id, college.college_name)
            college_list.append(single_college)
    except:
        college_list = []
    try:
        departments = Departments.objects.all()
        department_list = []
        for department in departments:
            single_department = (department.id, department.department_name)
            department_list.append(single_department)
    except:
        department_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
                session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    # gender_list = (
    #       ('Male', 'Male'),
    #      ('Female', 'Female')
    # )
    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    # course_id = forms.ChoiceField(label="Course", choices=course_list,
    #                               widget=forms.Select(attrs={"class": "form-control"}))
    batch_id = forms.ChoiceField(label="Batch", choices=batch_list,
                                 widget=forms.Select(attrs={"class": "form-control"}))
    college_id = forms.ChoiceField(label="College", choices=college_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))

    department_id = forms.ChoiceField(label="Department", choices=department_list,
                                      widget=forms.Select(attrs={"class": "form-control"}))

    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))

    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    id = forms.CharField(label="Student ID", max_length=60,
                         widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    # try:
    #     courses = Courses.objects.all()
    #     course_list = []
    #     for course in courses:
    #         single_course = (course.id, course.course_name)
    #         course_list.append(single_course)
    # except:
    #     course_list = []

    # For Displaying Colleges
    try:
        colleges = Colleges.objects.all()
        college_list = []
        for college in colleges:
            single_college = (college.id, college.college_name)
            college_list.append(single_college)
    except:
        college_list = []

        # For Displaying Batches
    try:
        batchinfos = BatchInfo.objects.all()
        batch_list = []
        batch_name_list = []
        for batch in batchinfos:
            if batch.batch_name not in batch_name_list:
                single_batch = (batch.batch_name, batch.batch_name)
                batch_list.append(single_batch)
                batch_name_list.append(batch.batch_name)

    except:
        batch_list = []

        # For Displaying Departments
    try:
        departments = Departments.objects.all()
        department_list = []
        for department in departments:
            single_department = (department.id, department.department_name)
            department_list.append(single_department)
    except:
        department_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
                session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))

    # course_id = forms.ChoiceField(label="course", choices=course_list,
    #                               widget=forms.Select(attrs={"class": "form-control"}))
    college_id = forms.ChoiceField(label="College", choices=college_list,
                                   widget=forms.Select(attrs={"class": "form-control"}))
    department_id = forms.ChoiceField(label="Department", choices=department_list,
                                      widget=forms.Select(attrs={"class": "form-control"}))
    batch_id = forms.ChoiceField(label="Batch", choices=batch_list,
                                 widget=forms.Select(attrs={"class": "form-control"}))

    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


#
# class AutoForm(forms.Form):
#     TYPE_CHOICES = [('', '-- choose a type --'), ] + [(t.type, t.type) for t in Colleges.objects.all()]
#     DEPARTMENT_CHOICES = [(d.id, d.department_name) for d in Departments.objects.all()]
#     DEPARTMENT_CHOICES.insert(0, ('', '-- choose a vehicle type first --'))
#
#     type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'onchange': 'get_departments();'}))
#     department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)




class TestForm(forms.Form):
    image = forms.ImageField(label='Test Image', required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    model_weight = forms.FileField(label="Model Weight New", required=False,
                                   widget=forms.FileInput(attrs={"class": "form-control"}))
    # For Displaying Model Weights
    try:
        models = MLModel.objects.all()
        model_weights = []
        for model in models:
            single_model_weights = (
                model.id, model.model_weight)
            model_weights.append(single_model_weights)
    except:
        model_weights = []
    model_weight_list = forms.ChoiceField(label="Model Weight Uploaded", required=False, choices=model_weights,
                                          widget=forms.Select(attrs={"class": "form-control"}))


classes_samples = MainClass.get_number_of_class_samples()


class MLForm(forms.Form):
    model_name = forms.CharField(label="Model Name", max_length=50, required=False,

                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    epoch = forms.IntegerField(label="Epoch",
                               validators=[MinValueValidator(1), MaxValueValidator(100)],
                               widget=forms.NumberInput(attrs={"class": "form-control"}))

    batchSize = forms.IntegerField(label="Batch Size", label_suffix=': It should less than ' + str(classes_samples[1]),
                                   validators=[MinValueValidator(1), MaxValueValidator(100)],
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    number_of_classes = forms.IntegerField(label="Number of Classes", initial='' + str(classes_samples[0]),
                                           disabled=True,
                                           widget=forms.NumberInput(attrs={"class": "form-control"}))

    model_weight = forms.FileField(label="Model Weight New", required=False,
                                   widget=forms.FileInput(attrs={"class": "form-control"}))


class EditMLForm(forms.Form):
    model_name = forms.CharField(label="Model Name", required=False,

                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    epoch = forms.IntegerField(label="Epoch",
                               validators=[MinValueValidator(1), MaxValueValidator(100)],
                               widget=forms.NumberInput(attrs={"class": "form-control"}))

    batchSize = forms.IntegerField(label="Batch Size", label_suffix=': It should less than ' + str(classes_samples[1]),
                                   validators=[MinValueValidator(1), MaxValueValidator(100)],
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))

    number_of_classes = forms.IntegerField(label="Number of Classes", initial='' + str(classes_samples[0]),
                                           disabled=True,
                                           widget=forms.NumberInput(attrs={"class": "form-control"}))




class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# ✅ Create the form using the custom widget
class UploadImageForm(forms.Form):
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=True
    )

