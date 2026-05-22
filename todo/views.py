from django.shortcuts import render, redirect
from .models import Task
from rest_framework.decorators import api_view

def task_list(request):

    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            Task.objects.create(title=title)

        return redirect('/')

    tasks = Task.objects.all()

    return render(request, 'todo/task_list.html', {
        'tasks': tasks
    })
def delete_task(request, task_id):

    task = Task.objects.get(id=task_id)

    task.delete()

    return redirect('/')
def complete_task(request, task_id):

    task = Task.objects.get(id=task_id)

    task.completed = True

    task.save()

    return redirect('/')
@api_view(['POST'])

def create_task(request):

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
from django.http import JsonResponse

@api_view(['GET'])
def task_api(request):

    tasks = Task.objects.all()

    data = []

    for task in tasks:
        data.append({
            'id': task.id,
            'title': task.title,
            'completed': task.completed
        })

    return JsonResponse(data, safe=False)
def edit_task(request, task_id):

    task = Task.objects.get(id=task_id)

    if request.method == 'POST':

        new_title = request.POST.get('title')

        if new_title:
            task.title = new_title
            task.save()

        return redirect('/')

    return render(request, 'todo/edit_task.html', {
        'task': task
    })