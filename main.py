from config import user_token, comm_token, offset, line
import vk_api
import requests
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from database import *


class VkBot:
    def_init_(self)
        print('Bot was created')
        self.vk = vk_api.VkApi(token=comm_token) # Авторизация сообщества
        self.longpoll = VkLongPoll(self.vk) # Работа с сообщениями

    def write_msg(self, user_id, message)
        """"Метод для отправки сообщений"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def name(self, user_id):
        """Получение имени пользователя, который написал боту"""
        url = f'http://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids' : user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response ['response']
            for i in information_dict:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_sex(self, user_id):
        """Получение пола пользователя, меняет на противоположный"""
        url = f'http://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                if i.get('sex') == 2:
                    find_sex = 1
                    return find_sex
                elif i.get('sex') == 1:
                    find_sex = 2
                    return find_sex
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    def get_age_low(self, uer_id):
        """Получение возраста пользователя или нижней границы для поиска"""
        url = url = f'http://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.write_msg(user_id, 'Введите нижнюю границу возраста (min - 16):')
                for event in self.longoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')


    def get_age_high(self, user_id):
        """Получение возраста пользователя или верхней границы для поиска"""
        url = url = f'http://api.vk.com/method/user.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            for i in information_list:
                date = i.get('bdate')
            date_list = date.split('.')
            if len(date_list) == 3:
                year = int(date_list[2])
                year_now = int(datetime.date.today().year)
                return year_now - year
            elif len(date_list) == 2 or date not in information_list:
                self.wtite_msg(user_id, 'Введите верхнюю границу возраста (max - 65):')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена, введите токен в переменную - user_token')

    # @staticmethod
    def cities(self, user_id, city_name):
        """Получение ID города пользователя по названию"""
        url = url = f'http://api.vk.com/method/database.getCities'
        params = {'access_token': user_token,
                  'country_id': 1,
                  'q': f'{city_name}',
                  'need_all': 0,
                  'count': 1000,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_list = response['response']
            list_cities = information_list['items']
            for i in list_cities:
                found_city_name = i.get('title')
                if found_city_name == city_name:
                    found_city_id = i.get('id')
                    return int(found_city_id)
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_city(self, user_id):
        """Получение информации о городе пользователя"""
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'fields': 'city',
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        try:
            information_dict = response['response']
            for i in information_dict:
                if 'city' in i:
                    city = i.get('city')
                    id = str(city.get('id'))
                    return id
                elif 'city' not in i:
                    self.write_msg(user_id, 'Введите название вашего города:')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            city_name = event.text
                            id_city = self.cities(user_id, city_name)
                            if id_city != '' or id_city != None:
                                return str(id_city)
                            else:
                                break
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def find_user(self, user_id):
        """ Поиск человека по полученным данным"""
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': self.get_sex(user_id),
                  'age_from': self.get_age_low(user_id),
                  'age_to': self.get_age_hign(user_id),
                  'city': self.find_city(user_id),
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': 500}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for person_dict in list_1:
                if person_dict.get('is_closed') == False:
                    first_name = person_dict.get('first_name')
                    last_name = person_dict.get('last_name')
                    vk_id = str(person_dict.get('id'))
                    vk_link = 'vk.com/id' + str(person_dict.get('id'))
                    insert_data_users(first_name, last_name, vk_id, vk_link)
                elif:
                    continue
            return f'Поиск завершен'
        except KeyError:
            self.write_msg(user_id, 'Ошибка получения токена')

    def get_photos_id(self, user_id):
        """Получение ID фото с ранжирование в обратном порядке"""
        url = 'https://api.vk.com/method/potos.getAll'
        params = {'access_token': user_token,
                  'type': 'album',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 25,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        dict_photos = dict()
        resp_json = resp.json()
        try:
            dict_1 = resp_json['response']
            list_1 = dict_1['items']
            for i in list_1:
                photo_id = str(i.get('id'))
                i_likes = i.get('likes')
                if i_likes.get('count'):
                    likes = i_likes.get('count')
                    dict_photos[likes] = photo_id
            list_of_ids = sorted(dict_photos.items(), reverse=True)
            return list_of_ids
        except KeyError:
            self.writemsg(user_id, 'Ошибка получения токена')

    def get_photo_1(self, user_id):
        """Получение id фотографии № 1"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count ==1:
                return i[1]

    def ger_photo_2(self, user_id):
        """Получение id фотографии № 2"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count == 1
            if count == 2:
                return i [1]

    def get_photo_3(self, user_id):
        """Получение id фотографии № 3"""
        list = self.get_photos_id(user_id)
        count = 0
        for i in list:
            count += 1
            if count == 3:
                return i[1]

    def send_photo_1(self, user_id, message, offset):
        """Отправка 1 фотографии"""
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{self.person_id(offset)}_(self.get_photo_1(self.person_id(offset)))',
                                         'random_id': 0})

