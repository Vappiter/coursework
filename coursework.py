from datetime import date
import time
import requests
import os
import json
from pprint import pprint
from tqdm import tqdm


class YaUploader:
    def __init__(self, ya_token: str):
        self.token = ya_token
        self.files_url_all = 'https://cloud-api.yandex.net/v1/disk/resources'

    def add_catalog(self, file_path: str): # Метод создания каталога на Яндекс Диске
      headers = self.get_header() 
      res1=requests.get(f'{self.files_url_all}?path={file_path}', headers=headers)
      if res1.status_code == 200:
        print (f'Каталог уже существует')
      else:  
        return requests.put(f'{self.files_url_all}?path={file_path}', headers=headers)
        
    def info_catalog(self, file_path: str): # Метод получения информации о имеющихся файлах в каталоге
      headers = self.get_header()
      return requests.get(f'{self.files_url_all}?path={file_path}', headers=headers).json()
     
    def get_header(self): # Общий заголовок запросов к Яндекс Диску
        return {
            'Content-type': 'application/json',
            'Accept':'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, file_path):
        upload_url = self.files_url_all + '/upload'
        headers = self.get_header()
        self.add_catalog(file_path)
        file_path_file = file_path + 'file_test.txt'
        params = {'path': file_path_file, 'overwrite': 'True'}
        res_upload_link = requests.get(
            upload_url, headers=headers, params=params)
        pprint(res_upload_link.json())
        return res_upload_link.json()

    # def upload(self, file_path: str, file_name): # Метод загружает файлы по списку file_list на яндекс диск"""
    #   href = self.get_upload_link(file_path=file_path).get("href", "")
    #   response = requests.put(href, data=open(file_name, 'rb'))
    #   pprint(response)
                

    # def get_files_list(self):
    #     files_url = self.files_url_all + '/files'
    #     headers = self.get_header()
    #     res_files_link = requests.get(files_url, headers=headers)
    #     return res_files_link.json()

    def save_file_vk(self, file_path, res):
        self.add_catalog(file_path)
        upload_url = self.files_url_all + '/upload/'
        headers = self.get_header()
        var2 = -1
        for var1 in tqdm(res):
            if var2 != var1['likes']:
             test1 = str(var1['likes']) + '.jpg'
             var2 = var1['likes']
            else:
              time1 = int(time.time())
              test1 = str(var1['likes']) + '_' + str(time1) + '.jpg'
              var2 = var1['likes']
            file_path_file = file_path + '/' + test1
            params = {'path': file_path_file,'url':var1['url'], 'overwrite': 'True'}
            requests.post(upload_url, headers=headers, params=params)
 
class VK_test:
    def __init__(self, vk_token: str):# Был ещё параметр vk_id_user='1', но если мы добавляем ещё и ФИО, он становиться не нужным
      
      ''' Определение. Не забыть что нужно во все методы добавить vk_id_user, так как можно ещё и ФИО вводить'''
      
      self.vk_token = vk_token
      self.vk_id_user = 1 # Было self.vk_id_user = vk_id_user
      self.vk_url_all = 'https://api.vk.com/method/'

    def get_params(self):
        return {
            'access_token': self.vk_token,
            # 'owner_id': self.vk_id_user,
            'v': '5.131'
        }
    
    def user_name(self): # Возвращает по id Имя и Фамилию пользователя. Нигде не используется, так может потом пригодится
      user_url = self.vk_url_all + 'users.get'
      params = self.get_params()
      params['user_id'] = self.vk_id_user
      res = requests.get(user_url, params)
      return(res.json())
    
    def find_user_id(self, user_name):# Возвращает список пользователей с введеными именем и фамилией
      
      ''' По введеному имени и фамилии возвращает user_id'''
      
      i = 1
      result_id_user = [{'id': 0} for i in range(0, 5)]
      user_url = self.vk_url_all + 'users.search'
      params = self.get_params()
      params['q'] = user_name
      params['count'] = '5'
      res = requests.get(user_url, params).json()
      for var1 in res['response']['items']:
        # for i in range (0, 5):
          last_name = var1['last_name'] # Что-то напрямую f строка не берет ????
          first_name = var1['first_name'] # Что-то напрямую f строка не берет ????
          id_user =  var1['id'] # Что-то напрямую f строка не берет ????
          result_id_user[i-1] = var1['id']
          print(f'\n {i}. Имя пользователя: {last_name} {first_name}, id пользователя {id_user}')
          i += 1
      i = int(input ('Введите номер пользователя, фотографии которого будем сохранять:' ))  
      self.vk_id_user = result_id_user[i-1] 
      return

    def get_photos_all(self, count_photos=5):
        
      '''Возвращает подготовленный массив фотографий для сохранения на диск'''
        
      all_photos_url = self.vk_url_all + 'photos.getAll'
      params = self.get_params()
      params['extended'] = '1'
      params['count'] = 200      
      res = (requests.get(all_photos_url, params)).json()
      var1 = res['response']['count']
      if count_photos > var1:
        pprint('У пользователя нет столько фото')
      else:
          return(self.processing_photo(res, count_photos))

    def get_photos_album(self, count_photos=5, id_album=0): # Разобраться, почему без определения по умолчанию не берет id_album
        
      '''Возвращает подготовленный массив фотографий для сохранения на диск из выбраного альбома'''
        
      all_photos_url = self.vk_url_all + 'photos.get'
      params = self.get_params()
      params['extended'] = '1'
      params['album_id'] = id_album
      params['owner_id'] = self.vk_id_user
      res = (requests.get(all_photos_url, params)).json()
      return self.processing_photo(res, count_photos)

    def get_album_user(self):
      
      ''' Возвращает массив альбомов пользователя, без wall and profile. Хочется понять почему? '''
      
      album_url = self.vk_url_all + 'photos.getAlbums'
      params = self.get_params()
      params['owner_id'] = self.vk_id_user
      res = (requests.get(album_url, params)).json()
      if res ['response']['count'] == 0:
       return 0
      else:
       return self.processing_album(res)

    def processing_album(self, res):
    
      '''Обрабатываются имеющиеся альбомы пользователя'''
    
      count_albums = res ['response']['count']
      result_album = [{'id': 0, 'title': '', 'count_photos': 0} for i in range(0, count_albums)]
      i = 0
      for var1 in res['response']['items']:
        album_info = {'id': 0, 'title': '', 'count_photos': 0} 
        album_info['id'] = var1['id']
        album_info['title'] = var1['title']
        album_info['count_photos'] = var1['size']
        result_album[i] = album_info
        i += 1
      return result_album
  

    def processing_photo(self, res, count_photos):
    
      '''Обрабатывает весь массив полученных фото согласно условий'''
    
      result = [{'height':0, 'width':0, 'url':'', 'likes':-1} for i in range(0, count_photos)]
      for var1 in res['response']['items']:
        photo_info = {'height':0, 'width':0, 'url':''}
        for i1 in range(0, count_photos):
          if var1['likes']['count'] > result[i1]['likes']:
           photo_info['likes'] = var1['likes']['count']
           for var2 in var1['sizes']:
             if photo_info['height'] < var2['height'] and photo_info['width'] < var2['width']:
              photo_info['height'] = var2['height']
              photo_info['width'] = var2['width']
              photo_info['url'] = var2['url']
           result[i1] = photo_info
           break
      return result
 
    def choice_album (self, user_album):
  
      ''' Выбор альбома из которого будем сохранять фотографии '''
  
      len_users_album = len(user_album)
      for i in range (0, len_users_album):
        title_album = user_album[i]['title'] # Что-то напрямую f строка не берет ????
        count_photos = user_album [i]['count_photos'] # Что-то напрямую f строка не берет ????
        print(f'\n {i+1}. Название альбома: {title_album}, с нём содержиться {count_photos}')
      i = int(input ('Введите номер альбома откуда будем сохранять фотографии:' ))
      return user_album [i-1]['id']

def processing_input_vk():
  
  ''' Обработка ввода для Вконтакте'''
  
  var_vk_photos_count = 0
  with open('vk_token.txt', encoding='utf-8') as file_token:
    vk_token = file_token.read()   
  # Новое, определение id по ФИО
  vk_photos = VK_test(vk_token)
  var_vk_input = input(f'\n Введите id пользователя или его имя и фамилию у которого Вы хотите сохранить фотографии: \n\
  (по умолчанию id = 1 - Павел Дуров) \n') 
  if var_vk_input == '':
    var_vk_input = 1
  elif var_vk_input.isdigit() != True:
    var_vk_input = vk_photos.find_user_id(var_vk_input)
  else:
    vk_photos.vk_id_user = var_vk_input  
  
  #   var_vk_number = input(f'\n Введите id пользователя у которого Вы хотите сохранить фотографии: \n\
  #   (по умолчанию id = 1 - Павел Дуров) \n') 
  # if var_vk_number == '':
  #  var_vk_number = 1
  var_vk_photos_count  = int(input (f'\n Введите количество фотографий, которые необходимо сохранить: \n\
  (по умолчанию будет сохраняться 5 фотографий) \n'))
  if var_vk_photos_count == '':
    var_vk_photos_count = 5   
  # vk_photos = VK_test(vk_token) # Было  vk_photos = VK_test(vk_token, var_vk_number) Теперь раньше создаем экземпляр
  user_album = vk_photos.get_album_user()
  if user_album == 0:
    print (f'У пользователя нет альбомов, только фото на стене и в профайле \n\
  Будем выбирать лучшие фотографии оттуда :)')
    return vk_photos.get_photos_all(var_vk_photos_count)
  else:
    id_album = vk_photos.choice_album(user_album)
    return vk_photos.get_photos_album(var_vk_photos_count, id_album) 

def enter_socnet():
    
  ''' А планировалась только как функция ввода данных, а по факту получается еще и обработки ??? '''
   
  print('\n \n Программа позволяет делать backup файлов фотографий из различных соцсетей на различные диски\n')
  count_attempt = 5
  var_socnet_input = ''
  while var_socnet_input != 'Q' and count_attempt > 0:
    var_socnet_input = input ('Выберите социальную сеть\n\
    V - Вконтакте\n\
    O - Одноклассники (в разработке)\n\
    I - Инстаграмм (в разработке)\n\
    Q - Выход из программы\n').upper()
    count_attempt -= 1 
    if var_socnet_input == 'V':
     return processing_input_vk()
    elif var_socnet_input == 'O':
      return 'Q'
    elif var_socnet_input == 'I':
      return 'Q'
    elif var_socnet_input == 'Q':
      return 'Q'  
    elif count_attempt == 1:
      print('Извините нажата неизвестная клавиша\n\
      осталась последняя попытка.  :(')
    elif count_attempt == 0:   
      print('До свидания!!!')
      return 'Q'    
    else:
      print(f'Извините нажата неизвестная клавиша\n\
      Осталось {count_attempt} попыток! ;)')     
      
def enter_disk(array_ptohos):
    
  ''' Выбор диска для сохранения '''
   
  print('\n \n Данные для сохранения на диск подготовлены, осталось выбрать диск\n')
  count_attempt = 5
  var_disk_input = ''
  while var_disk_input != 'Q' and count_attempt > 0:
    var_disk_input = input ('Выберите диск\n\
    Y - ЯндексДиск\n\
    G - GoogleDrive (в разработке)\n\
    M - OneDrive (в разработке)\n\
    Q - Выход из программы\n').upper()
    count_attempt -= 1 
    if var_disk_input == 'Y':
     with open('ya_token.txt', encoding='utf-8') as file_token:
        ya_token = file_token.read()  
     ya_disk = YaUploader(ya_token)
     path_to_file = str(date.today()) + '_Photo'
     ya_disk.save_file_vk(path_to_file, array_ptohos)
     print (f'\n Фотографии сохранены. Необходимо подготовить выходной файл\n\
     \n НАЖМИТЕ КЛАВИШУ "ENTER"\n')
     input()
     time.sleep(3) # Без этого не корректно отрабатывают следующие функции, не успевает обновить информацию
     return preparftion_exit_file(ya_disk.info_catalog(path_to_file))
    elif var_disk_input == 'G':
      return 'Q'
    elif var_disk_input == 'M':
      return 'Q'
    elif var_disk_input == 'Q':
      return 'Q' 
    elif count_attempt == 1:
      print('Извините нажата неизвестная клавиша\n\
      осталась последняя попытка.  :(')
    elif count_attempt == 0:   
      print('До свидания!!!')
      return 'Q'    
    else:
      print(f'Извините нажата неизвестная клавиша\n\
      Осталось {count_attempt} попыток! ;)')   
      
def preparftion_exit_file(info_cat):
  count_photos_cat = info_cat ['_embedded']['total']
  result_exit_file = [{'file_name': '', 'size': 0, } for i in range(0, count_photos_cat)]
  i = 0
  for var1 in info_cat['_embedded']['items']:
    file_info = {'file_name': 0, 'size': ''} 
    file_info['file_name'] = var1['name']
    file_info['size'] = var1['size']
    result_exit_file[i] = file_info
    i += 1
  with open('info_cat.txt', 'w') as file_wr: 
    json.dump (result_exit_file, file_wr)
  
      

if __name__ == '__main__':
    
    ''' Общая функция '''
    
    file_path = (os.path.split(__file__)) # Считывает текущую директорию скрипта, тут же должны храниться файлы токенов
    os.chdir(file_path [0]) # Устанавливает директорию
    var_quit = ''
    while var_quit != 'Q': 
      array_photos = enter_socnet() 
      if array_photos == 'Q':
       quit()
      else:
        answer = enter_disk(array_photos)
      if answer == 'Q':
       quit()
      else:  
       print(f'Фотографии сохранены.\n') 
      var_quit = input (f'\n Закончить работать - нажмите клавишу "q", для продолжения любую другую \n').upper()     

