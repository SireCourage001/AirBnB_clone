#!/usr/bin/python3
from models.base_model import BaseModel

main_model = BaseModel()
main_model.name = "My First Model"
main_model.my_number = 89
print(main_model)
main_model.save()
print(main_model)
my_model_json = main_model.to_dict()
print(my_model_json)
print("JSON of main_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))
