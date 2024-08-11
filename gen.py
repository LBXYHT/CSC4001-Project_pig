import random

#find existed variable
def find_exist_var(list_var_name, deleted_var):
    var_name = ""
    while True:
        var_name = random.choice(list_var_name)
        if var_name not in deleted_var:
            break
    return var_name

#generate D instruction
def gen_line_D(var_name, var_types):
    var_type = random.choice(var_types)
    bits = int(var_type[2:])
    stmt = f"D {var_type} {var_name}"
    return bits, stmt

#generate expression
#redundancy to include list_var_val, cancel it
def gen_exp(list_var_name, iteration_time, deleted_var):
    #bits: variable bit, list_var_bit: bit list, list_var_val: val list
    
    if iteration_time == 3:
        exp_type = random.choice(range(2))
    else:
        exp_type = random.choice(range(4))
            
    if exp_type == 0:
        #exp form: LP CONSTANT RP
        bit_range = random.choice([8, 16, 32, 64])
        val_type = random.randint(0, 1)
        if val_type == 0:
            val = "0" * (bit_range-1) + "1"
        else:
            val = "1" * (bit_range-1) + "0"
        exp = f"( {val} )"
        return exp
    
    elif exp_type == 1:
        #exp form: LP VAR RP
        var = find_exist_var(list_var_name, deleted_var)
        exp = f"( {var} )"
        return exp
    
    elif exp_type == 2:
        #exp form: LP EXP BOP EXP RP
        subexp1 = gen_exp(list_var_name, iteration_time+1, deleted_var)
        opr = random.choice(["+", "-", "&", "|"])
        subexp2 = gen_exp(list_var_name, iteration_time+1, deleted_var)
        exp = f"( {subexp1} {opr} {subexp2} )"
        return exp
        
    elif exp_type == 3:
        #exp form: LP NOT EXP RP
        subexp = gen_exp(list_var_name, iteration_time+1, deleted_var)
        exp = f"( ! {subexp} )"
        return exp
    
#generate A instruction
def gen_line_A(var_name, exp):
    stmt = f"A {var_name} {exp}"
    return stmt

#generate B instruction
def gen_line_B(rand_line, exp):
    rand_line = str(rand_line).zfill(3)
    stmt = f"B {rand_line} {exp}"
    return stmt
    
#generate R instruction
def gen_line_R(var_name):
    stmt = f"R {var_name}"
    return stmt

#generate O instruction
def gen_line_O(var_name):
    stmt = f"O {var_name}"
    return stmt


if __name__ == "__main__":
    f = open("./input.pig", "w")
    var_types = ["bv8", "bv16", "bv32", "bv64"]
    #var_nums = random.randint(1, 5)
    var_nums = random.randint(40, 100)
    list_var_bit = []
    list_var_name = []
    line_count = 0
    cycle = 0
    deleted_var = []
        
    while line_count < 998:
        #define instruction
        if cycle < var_nums:
            index_str = str(cycle).zfill(3)
            var_name = f"v{index_str}"
            bits, stmt = gen_line_D(var_name, var_types)
            #add new define var bit
            list_var_bit.append(bits)
            #add new define var name
            list_var_name.append(var_name)
            print(stmt, file=f)
            line_count += 1
        
        #bits = list_var_bit[i]
        if (cycle == 40 or cycle == 420) and len(deleted_var) != 0:
            delete_var_name = deleted_var[0]
            index = int(delete_var_name[1:])
            bits, stmt = gen_line_D(delete_var_name, var_types)
            #add new define var bit
            list_var_bit[index] = bits
            #delete var from deleted list
            deleted_var.remove(delete_var_name)
            print(stmt, file=f)
            line_count += 1
        
        #assign instruction
        var_name = find_exist_var(list_var_name, deleted_var)
        exp = gen_exp(list_var_name, 0, deleted_var)
        stmt = gen_line_A(var_name, exp)
        print(stmt, file=f)
        line_count += 1
        
        #output instruction
        #var_name = find_exist_var(list_var_bit, deleted_var)
        stmt = gen_line_O(var_name)
        print(stmt, file=f)
        line_count += 1
        
        #branch instruction
        if cycle == 150 or cycle == 400:
            if cycle == 150:
                rand_line = random.randint(400 + var_nums, 500 + var_nums)
            else:
                rand_line = random.randint(200 + var_nums, 300 + var_nums)
            i = random.randint(0, 1)
            #randomly decide whether the exp is 0
            if i == 0:
                exp = f"( 00000000 )"
            else:
                exp = gen_exp(list_var_name, 0, deleted_var)
            stmt = gen_line_B(rand_line, exp)
            print(stmt, file=f)
            line_count += 1
            
        if cycle == 100:
            while True:
                var_name = find_exist_var(list_var_name, deleted_var)
                var_index = int(var_name[1:])
                bits = list_var_bit[var_index]
                if bits == 8 or bits == 16:
                    break
            type = random.randint(0, 1)
            if type == 0:
                if bits == 8:
                    stmt = f"A {var_name} ( ( {var_name} ) + ( 00000001 ) )"
                elif bits == 16:
                    stmt = f"A {var_name} ( ( {var_name} ) + ( 10000000 ) )"
            else:
                stmt = f"A {var_name} ( 00000000 )"
            print(stmt, file=f)
            line_count += 1
                
            stmt = gen_line_O(var_name)
            print(stmt, file=f)
            line_count += 1
            
            exp = f"( {var_name} )"
            stmt = gen_line_B(line_count-2, exp)
            print(stmt, file=f)
            line_count += 1
            
        #remove instruction
        if cycle == 20 or cycle == 60 or cycle == 40:
            while True:
                #i = random.randint(0, var_nums-1)
                delete_var_name = random.choice(list_var_name)
                if delete_var_name not in deleted_var:
                    deleted_var.append(delete_var_name)
                    break
            stmt = gen_line_R(delete_var_name)
            print(stmt, file=f)
            line_count += 1
        
        cycle += 1