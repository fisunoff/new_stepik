from abc import ABC


class TagManager:
    tags = dict()

    def register(self, tag):
        self.tags[tag.name] = tag

    def get_tags(self):
        return self.tags


class Tag(ABC):
    name = NotImplementedError
    description = NotImplementedError
    is_list = False

    def __init__(self, **context):
        self.context = context

    def get_data(self):
        raise NotImplementedError

    def __str__(self):
        return f'{self.name} - {self.description}'

    @classmethod
    def get_name(cls):
        return cls.name

    @classmethod
    def get_description(cls):
        return cls.description


class ProfileTag(Tag, ABC):
    def __init__(self, **context):
        super().__init__(**context)
        self.profile = context['request'].user.profile


class ProfileFIOTag(ProfileTag):
    name = 'ПрофильФИО'
    description = 'Фамилия, имя, отчество текущего пользователя'

    def get_data(self):
        return str(self.profile)


manager = TagManager()
manager.register(ProfileFIOTag)
