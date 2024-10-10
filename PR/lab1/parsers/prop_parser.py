# python -m parsers.prop_parser

from util.file_system import read_json
from typing import Union, Dict, List
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


if __name__ == "__main__":
    # Encode
    data = read_json("resources/data.json")
    encoded = encode_to_prop(data)
    print("Encoded:")
    print(encoded)