from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from .timetable import *

def main(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = everytimeSubmit(request.POST)
        # check whether it's valid:
        if form.is_valid():
            id_ = form.data['everytime_id']
            pw_ = form.data['everytime_pw']
            return login(request,id_,pw_)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = everytimeSubmit()

    return render(request, 'gonggang/main.html', {'form': form})

def login(request,username,password):
    rtn = []
    #get timetables
    friends = friends_list(username, password)
    table = []
    for i in range(len(friends)):
        t= table2array(get_timetable(username,password,friends[i][0]))
        table.append(t)

    #지금 공강인 친구찾기
    from datetime import date
    now = time.gmtime(time.time())
    d,h,m = date.today().weekday(),now.tm_hour, now.tm_min
    now = [(h+9,m),d]
    l = len(table)
    for i in range(l):
        name = friends[i][1]
        if(isavailable(table[i],now)):
            rtn.append(name)

    return render(request, 'gonggang/result.html', {'valids':rtn})
