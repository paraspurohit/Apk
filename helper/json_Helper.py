import json

from constants.file import  DOCTOR_DETAIL_FILE_PATH


class JsonHelper():

    async def add(self,new_data, user, FILE_Path):
        with open(FILE_Path, 'r+') as file:
            file_data = json.load(file)
            file_data[user].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
        return
    
    def write_json(self,data, filename= DOCTOR_DETAIL_FILE_PATH):
        with open (filename, "w") as file:
            json.dump(data, file, indent=4)
    
    def read(self,path):
        with open(path, 'r') as file:
          data = json.load(file)  
        return data