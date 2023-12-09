#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

avbl_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in avbl_objs.keys():
    obj = avbl_objs[obj_id]
    print(obj)

print("-- Create a new User --")
user_one = User()
user_one.first_name = "Betty"
user_one.last_name = "Bar"
user_one.email = "airbnb@mail.com"
user_one.password = "root"
user_one.save()
print(user_one)

print("-- Create a new User 2 --")
my_user_two = User()
my_user_two.first_name = "John"
my_user_two.email = "airbnb2@mail.com"
my_user_two.password = "root"
my_user_two.save()
print(my_user_two)
