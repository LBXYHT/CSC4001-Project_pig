def add_binary_str(string1, string2):
    num1 = int(string1, 2)
    num2 = int(string2, 2)
    
    length = max(len(string1), len(string2))
    
    sum = num1 + num2
    bin_sum = bin(sum)[2:]
    if len(bin_sum) > length:
        bin_sum = bin_sum[1:]
    else:
        bin_sum = (length-len(bin_sum)) * "0" + bin_sum
    return bin_sum

def sub_binary_str(string1, string2):
    num1 = int(string1, 2)
    num2 = int(string2, 2)
    
    length = max(len(string1), len(string2))
    
    if num1 < num2:
        num1 += 2 ** length
        diff = num1-num2
        bin_diff = bin(diff)[2:]
        if len(bin_diff) < length:
            bin_diff = "0" * (length-len(bin_diff)) + bin_diff
    else:
        diff = num1-num2
        bin_diff = bin(diff)[2:]
        bin_diff = "0" * (length-len(bin_diff)) + bin_diff
    return bin_diff

def and_binary_str(string1, string2):
    length = max(len(string1), len(string2))
    if len(string1) < length:
        string1 = "0" * (length-len(string1)) + string1
    if len(string2) < length:
        string2 = "0" * (length-len(string2)) + string2
    
    result = ""
    for i in range(length):
        if string1[i] == "1" and string2[i] == "1":
            result += "1"
        else:
            result += "0"
    return result
            
def or_binary_str(string1, string2):
    length = max(len(string1), len(string2))
    if len(string1) < length:
        string1 = "0" * (length-len(string1)) + string1
    if len(string2) < length:
        string2 = "0" * (length-len(string2)) + string2
    
    result = ""
    for i in range(length):
        if string1[i] == "0" and string2[i] == "0":
            result += "0"
        else:
            result += "1"
    return result
            
def not_binary_str(string1):
    length = len(string1)
    
    result = ""
    for i in range(length):
        if string1[i] == "0":
            result += "1"
        elif string1[i] == "1":
            result += "0"
    return result

def search_last(list, element):
    last_index = 0
    for index, i in enumerate(list):
        if i == element:
            last_index = index
    
    return last_index
            
def exp_cal(split_line, list_bit, var_name, **vars):
    #return the result of expression
    exp_value = bin_exp_cal(split_line, **vars)

    bits = list_bit[int(var_name[1:])]
    value = ""
    if bits >= len(exp_value):
        value = "0" * (bits-len(exp_value)) + exp_value
    else:
        value = exp_value[len(exp_value)-bits:]
    return value        

def bin_exp_cal(split_line, **vars):
    #return the result of binary expression
    list = []
    for line in split_line:
        if line != ")":
            list.append(line)
        else:
            LP_index = search_last(list, "(")                               #find the index of last "("
            exp_list = list[LP_index + 1:]                                  #select expression without LP
            list = list[:LP_index]                                          #delete "(" and latter elements
            if len(exp_list) == 2:
                #not
                value = exp_list[1]
                not_val = not_binary_str(value)
                list.append(not_val)
            elif len(exp_list) == 3:
                #and, or, add, sub
                if exp_list[1] == "+":
                    add_value = add_binary_str(exp_list[0], exp_list[2])
                    list.append(add_value)
                elif exp_list[1] == "-":
                    sub_value = sub_binary_str(exp_list[0], exp_list[2])
                    list.append(sub_value)
                elif exp_list[1] == "&":
                    and_value = and_binary_str(exp_list[0], exp_list[2])
                    list.append(and_value)
                elif exp_list[1] == "|":
                    or_value = or_binary_str(exp_list[0], exp_list[2])
                    list.append(or_value)
            elif len(exp_list) == 1:
                if exp_list[0][0] == "v":
                    #value = list_val[int(exp_list[0][1:])]
                    value = vars[exp_list[0]]
                    list.append(value)
                else:
                    value = exp_list[0]
                    list.append(value)
        
    return list[0]

if __name__ == "__main__":
    with open("./input.pig", "r") as f:
        g = open("./1.out", "w") 
        vars = dict()
        lines = f.readlines()
        list_bit = []                                                       #save bit of var
        list_remove = []                                                    #save removed 
        index = 0
        executed_lines = 0
        while index < len(lines):
            if executed_lines == 5000:
                print("too-many-lines", file=g)
                break
            line = lines[index]
            
            if line[0] == 'D':
                list_define = line.split()                                  #split define line
                var_name = list_define[2]
                vars[var_name] = "0" * int(list_define[1][2:])              #initialize var_val
                if var_name in list_remove:
                    i = int(var_name[1:])
                    list_bit[i] = int(list_define[1][2:])                   #update new-defined bits after removed
                    list_remove.remove(var_name)                            #remove the var from remove list
                else:
                    list_bit.append(int(list_define[1][2:]))                #update bit of defined variable
                index+=1                                                    #update read line
                executed_lines+=1                                           #update executed line
                continue
            
            if line[0] == 'A':
                list_assign = line.split()
                expression = list_assign[2:]                                #select the expression into list
                var_name = list_assign[1]                                   #generate variable name
                value = exp_cal(expression, list_bit, var_name, **vars)     #result of expression
                vars[var_name] = value                                      #assign value to dict() vars (might add bits at the same time)
                index+=1
                executed_lines+=1
                continue
                
            if line[0] == 'B':
                branch_line = line.split()
                expression = branch_line[2:]
                value = bin_exp_cal(expression, **vars)     #calculate expression
                executed_lines+=1
                if int(value) != 0:
                    index = int(branch_line[1])
                else:
                    index += 1
                continue
                
            if line[0] == 'R':
                remove_line = line.split()
                var_name = remove_line[1]
                list_remove.append(var_name)
                
                i = int(var_name[1:])
                list_bit[i] = 0
                
                index += 1
                executed_lines+=1
                continue
                
                
            if line[0] == 'O':
                print(vars[line[2:6]], file=g)
                index+=1
                executed_lines+=1
                continue

                