from datetime import date
import requests
import os
from pprint import pprint
from tqdm import tqdm


class YaUploader:
    def __init__(self, ya_token: str):
        self.token = ya_token
        self.files_url_all = 'https://cloud-api.yandex.net/v1/disk/resources'

    def add_catalog(self, file_path: str):
        #   files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_header()
        return requests.put(f'{self.files_url_all}?path={file_path}', headers=headers)
        #  res_files_link.status_code

    def get_header(self):
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

    def upload(self, file_path: str, file_name):
        #   headers = self.get_header()
        href = self.get_upload_link(file_path=file_path).get("href", "")
        response = requests.put(href, data=open(file_name, 'rb'))
        pprint(response)
        """Метод загружает файлы по списку file_list на яндекс диск"""

    def get_files_list(self):
        files_url = self.files_url_all + '/files'
        headers = self.get_header()
        res_files_link = requests.get(files_url, headers=headers)
        return res_files_link.json()

    def save_file_vk(self, file_path, res):
        self.add_catalog(file_path)
        upload_url = self.files_url_all + '/upload/'
        headers = self.get_header()
        for var1 in tqdm(res):
            test1 = str(var1['likes']) + '.jpg'
            file_path_file = file_path + '/' + test1
            params = {'path': file_path_file,'url':var1['url'], 'overwrite': 'True'}
            response = requests.post(upload_url, headers=headers, params=params)
 
class VK_test:
    def __init__(self, vk_token: str, vk_id_user='1'):
        self.vk_token = vk_token
        self.vk_id_user = vk_id_user
        self.vk_url_all = 'https://api.vk.com/method/'

    def get_params(self):
        return {
            'access_token': self.vk_token,
            'owner_id': self.vk_id_user,
            # 'user_id':self.vk_id_user,
            'v': '5.131'
        }
    # def get_all_photos(self):
    #     all_photos_url = self.vk_url_all + 'photos.getAll'
    #     params = self.get_params()
    #     # params['extended'] = '1'
    #     res = requests.get(all_photos_url, params)
    #     return(res.json())

    def user_name(self):
        
        ''' Возвращает по id Имя и Фамилию пользователя'''
        
        user_url = self.vk_url_all + 'users.get'
        params = self.get_params()
        params['user_id'] = self.vk_id_user
        res = requests.get(user_url, params)
        return(res.json())

    def get_photos(self, count_photos=5):
        
        '''Возвращает подготовленный массив фотографий для сохранения на диск'''
        
        all_photos_url = self.vk_url_all + 'photos.getAll'
        params = self.get_params()
        params['extended'] = '1'
        res = (requests.get(all_photos_url, params)).json()
        var1 = res['response']['count']
        if count_photos > var1:
            pprint('У пользователя нет столько фото')
        else:
            return(processing_photo(res, 1, count_photos))


def processing_photo(res, application, count_photos):
    
    '''Обрабатывает весь массив полученных фото согласно условий'''
    
    result = [{'height': 0, 'width': 0, 'url': '', 'likes': 0}
              for i in range(0, count_photos)]
    if application == 1:
        for var1 in res['response']['items']:
            photo_info = {'height': 0, 'width': 0, 'url': ''}
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
    else:
        return

