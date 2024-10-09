def getWI(text, indent, new_line=True):
    """Get with indentation"""
    
    indented_text = indent * " " + text
    if new_line:
        return "\n" + indented_text
    else:
        return indented_text