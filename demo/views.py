from django.shortcuts import render,HttpResponse

# Create your views here.
from demo import models
import json
from django.forms.models import model_to_dict   # 对象转换成字典


def login(request):
    return render(request, "base.html")


def hello_world(request):
    """
        Hello,World!
    """
    return HttpResponse("Hello,World!")


def get_student(request):
    """
        获取一个学生
    :param request:
    :return:
    """
    students = models.Student.objects.filter(student_id=request.GET["student_id"])
    json_dict = {}
    for student in students:
        student_dict = model_to_dict(student, fields=["student_id", "student_name", "student_age"])
        json_dict[student.student_id] = student_dict
    return HttpResponse(json.dumps(json_dict), content_type="application/json")

