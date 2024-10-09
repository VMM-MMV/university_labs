from file_system import read_json

def getWI(text, indent, new_line=True):
    indented_text = indent * " " + text
    if new_line:
        return "\n" + indented_text
    else:
        return indented_text

def encode(node, indent=4, indent_level=4):
    json_str = ""
    if isinstance(node, dict):
        json_str += getWI("{", indent - indent_level)
        
        for key, value in node.items():
            json_str += getWI(f'"{key}": ', indent)
            json_str += encode(value, indent) + ","
        
        json_str = json_str[:len(json_str)-1]
        json_str += getWI("}", indent - indent_level)
        return json_str
    
    elif isinstance(node, list):
        json_str += getWI("[", indent - indent_level, False)
        
        for child_node in node:
            json_str += encode(child_node, indent + indent_level) + ","
        
        json_str = json_str[:len(json_str)-1]
        json_str += getWI("]", indent - indent_level)
        return json_str
    
    else:
        return getWI(f'"{node}"', indent, False)

if __name__ == "__main__":
    data = dict(read_json("data.json"))
    res = encode(data)
    print(res)