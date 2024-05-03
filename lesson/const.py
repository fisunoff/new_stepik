NEW = 'новый'
IN_PROGRESS = 'на проверке'
DONE = 'оценен'

statuses = ((NEW, NEW),
            (IN_PROGRESS, IN_PROGRESS),
            (DONE, DONE),
)


TEXT = 'текст'
RADIO = 'Одиночный выбор'

task_types = (
    (TEXT, TEXT),
    (RADIO, RADIO),
)