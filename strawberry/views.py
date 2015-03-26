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
        studentID = request.POST["studentID"]
        name = request.POST["name"]
        club = request.POST["club"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        numRolls = request.POST["numRolls"]
        numBerries = request.POST["numBerries"]
        date = request.POST["date"]
        
        if (len(studentID) != 8) : status = u'학번을 다시 입력해 주세요'
        elif (len(password) != 4) : status = u'패스워드는 4자리 숫자입니다'
        elif (not str(password).isdigit()) : status = u'패스워드는 4자리 숫자입니다'
        elif (not numBerries.isdigit()) : status = u'딸기 수는 숫자로만 입력해 주세요'
        elif (not numRolls.isdigit()) : status = u'김밥 수는 숫자로만 입력해 주세요'
        elif (len(phone.split("-")) != 3) : status = u'전화번호 양식에 맞게 입력해주세요'
        else:
            reservation = Reservation(studentID=int(studentID), name=name,
                                      club=club, phoneNum=phone, password=password,
                                      numBerries=int(numBerries), numRolls=int(numRolls), date=date)
            status = 'success'
            reservation.save()
    return render(request, "reserve.html", {'status': status})


def compare(t1, t2):
	a = t1[0];
	b = t2[0];
	return cmp(a, b);


def printEx(num):
    reservations = Reservation.objects.all()

    l = []

    for reservation in reservations:
	    date = int(reservation.date.split("/")[1])
	    t = (date, reservation.reserveID , reservation.name, reservation.studentID, reservation.club,
                reservation.numBerries, reservation.numRolls, reservation.phoneNum, reservation.date)
	    l.append(t)

    l.sort(compare)

    with io.open("static/yum.csv", 'w', encoding='cp949') as outfile:
        outfile.write(("reservationID,name,studentID,club,strawBerry,GimBob,phone,date\n").decode('cp949'))
        for t in l:
            if num==t[0]:
                outfile.write((str(t[1]) + ",").decode('cp949'))
                outfile.write(t[2])
                outfile.write((","+str(t[3])+",").decode('cp949'))
                outfile.write(t[4])
                outfile.write(( "," + str(t[5]) + "," + str(t[6]) + ",").decode('cp949'))
                outfile.write(t[7]+","+t[8].split(",")[0])
               # outfile.write(("\n").decode('cp949')))
                outfile.write(("\n").decode('cp949'))
   # io.close()

    return






@login_required(login_url='/admin/')
def master(request, num):
    printEx(int(num))
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
