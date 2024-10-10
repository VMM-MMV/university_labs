# python -m parsers.prop_parser

from util.indenter import getWI
from util.file_system import read_json

def encode_to_prop(root):
    def encode(node, path=""):
        if isinstance(node, dict):
            prep_str = ""
            for key, value in node.items():
                prep_str += encode(value, f"{path}.{key}" if path else key)
            return prep_str

        elif isinstance(node, list):
            prep_str = ""
            for i, child_node in enumerate(node):
                prep_str += encode(child_node, f"{path}[{i}]")
            return prep_str
            
        else:
            return f'{path}="{node}"\n'
    
    return encode(root)

if __name__ == "__main__":
    data = read_json("resources/data.json")
    res = encode_to_prop(data)
    print(res)