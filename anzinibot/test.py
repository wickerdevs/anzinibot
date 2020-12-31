from anzinibot.models.worker import TaskQueue

queue = TaskQueue(1)
messages = [1, 2, 3, 4, 5, 6]

def task(message:str):
    print(f'\nExecuted {message}')

for item in messages:
    print(f'\nAdded {item}')
    queue.add_task(task, item)

#queue.join()
print('DONE')