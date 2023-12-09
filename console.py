#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    my_curled_brcs = re.search(r"\{(.*?)\}", arg)
    brakts = re.search(r"\[(.*?)\]", arg)
    if my_curled_brcs is None:
        if brakts is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brakts.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brakts.group())
            return retl
    else:
        lexer = split(arg[:my_curled_brcs.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(my_curled_brcs.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        check_match = re.search(r"\.", arg)
        if check_match is not None:
            arg_lent = [arg[:check_match.span()[0]], arg[check_match.span()[1]:]]
            check_match = re.search(r"\((.*?)\)", arg_lent[1])
            if check_match is not None:
                command = [arg_lent[1][:check_match.span()[0]], check_match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(arg_lent[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        arg_lent = parse(arg)
        obj_dic = storage.all()
        if len(arg_lent) == 0:
            print("** class name missing **")
        elif arg_lent[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_lent) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_lent[0], arg_lent[1]) not in obj_dic:
            print("** no instance found **")
        else:
            print(obj_dic["{}.{}".format(arg_lent[0], arg_lent[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_lent = parse(arg)
        obj_dic = storage.all()
        if len(arg_lent) == 0:
            print("** class name missing **")
        elif arg_lent[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_lent) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_lent[0], arg_lent[1]) not in obj_dic.keys():
            print("** no instance found **")
        else:
            del obj_dic["{}.{}".format(arg_lent[0], arg_lent[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_lent = parse(arg)
        if len(arg_lent) > 0 and arg_lent[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(arg_lent) > 0 and arg_lent[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(arg_lent) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arg_lent = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_lent[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_lent = parse(arg)
        obj_dic = storage.all()

        if len(arg_lent) == 0:
            print("** class name missing **")
            return False
        if arg_lent[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_lent) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_lent[0], arg_lent[1]) not in obj_dic.keys():
            print("** no instance found **")
            return False
        if len(arg_lent) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_lent) == 3:
            try:
                type(eval(arg_lent[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_lent) == 4:
            obj = obj_dic["{}.{}".format(arg_lent[0], arg_lent[1])]
            if arg_lent[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_lent[2]])
                obj.__dict__[arg_lent[2]] = valtype(arg_lent[3])
            else:
                obj.__dict__[arg_lent[2]] = arg_lent[3]
        elif type(eval(arg_lent[2])) == dict:
            obj = obj_dic["{}.{}".format(arg_lent[0], arg_lent[1])]
            for k, v in eval(arg_lent[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
