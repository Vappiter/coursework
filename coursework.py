from datetime import date
import requests
from os import chdir
from pprint import pprint

class YaUploader:
    def __init__(self, ya_token: str):
        self.token = ya_token
        self.files_url_all = 'https://cloud-api.yandex.net/v1/disk/resources'

    def add_catalog(self, file_path: str):
    #   files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
      headers = self.get_header()
      res_files_link = requests.put(f'{self.files_url_all}?path={file_path}',headers=headers)
      var1 = res_files_link.status_code
      
    def get_header(self):
        return {
            'Content-type': 'application/json',
            'Authorization':'OAuth {}'.format(self.token)
        }
        
    def get_upload_link (self, file_path):
      upload_url = self.files_url_all + '/upload'
      headers = self.get_header()  
      self.add_catalog(file_path)
      file_path_file = file_path + 'file_test.txt'
      params = {'path':file_path_file, 'overwrite':'True'}  
      res_upload_link = requests.get(upload_url,headers=headers,params=params)
      pprint (res_upload_link.json())
      return res_upload_link.json()
        
    def upload(self, file_path: str):
    #   headers = self.get_header()
      href = self.get_upload_link(file_path=file_path).get("href","")
      response = requests.put(href,data=open('file_test.txt','rb'))
      pprint (response)
      """Метод загружает файлы по списку file_list на яндекс диск"""
          
    def get_files_list(self):
      files_url = self.files_url_all + '/files'
      headers = self.get_header()
      res_files_link = requests.get(files_url,headers=headers)
      return res_files_link.json()

class VK_test:
    def __init__(self, vk_token: str, vk_id_user = '1'):
        self.vk_token = vk_token
        self.vk_id_user = vk_id_user
        self.vk_url_all = 'https://api.vk.com/method/'
       
        
    def get_params(self):
        return {
            'user_id':self.vk_id_user,
            'access_token':self.vk_token, 
            'v':'5.131'
        }
    def get_all_photos(self):
        all_photos_url = self.vk_url_all + 'photos.getAll'
        params = self.get_params()
        params['extended'] = '1'
        res = requests.get(all_photos_url, params)
        return(res.json())
    
    def user_name(self):
        user_url = self.vk_url_all + 'users.get'
        params = self.get_params()
        res = requests.get(user_url, params)
        return(res.json())   
    
    def get_photos(self, count_photos = 5):
        all_photos_url = self.vk_url_all + 'photos.getAll'
        params = self.get_params()
        params['extended'] = '1'
        res = (requests.get(all_photos_url, params)).json()
        var1 = int(res['response']['count'])
        if count_photos > var1:
            pprint ('У пользователя нет столько фото')
        else:
            processing_photo(res, 1)    
        return(res)    
def processing_photo (res, application):
    result = []
    i1 = 0
    if application == 1:
     for var1, var2 in res.items():
         for var3, var4 in var2.items():
             if var3 == 'count':
                 i1 = var4
             else:
                for i2 in range (0,i1): 
                 for var5 in var4[i2].items():
                   if var5[0] == 'sizes':
                    for var6 in var5[1]:
                        
                      result.append(var6['height'])
                      result.append(var6['width'])  
                      pprint(result)
            #  pprint (var4)
     else:
        return


if __name__ == '__main__':
  chdir (r"Z:\2021-09-23_PYTHON\coursework")
  with open ('ya_token.txt', encoding='utf-8') as file_token:
       ya_token = file_token.read()
  with open ('vk_token.txt', encoding='utf-8') as file_token:
       vk_token = file_token.read()
#   ya_disk = YaUploader(ya_token)
#   path_to_file = str(date.today()) + '_Photo'
#   res1 = ya_disk.get_files_list()
#   pprint(res1)
  vk_photos = VK_test(vk_token,'643851064')
  photos = vk_photos.get_all_photos()
#   pprint(photos)
  user_name = vk_photos.user_name()
  pprint(user_name)
  vk_photos.get_photos(7)
    