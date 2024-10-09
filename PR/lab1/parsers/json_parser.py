# python -m parsers.json_parser

from util.indenter import getWI
from util.file_system import read_json

def encode_to_json(root, indentation_size=4):
    def encode(node, indent=0):
        json_str = ""
        if isinstance(node, dict):
            json_str += getWI("{", indent)
            
            for key, value in node.items():
                json_str += getWI(f'"{key}": ', indent + indentation_size)

                if isinstance(value, (dict, list)):
                    json_str += encode(value, indent + indentation_size)
                else:
                    json_str += encode(value)
                json_str += ","
            
            if json_str.endswith(","):
                json_str = json_str[:-1]

            json_str += getWI("}", indent)
            return json_str
        
        elif isinstance(node, list):
            json_str += getWI("[", indent)
            
            for child_node in node:
                json_str += encode(child_node, indent + indentation_size) + ","
            
            if json_str.endswith(","):
                json_str = json_str[:-1]
                
            json_str += getWI("]", indent)
            return json_str
        
        else:
            return f'"{node}"'
    return encode(root)
    
if __name__ == "__main__":
    data = dict(read_json("resources/data.json"))
    res = encode_to_json(data)
    print(res)