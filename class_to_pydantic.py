import re

from attr import attributes

indent = ' '*4

def open_file(filename):
    with open(filename, "r") as file:
        data = file.read()
    return data

def save_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)

def proces_declaration(line):
    right_side = False

    asssignment = line.split("=")
    if len(asssignment) == 2:
        right_side = asssignment[1].strip()
    if len(asssignment) > 2:
        raise Exception("Wtf is this line: {line}")
    line = asssignment[0]

    line = line.split(":")
    if len(line) == 1:
        atr, atr_type = line[0], "Any"
    else:
        atr, atr_type = line
    atr =  atr.strip()
    atr_type = atr_type.strip()

    if right_side:
        atr_type = f"Optional[{atr_type}]" 
        return f"{atr}: {atr_type} = {right_side}"
    else:
        return f"{atr}: {atr_type}"

def switch_form(data):
    data_lines = data.splitlines()

    new_lines = []
    in_init = False
    in_init_def = False
    in_valid_class = False
    last_line = ''

    for i, line in enumerate(data_lines):
        local_indent = len(re.match(r"(\s*).*",line).group(1))

        if not line.strip():
            if new_lines and not new_lines[-1].strip():
                continue
            new_lines.append(line)
            continue

        if in_init_def:
            if match := re.match(r"\s*\):", line):
                in_init = in_init_def
                in_init_def = False
                continue
            else:
                atributes = line.split(",")
                if len(atributes) == 2:
                    if 'self' in line:
                        continue
                    new_lines.append(indent + proces_declaration(line.strip().rstrip(',')))
                    continue
                for atr in atributes:
                    if 'self' not in atr and atr:
                        new_lines.append(indent + proces_declaration(atr.strip()))
            
                continue

        # if in_init_def:
        #     if match := re.match(r"\s*\):", line):
        #         in_init = in_init_def
        #         in_init_def = False
        #         continue
        #     else:
        #         if 'self' in line:
        #             continue

            
        #         new_lines.append(indent + proces_declaration(line.strip().rstrip(',')))
        #         continue

        if in_init and local_indent > in_init:
            continue
        else:
            in_init = False

        if match := re.match(r"class .*\((.*)\):*.", line):
            if match.group(1) in ["RepresentableMixin","ProtocolObject"]:
                line = re.sub(r"RepresentableMixin", "BaseModel, RepresentableMixin",line)
                line = re.sub(r"ProtocolObject", "BaseModel, ProtocolObject",line)
                in_valid_class = True
            else:
                in_valid_class = False

        if not in_valid_class:
            new_lines.append(line)
            continue

        if match := re.match(r"(\s*)def __init__\((.*)\):", line):
            in_init = len(match.group(1))
            # print(f"Matched simple init with indent {in_init}")
            atributes = match.group(2).split(',')
            for atr in atributes:
                if 'self' not in atr:
                    print(i)
                    new_lines.append(indent + proces_declaration(atr.strip()))
            continue

        if match := re.match(r"(\s*)def __init__\($", line):
            in_init_def = len(match.group(1))
            # print(f"Matched multiline init with indent {in_init_def}")
            continue

        new_lines.append(line)



    return new_lines

def main():
    data = open_file("c_t_p_content.py")
    #print(data)
    new_data = switch_form(data)
    to_save = "\n".join(new_data)
    #print(to_save)
    data = save_file("c_t_p_content_new.py", to_save)


if __name__ == "__main__":
    main()