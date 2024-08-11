def check_exp(list_var, exp):
    for i in exp:
        if i[0] == "v" and i not in list_var:
            return 1
    return 0

def jump_binary(index, lines, list_var, list_index, jumped_index):
    list_var_local = list_var[:]
    jumped_index_local = jumped_index[:]
    length = len(lines)
    while index < length:
        line = lines[index]
        head = line[0]
        if head == 'D':
            list_define = line.split()                                  #split define line
            var_name = list_define[2]
            if var_name not in list_var_local:
                list_var_local.append(var_name)
            index+=1
            continue
        
        if head == 'A':
            if index not in list_index: 
                list_assign = line.split()
                undeclared = check_exp(list_var_local, list_assign)
                if undeclared == 1:
                    list_index.append(index)
            index+=1
            continue
            
        if head == 'B':
            branch_line = line.split()
            jump_index = int(branch_line[1])
            if index not in list_index:
                undeclared = check_exp(list_var_local, branch_line)
                if undeclared == 1:
                    list_index.append(index)
            if jump_index not in jumped_index_local:
                jumped_index_local.append(jump_index)
                jump_binary(jump_index, lines, list_var_local, list_index, jumped_index_local)
            index+=1
            continue
            
        if head == 'R':
            remove_line = line.split()
            var_name = remove_line[1]                                   #generate variable name
            if var_name not in list_var_local:
                if index not in list_index:
                    list_index.append(index)
            else:
                list_var_local.remove(var_name)
            index+=1
            continue
            
            
        if head == 'O':
            if index not in list_index:
                list_output = line.split()
                var_name = list_output[1]                                   #generate variable name
                if var_name not in list_var_local:
                    list_index.append(index)
            index+=1
            continue 

if __name__ == "__main__":
    with open("./test7.pig", "r") as f:
        lines = f.readlines()
        list_var = []
        index = 0
        list_index = []                                                     #save visited 'may undeclared' line
        jumped_index = []
        while index < len(lines):
            line = lines[index]
            head_out = line[0]
            if head_out == 'D':
                list_define = line.split()                                  #split define line
                var_name = list_define[2]
                if var_name not in list_var:
                    list_var.append(var_name)
                index+=1
                continue
            
            if head_out == 'A':
                if index not in list_index:
                    list_assign = line.split()
                    expression = list_assign[1:]                                #select the expression into list
                    undeclared = check_exp(list_var, expression)
                    if undeclared == 1:
                        list_index.append(index)
                index+=1
                continue
                
            if head_out == 'B':
                branch_line = line.split()
                jump_index = int(branch_line[1])
                exp = branch_line[2:]
                if index not in list_index:
                    undeclared = check_exp(list_var, exp)
                    if undeclared == 1:
                        list_index.append(index)
                if jump_index not in jumped_index:
                    jumped_index.append(jump_index)
                    jump_binary(jump_index, lines, list_var, list_index, jumped_index)
                index+=1
                continue
                
            if head_out == 'R':
                remove_line = line.split()
                var_name = remove_line[1]                                   #generate variable name
                if var_name not in list_var:
                    if index not in list_index:
                        list_index.append(index)
                else:
                    list_var.remove(var_name)
                index+=1
                continue
                
                
            if head_out == 'O':
                list_output = line.split()
                var_name = list_output[1]                                   #generate variable name
                if var_name not in list_var:
                    if index not in list_index:
                        list_index.append(index)
                index+=1
                continue
            
        print(len(list_index))
                