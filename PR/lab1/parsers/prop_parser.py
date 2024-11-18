# python -m parsers.prop_parser

from util.file_system import read_json
import re

def encode_to_prop(root):
    def encode(node, path=""):
        if isinstance(node, dict):
            prop_str = ""
            for key, value in node.items():
                prop_str += encode(value, f"{path}.{key}" if path else key)
            return prop_str
        
        elif isinstance(node, list):
            prop_str = ""
            for i, child_node in enumerate(node):
                prop_str += encode(child_node, f"{path}[{i}]")
            return prop_str
        
        else:
            return f'{path}="{node}"\n'
    
    return encode(root)

def is_int(value):
    if isinstance(value, int):
        return True
    return isinstance(value, str) and value.isdigit()

def decode_from_prop(prop_string):
    def nested_set(dic, keys, value):
        for key in keys[:-1]:
            if is_int(key):
                key = int(key)
            if isinstance(dic, dict):
                dic = dic.setdefault(key, {})
            else:
                while len(dic) <= key:
                    dic.append({})
                dic = dic[key]

        last_key = keys[-1]
        if is_int(last_key):
            last_key = int(last_key)
        if isinstance(dic, dict):
            dic[last_key] = value
        else:
            while len(dic) <= last_key:
                dic.append(None)
            dic[last_key] = value

    def convert_lists(item):
        if isinstance(item, dict):
            if all(is_int(key) for key in item.keys()):
                max_index = max(int(key) if isinstance(key, str) else key for key in item.keys())
                return [convert_lists(item.get(i) or item.get(str(i))) for i in range(max_index + 1)]
            return {k: convert_lists(v) for k, v in item.items()}
        return item

    result = {}
    for line in prop_string.strip().split('\n'):
        key, value = line.split('=', 1)
        value = value.strip('"')
        keys = [int(k) if is_int(k) else k for k in re.findall(r'\w+|\d+', key)]
        nested_set(result, keys, value)

    return convert_lists(result)

if __name__ == "__main__":
    # Encode
    data = read_json("resources/data.json")
    encoded = encode_to_prop(data)
    dec = decode_from_prop(encoded)
    encoded = encode_to_prop(dec)
    print("Encoded:")
    print(encoded)
    print(dec)
