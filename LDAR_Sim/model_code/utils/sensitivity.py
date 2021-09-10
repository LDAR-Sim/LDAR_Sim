import yaml


def yaml_to_dict(y_file):
    with open(y_file, "r") as f_content:
        try:
            return yaml.safe_load(f_content)
        except yaml.YAMLError as exc:
            print(exc)


def set_from_keylist(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value
