from file_system import read_json

def getWI(text, indent, new_line=True):
    indented_text = indent * " " + text
    if new_line:
        return "\n" + indented_text
    else:
        return indented_text

def encode_to_xml(root, iteration_name="item"):
    def encode(node, indent=4, indent_level=4):
        json_str = ""
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, (list, dict)):
                    json_str += getWI(f'<{key}>', indent)
                    json_str += encode(value, indent + indent_level)
                    json_str += getWI(f'</{key}>', indent)
                else:
                    json_str += getWI(f'<{key}>{value}</{key}>', indent)
                
            return json_str
        
        elif isinstance(node, list):
            
            for child_node in node:
                json_str += getWI(f'<{iteration_name}>', indent)
                json_str += encode(child_node, indent + indent_level)
                json_str += getWI(f'</{iteration_name}>', indent)
            
            return json_str
        
        else:
            return f"{node}"
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<root>
    {encode(root)}
</root>"""

if __name__ == "__main__":
    data = dict(read_json("data.json"))
    res = encode_to_xml(data)
    print(res)