# python -m parsers.xml_parser

from util.file_system import read_json
from util.indenter import getWI

def encode_to_xml(root, indentation_size=4, iteration_name="item"):
    def encode(node, indent=4):
        xml_str = ""
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, (list, dict)):
                    xml_str += getWI(f'<{key}>', indent)
                    xml_str += encode(value, indent + indentation_size)
                    xml_str += getWI(f'</{key}>', indent)
                else:
                    xml_str += getWI(f'<{key}>{value}</{key}>', indent)
                
            return xml_str
        
        elif isinstance(node, list):
            
            for child_node in node:
                xml_str += getWI(f'<{iteration_name}>', indent)
                xml_str += encode(child_node, indent + indentation_size)
                xml_str += getWI(f'</{iteration_name}>', indent)
            
            return xml_str
        
        else:
            return f"{node}"
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<root>{encode(root)}
</root>"""

if __name__ == "__main__":
    data = dict(read_json("resources/data.json"))
    res = encode_to_xml(data)
    print(res)