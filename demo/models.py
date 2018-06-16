from django.db import models

# Create your models here.


class Student(models.Model):
    """
        学生表
    """
    student_id = models.BigAutoField(primary_key=True)  # 学号
    student_name = models.CharField(max_length=128)   # 学生姓名
    student_age = models.IntegerField(null=True, blank=True)  # 学生年龄
    student_sex = models.CharField(max_length=128)  # 学生性别
    student_card = models.CharField(max_length=128)  # 身份证号

    def __str__(self):
        return "%s ---- %s ----- %s" %(self.student_id, self.student_name,self.student_sex)

    class Meta:
        db_table = "student"


class Teacher(models.Model):
    """
        老师表
    """
    teacher_id = models.BigAutoField(primary_key=True)  # ID
    teacher_name = models.CharField(max_length=128)   # 姓名
    teacher_sex = models.CharField(max_length=128)  # 性别

    def __str__(self):
        return "%s ---- %s ----- %s" %(self.teacher_id, self.teacher_name,self.teacher_sex)

    class Meta:
        db_table = "teacher"
