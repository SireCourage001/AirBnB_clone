#!/usr/bin/python3
from models.base_model import BaseModel

main_model_one = BaseModel()
main_model_one.name = "My_First_Model"
main_model_one.my_number = 89
print(main_model_one.id)
print(main_model_one)
print(type(main_model_one.created_at))
print("--")
my_model_json = main_model_one.to_dict()
print(my_model_json)
print("JSON of main_model_one:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

print("--")
new_model = BaseModel(**my_model_json)
print(new_model.id)
print(new_model)
print(type(new_model.created_at))

print("--")
print(main_model_one is new_model)
