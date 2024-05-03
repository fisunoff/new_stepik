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
        self.profile = context['profile']


class CourseTag(Tag, ABC):
    def __init__(self, **context):
        super().__init__(**context)
        self.course = context['course']


class ProfileFIOTag(ProfileTag):
    name = 'ПрофильФИО'
    description = 'Фамилия, имя, отчество текущего пользователя'

    def get_data(self):
        return str(self.profile)


class ProfileNameTag(ProfileTag):
    name = 'ИмяСерт'
    description = 'Имя получателя сертификата'

    def get_data(self):
        return str(self.profile.name)


class ProfileSurnameTag(ProfileTag):
    name = 'ФамСерт'
    description = 'Фамилия получателя сертификата'

    def get_data(self):
        return str(self.profile.surname)


class CourseNameTag(CourseTag):
    name = 'ИмяКурса'
    description = 'Наименование курса'

    def get_data(self):
        return str(self.course.name)


class CompanyNameTag(Tag):
    name = 'ИмяКомп'
    description = 'Наименование компании'

    def get_data(self):
        return 'ООО @Рога и копыта'


class CertNumberTag(Tag):
    name = 'НомСерт'
    description = 'Номер сертификата'

    def __init__(self, **context):
        super().__init__(**context)
        self.cert_id = context['id']

    def get_data(self):
        return str(self.cert_id)


manager = TagManager()
manager.register(ProfileFIOTag)
manager.register(ProfileNameTag)
manager.register(ProfileSurnameTag)
manager.register(CourseNameTag)
manager.register(CompanyNameTag)
manager.register(CertNumberTag)
