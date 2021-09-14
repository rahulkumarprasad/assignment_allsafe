from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .tasks import get_website_title,get_services_of_allsafe,get_all_links
from celery.result import AsyncResult
from allsafe_website_info.celery import app

def preform_tasks(tasks):
    tasks_ids={}
    for i in tasks:
        i=int(i)
        if i == 1:
            task_name="Title"
            task_obj=get_website_title.delay()
        elif i==2:
            task_name="Services"
            task_obj=get_services_of_allsafe.delay()
        elif i==3:
            task_name="Links"
            task_obj=get_all_links.delay()
        tasks_ids[task_name]=task_obj.task_id
    return tasks_ids

def home(request):
    if request.method=="POST":
        tasks=request.POST.getlist("tasks")
        if len(tasks) > 0:
            task_id=preform_tasks(tasks)
            data={"task id":task_id}
            return JsonResponse(data,safe=False)
        else:
            return HttpResponse("Please Select tasks to preform")
    return render(request,"html/index.html",{"active":"home"})


def result(request):
    if request.method=="POST":
        id=request.POST.get("task_id",None)
        if id!=None:
            res=AsyncResult(id,app=app)
            data={"active":"result","status":res.status,"result":res.result}
            return render(request,"html/result.html",data)

    return render(request,"html/result.html",{"active":"result"})