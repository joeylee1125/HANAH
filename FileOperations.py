# -*- coding: UTF-8 -*-
import csv
import os
import shutil
from docx import Document


class MyFolder:
    def __init__(self, folder_name):
        self.name = folder_name

    def create(self):
        if not os.path.exists(self.name):
            os.makedirs(self.name)

    def move(self):
        pass

    def copy(self):
        pass

class MyFile:
    def __init__(self, file_name):
        self.name = file_name
        
    def create(self):
        with open(self.name, 'w') as f:
            f.close()
    
    def delete(self):
        os.remove(self.name)
        
    def move(self, dst):
        shutil.move(self.name, dst)
        
    def copy(self, dst):
        shutil.copy(self.name, dst)
        
    def read(self):
        pass
        
    def write(self, content):
        pass

    def append(self):
        pass

class MyTextFile(MyFile):
    def __init__(self, file_name):
        super().__init__(file_name)

    def read(self):
        try:
            with open(self.name, 'r') as f:
                self.content = f.read()
        except Exception as e:
            print(e)

    def write(self, content):
        try:
            with open(self.name, "w") as f:
                f.write(content)
        except Exception as e:
            print(e)

class MyCsvFile(MyFile):
    def __init__(self, file_name):
        super().__init__(file_name)

    def read_dict(self):
        with open(self.name, encoding='utf-8_sig') as csvfile:
            reader = csv.DictReader(csvfile)
            data_dict = dict.fromkeys(reader.fieldnames)
            for key in data_dict:
                data_dict[key] = []
            for row in reader:
                for key in data_dict:
                    data_dict[key].append(row[key])
        self.content = data_dict
        return self.content

    def write(self, content):
        with open(self.name, 'w', newline='', encoding='utf-8_sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(content.keys())
            writer.writerows(zip(*content.values()))

    def write_dict(self, fields, content):
        with open(self.name, 'w', newline='', encoding='utf-8_sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for row in content:
                writer.writerow(row)

class MyDocFile(MyFile):
    def __init__(self, file_name):
        super().__init__(file_name)

    def read(self):
        try:
            document = Document(self.name)
            l = [paragraph.text for paragraph in document.paragraphs]
            self.content = ''.join(str(e) for e in l)
            print(self.content)
            return self.content
        except Exception as e:
            print(e)
            print("Document %s is invalid" % self.name)