def enter_socnet():
    
  ''' А планировалась только как функция ввода данных, а по факту получается еще и обработки ??? '''
   
  print('\n \n Программа позволяет делать backup файлов фотографий из различных соцсетей на различные диски\n')
  count_attempt = 5
  var_socnet_input = ''
  while var_socnet_input != 'Q' and count_attempt > 0:
    var_socnet_input = input ('Выберите социальную сеть\n\
    V - Вконтакте\n\
    O - Одноклассники\n\
    I - Инстаграмм\n\
    Q - Выход из программы\n').upper()
    count_attempt -= 1 
    if var_socnet_input == 'V':
     with open('vk_token.txt', encoding='utf-8') as file_token:
      vk_token = file_token.read()   
     var_vk_number = input (f'\n Введите id пользователя у которого Вы хотите сохранить фотографии: \n\
     (по умолчанию id = 1 - Павел Дуров) \n') 
     if var_vk_number == '':
      var_vk_number = 1
     var_vk_photos_count  = input (f'\n Введите количество фотографий, которые необходимо сохранить: \n\
     (по умолчанию будет сохраняться 5 фотографий) \n')
     if var_vk_photos_count == '':
      var_vk_photos_count = 5   
     vk_photos = VK_test(vk_token, var_vk_number)
     return vk_photos.get_photos(var_vk_photos_count)
    elif var_socnet_input == 'O':
      pass
    elif var_socnet_input == 'I':
      pass
    elif var_socnet_input == 'Q':
      return None  
    elif count_attempt == 1:
      print('Извините нажата неизвестная клавиша\n\
      осталась последняя попытка.  :(')
    elif count_attempt == 0:   
      print('До свидания!!!')
      return None    
    else:
      print(f'Извините нажата неизвестная клавиша\n\
      Осталось {count_attempt} попыток! ;)')     
      
def enter_disk(array_ptohos):
    
  ''' Выбор диска для сохранения '''
   
  print('\n \n Данные для сохранения на диск подготовлены, осталось выбрать диск\n')
  count_attempt = 5
  var_socnet_input = ''
  while var_socnet_input != 'Q' and count_attempt > 0:
    var_socnet_input = input ('Выберите диск\n\
    Y - ЯндексДиск\n\
    G - GoogleDrive\n\
    M - OneDrive\n\
    Q - Выход из программы\n').upper()
    count_attempt -= 1 
    if var_socnet_input == 'Y':
     with open('ya_token.txt', encoding='utf-8') as file_token:
        ya_token = file_token.read()  
        ya_disk = YaUploader(ya_token)
        path_to_file = str(date.today()) + '_Photo'
    # res1 = ya_disk.get_files_list()
        ya_disk.save_file_vk(path_to_file, array_ptohos)
     return None   
    elif var_socnet_input == 'G':
      pass
    elif var_socnet_input == 'M':
      pass
    elif var_socnet_input == 'Q':
      return None  
    elif count_attempt == 1:
      print('Извините нажата неизвестная клавиша\n\
      осталась последняя попытка.  :(')
    elif count_attempt == 0:   
      print('До свидания!!!')
      return None    
    else:
      print(f'Извините нажата неизвестная клавиша\n\
      Осталось {count_attempt} попыток! ;)')       

if __name__ == '__main__':
    
    ''' Общая функция '''
    
    file_path = (os.path.split(__file__)) # Считывает текущую директорию скрипта, тут же должны храниться файлы токенов
    os.chdir(file_path [0]) # Устанавливает директорию
    array_ptohos = enter_socnet() 
    if array_ptohos != None:
     enter_disk(array_ptohos)   
    #   with open('ya_token.txt', encoding='utf-8') as file_token:
    #     ya_token = file_token.read()  
    #     ya_disk = YaUploader(ya_token)
    #     path_to_file = str(date.today()) + '_Photo'
    # # res1 = ya_disk.get_files_list()
    #     ya_disk.save_file_vk(path_to_file, array_ptohos)



    # os.chdir(r"Z:\2021-09-23_PYTHON\coursework")
    # with open('ya_token.txt', encoding='utf-8') as file_token:
    #     ya_token = file_token.read()
    # with open('vk_token.txt', encoding='utf-8') as file_token:
    #     vk_token = file_token.read()
    # ya_disk = YaUploader(ya_token)
    # path_to_file = str(date.today()) + '_Photo'
    # res1 = ya_disk.get_files_list()
    # #   pprint(res1)
    # vk_photos = VK_test(vk_token, '10668318')
    # # photos_vk = vk_photos.get_all_photos()
    # #   pprint(photos_vk)
    # # user_name = vk_photos.user_name()
    # # pprint(user_name) 
    # ya_disk.save_file_vk(path_to_file, vk_photos.get_photos())
