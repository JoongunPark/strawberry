# -*- coding: utf-8 -*-
import io
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from berryDB.models import Reservation
from django.core.serializers import serialize

__author__ = 'un'


def home(request):
    return render(request, "home.html")


def reserve(request):
    status = ''
    if request.method == 'POST':
        studentID = int(request.POST["studentID"])
        name = request.POST["name"]
        club = request.POST["club"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        numRolls = int(request.POST["numRolls"])
        numBerries = int(request.POST["numBerries"])
        date = request.POST["date"]
        reservation = Reservation(studentID=studentID, name=name,
                                  club=club, phoneNum=phone, password=password,
                                  numBerries=numBerries, numRolls=numRolls, date=date)
        status = 'success'
        reservation.save()

    return render(request, "reserve.html", {'status': status})


def compare(t1, t2):
	a = t1[0];
	b = t2[0];
	return cmp(a, b);


def printEx():
    reservations = Reservation.objects.all()

    l = []

    for reservation in reservations:
	    date = int(reservation.date.split(" ")[1][:-3])
	    t = (date, reservation.reserveID , reservation.name, reservation.studentID,
                reservation.numBerries, reservation.numRolls, reservation.phoneNum)
	    l.append(t)

    l.sort(compare)

    with io.open("static/yum.csv", 'w', encoding='utf8') as outfile:
        outfile.write(("날짜,예약 번호,예약자,학번,딸기 주문량,김밥 주문량,전화번호"+'\n').decode('utf-8'))
        for t in l:
                outfile.write((str(t[0]) + "," + str(t[1]) + ",").decode('utf-8'))
                outfile.write(t[2])
                outfile.write((","+str(t[3]) + "," + str(t[4]) + "," + str(t[5]) + "," + t[6] + "\n").decode('utf-8'))
    return






@login_required(login_url='/admin/')
def master(request):
    printEx()
    reservations = Reservation.objects.all()
    reservationID = request.GET.get('reservationID', None)
    if reservationID == None:
        pass
    else:
        reservation = Reservation.objects.all().filter(reserveID=reservationID)
        if len(reservation) != 0:
            reservation[0].delete()
            return HttpResponse("예약 취소에 성공하셨습니다.")

    return render(request, 'master.html', {'reservations': reservations})


def modify(request):
    reservations = []
    if request.method == 'POST':
        if request.POST["studentID"] != None:
            studentID = int(request.POST["studentID"])
            #password = request.POST["password"]
            reservations = Reservation.objects.all().filter(studentID=studentID)
    else:
        reservationID = request.GET.get('reservationID', None)
        password = request.GET.get('password', None)
        if reservationID == None or password == None:
            pass
        else:
            reservation = Reservation.objects.all().filter(reserveID=reservationID, password=password)
            if len(reservation) != 0:
                reservation[0].delete()
                return HttpResponse("예약 취소에 성공하셨습니다.")
            else:
                return HttpResponse("예약 취소에 실패하셨습니다. 비밀번호를 다시 입력하세요")

    return render(request, "modify.html", {'reservations': reservations})
