from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import main.tasks as tasks


@login_required
def run_task(request, task_name=None):
    task = getattr(tasks, task_name, None)
    if not tasks or not hasattr(task, 'delay'):
        raise Exception(f'Task {task_name} not defined')
    task.delay()
    return HttpResponse(f'Enqueued task {task_name}')
