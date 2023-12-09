#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel

avbl_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in avbl_objs.keys():
    obj = avbl_objs[obj_id]
    print(obj)

print("-- Create a new object --")
main_model = BaseModel()
main_model.name = "My_First_Model"
main_model.my_number = 89
main_model.save()
print(main_model)
