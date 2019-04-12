from django.shortcuts import render, HttpResponse, redirect

from crm.models import UserInfo

from django.http import JsonResponse
from rbac.service.initial import initial_sesson
from django.views import View
from django.contrib import auth
import datetime
from crm.models import Book, Room
import json


def login(request):
    if request.method == "GET":
        return render(request, "login.html")

    else:
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        response = {"user": None, "msg": ""}
        user = auth.authenticate(username=user, password=pwd)

        if user:
            auth.login(request, user)
            response["user"] = user.username
            initial_sesson(user, request)
        else:
            response["msg"] = "用户名或者密码错误!"

        return JsonResponse(response)


def logout(request):
    request.session.flush()
    return redirect("/login/")


def home(request):
    return render(request, "home.html")


class RoomBookView(View):

    def get(self, request, *args, **kwargs):

        current_date = datetime.datetime.now().date()
        book_date = request.GET.get("book_date", current_date)
        time_choices = Book.time_choices
        room_list = Room.objects.all()
        books = list(Book.objects.filter(date=book_date).values("room_id", "time_id", "user__name"))
        books = json.dumps(books)
        print("request.user", request.user)

        return render(request, 'room_book.html', locals())

    def post(self, request, *args, **kwargs):
        print(request.POST)
        response = {'status': True, 'msg': None, 'data': None}
        try:
            choice_date = request.POST.get('choose_date')
            post_data = json.loads(request.POST.get('post_data'))

            # 增加预定
            book_obj_list = []
            for room_id, time_list in post_data['ADD'].items():
                for time_id in time_list:
                    obj = Book(room_id=room_id, time_id=time_id, user_id=request.user.pk, date=choice_date)
                    book_obj_list.append(obj)
            Book.objects.bulk_create(book_obj_list)

            # 删除会议室预定信息
            print(post_data['DEL'])
            from django.db.models import Q
            remove_booking = Q()
            for room_id, time_id_list in post_data['DEL'].items():
                for time_id in time_id_list:
                    temp = Q()
                    temp.connector = 'AND'
                    temp.children.append(('user_id', request.user.pk,))
                    temp.children.append(('date', choice_date))
                    temp.children.append(('room_id', room_id,))
                    temp.children.append(('time_id', time_id,))
                    remove_booking.add(temp, 'OR')

            if remove_booking:
                Book.objects.filter(remove_booking).delete()

        except Exception as e:

            response['status'] = False
            response['msg'] = str(e)

        return JsonResponse(response)
