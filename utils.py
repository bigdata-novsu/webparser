from bs4 import Comment
import os

# dump string or list to file
def dump_to_file(file_name, value):
    file_name = "log/" + file_name
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    file = open(file_name, "w", encoding="utf-8")
    if isinstance(value, list) or isinstance(value, map):
        file.write('\n'.join(value))
    else:
        file.write(str(value))
    file.close()

# convert tags to dictionary
def tags_to_dict(tags):
    dict = {}
    for it in tags:
        l = dict.get(it.name, None)
        if (l == None):
            l = list()
            dict[it.name] = l
        l.append(str(it.string))
    return dict

