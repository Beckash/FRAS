from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

datetime_object = datetime.now()


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


# Overriding the Default Django Auth User and adding One More Field (user_type)
class Users(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Instructor"), (3, "Student"), (4, "DepartmentHead"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class ICT_Professional(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Users, on_delete=models.CASCADE)
    profile_pic = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class BatchInfo(models.Model):
    id = models.AutoField(primary_key=True)
    batch_name = models.IntegerField(default=2018)
    section = models.CharField(max_length=2, default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# def __str__(self):


#     return self.course_name

class Colleges(models.Model):
    id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):


#     return self.course_name


class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=30)
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE, default=1)
    # staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    subject_code = models.CharField(max_length=30)
    subject_name = models.CharField(max_length=30)
    semester = models.CharField(max_length=10)
    curicullem = models.CharField(max_length=10)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, default=1)
    batch = models.IntegerField(default=2018)
    # staff_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Users, on_delete=models.CASCADE)
    address = models.TextField()
    profile_pic = models.FileField(null=True)
    college_id = models.ForeignKey(Colleges, on_delete=models.DO_NOTHING, default=1)
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Assign Instructor
class AssignInstructor(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.IntegerField(default=2018)
    section = models.CharField(max_length=4)
    subject_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, default=1)
    class_type = models.CharField(max_length=20, default='lecture_class')
    staff_id = models.ForeignKey(Instructor, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Department Head Table
class DepartmentHead(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Users, on_delete=models.CASCADE)
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE, default=1)
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Students Table
class Students(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(unique=True, max_length=60, null=True)
    admin = models.OneToOneField(Users, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6)
    profile_pic = models.FileField()
    address = models.TextField()
    batch = models.IntegerField(default=2018)
    college_id = models.ForeignKey(Colleges, on_delete=models.DO_NOTHING, default=1)
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Attendance Weight Table
class AttendanceWeight(models.Model):
    id = models.AutoField(primary_key=True)
    batch = models.IntegerField(default=2018)
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    subject_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    lab_class = models.IntegerField()
    lecturer_class = models.IntegerField()
    objects = models.Manager()


# Student Status Table
class StudentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, default='normal')
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Registering Students for Each Courses Table
class RegisterForCourse(models.Model):
    id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    subject_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default=1)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING, default=1)
    section = models.CharField(max_length=4, default='A')
    curicullem = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
    batch = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Attendance Table
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, default=1)
    subject_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default=1)
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    section = models.CharField(max_length=4, default='A')
    batch = models.CharField(max_length=10, default='2018')
    attendance_type = models.CharField(max_length=50, default='lecture')
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Individual Student Attendance Report Table
class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING, default=1)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING, default=1)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=1)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, default=1)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    receiver = models.ForeignKey(Users, on_delete=models.DO_NOTHING, default=1)
    staff_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=Users)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            ICT_Professional.objects.create(admin=instance)
        if instance.user_type == 2:
            Instructor.objects.create(admin=instance)
        # if instance.user_type == 3:
        #     Students.objects.create(admin=instance, batch_id=BatchInfo.objects.get(id=1),
        #                             session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="",
        #                             gender="")
        if instance.user_type == 3:
            Students.objects.create(admin=instance, department_id=Departments.objects.get(id=1),
                                    session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="",
                                    gender="")
        if instance.user_type == 4:
            DepartmentHead.objects.create(admin=instance)


@receiver(post_save, sender=Users)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.ict_professional.save()
    if instance.user_type == 2:
        instance.instructor.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.departmenthead.save()


# Face Recognition Models
# def path_model_name(instance, filename):
#     path = 'media/models/' + str(instance.id) + '/' + filename
#     return path


class MLModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    model_weight = models.FileField(upload_to='Model/')
    batchSize = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=10)
    epochs = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=10)
    progress = models.FloatField(default=0)
    number_of_classes = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=10)


def path_file_name(instance, filename):
    path = 'ImageDataset/' + str(instance.dataset.student_id.student_id) + '/' + filename
    return path


class Dataset(models.Model):
    # id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)


class DatasetItem(models.Model):
    # id = models.AutoField(primary_key=True)
    path_to_dir = models.CharField(max_length=200, default='Datasets/')
    image = models.FileField(upload_to=path_file_name)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)


class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(Departments, on_delete=models.DO_NOTHING, default=1)
    section = models.CharField(max_length=4, default='A')
    batch = models.CharField(max_length=10, default='2020')
    ip_address = models.CharField(max_length=30)
    direction = models.CharField(max_length=30)
