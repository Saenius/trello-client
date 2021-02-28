import sys
import requests

#ввдите свои ключ и токен, чтоб проверить код
auth_params = {
    'key': "#",
    'token': "#",}

#введите свой айди в переменную board_id
base_url = "https://api.trello.com/1/{}"
board_id = "#"
board = requests.get(base_url.format('boards') + '/' + board_id, params = auth_params).json()
idBoard = board['id']

column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params = auth_params).json()
for column in column_data:
    task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params = auth_params).json()
    column_name = column['name'] + ' ' + str(len(task_data))
    print(column_name)

def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params = auth_params).json()

    for column in column_data:
        print(column['name'])
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params = auth_params).json()
        if not task_data:
            print('\t' + 'No tasks')
            continue
        for task in task_data:
            print('\t' + task['name'] + ' (id = ' + task['id'] + ')')




def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params = auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})

            break

def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params = auth_params).json()

    list_task = []
    dict_task = {}
    count = 1
    task_id = None

    for column in column_data:
        column_tasks = requests.get(base_url.format('lists')+ '/' + column['id'] + '/cards',params = auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                dict_task[key] = task_id
                list_task.append('Задача: {} | Колонка: {} | номер: {}'.format(task['name'], column['name'], count))
                count += 1
    if len(list_task) > 1:
        for i in list_task:
            print(i)
        id_input = input('Выберите id задачи: ')
        task_id = dict_task[int(id_input)]
    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break

#здесь тоже укажите свой ключ и айди
def create_column(column_name):
    base_url = "https://api.trello.com/1/{}"
    query = {
        'key': "#",
        'token': "#",
        'idBoard': idBoard,
        'name': f'{column_name}'
    }

    response = requests.request(
        "POST",
        base_url.format('lists'),
        params = query
    )
    print('колонка создана')
    

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
