# Νικολακόπουλος Αριστείδης             5308    cs05308@uoi.gr
# Μπουζούκας Κωνσταντίνος Λευτέρης      5302    cs05302@uoi.gr
# Δεν καταλάβαμε τι εννοείται με το username στις διαφάνειες για την εργασία , σας βάλαμε τα mail μας 
import sys
import gc
#Syntax

#Globals
keywords = ["πρόγραμμα","δήλωση", "εάν", "τότε","επανάλαβε","μέχρι", "για","έως" ,"διάβασε",
             "γράψε" , "συνάρτηση", "διαδικασία", "διαπροσωπεία" , "είσοδος","έξοδος",
             "αρχή_συνάρτησης", "αρχή_διαδικασίας" , "αρχή_προγράμματος", "τέλος_συνάρτησης",
             "τέλος_διαδικασίας", "τέλος_προγράμματος" , "εκτέλεσε", "αλλιώς", "εάν_τέλος",
             "όσο" , "όσο_τέλος", "με_βήμα" ,"για_τέλος","δηλώσεις"] 

end_keywords = ["τέλος_συνάρτησης","τέλος_διαδικασίας", "τέλος_προγράμματος", "όσο_τέλος", "εάν_τέλος","για_τέλος","τέλος_προγράμματος","μέχρι"]

funclist = []
file_name = sys.argv[1]
file = open(file_name,"r")
f_str = file.read()
isComm = False
line_ind = 1
ind = 0
end_block = False
count_br = 0
count_big_br = 0
temp_li = 0
can_command = False
var_count = 0
syntax_check = 0
curr_block = ""
class token:
    def __init__(self,str,family,line):
        self.str = str 
        self.family = family
        self.line = line
        if family == "id":
            i = 0
            for i in range(len(keywords)):
                if str == keywords[i]:
                    self.family = "keyword"
                    break

            if str == "όχι":
                self.family = "not_Operator"
            if str == "και" or str == "ή":
                self.family = "bool_Operator"
   
class error:
    global line_ind
    def __init__(self,error_code):
        self.error_code = error_code 
        if error_code == 1: 
            print("Error in line :" + str(line_ind) + "\nWrong Syntax!")
        if error_code == 2:
            print("Failed Initialitation of The Program!")
        if error_code == 3:
            print("Program Did not terminate!\nLine:" + str(line_ind))
        if error_code == 4:
            print("Cannot Understand Symbol in line:" + str(line_ind))
        if error_code == 5:
            print("Comment Didnt Close \nStarted in Line: " + str(temp_li))

def check_br():
    global tok
    global count_big_br
    global count_br
    if type(tok) == token:
        while tok.family == "groupSymbol":
            if tok.str == "[" :
                count_big_br +=1
                tok = get_token()
            if tok.str == "]" :
                count_big_br -=1
                tok = get_token()
            if tok.str == "(" :
                count_br +=1
                tok = get_token()
            if tok.str == ")" :
                count_br -=1
                tok = get_token()

def expression():
    global tok
    check_br()
    if type(tok) == error:
        pass
    else:
        check_br()
        if tok.family == "id" or tok.family == "number":
            tok = get_token()
            check_br()
            if type(tok) == error:
                pass
            else:
                while True:
                    if type(tok) == error:
                        break
                    elif tok.family == "Math_Operator":
                        tok = get_token()
                        check_br()
                        if type(tok) == error:
                            break
                        if tok.family == "id" or tok.family == "number":
                            tok = get_token()
                            check_br()
                            if type(tok) == error:
                                break

                            pass
                        else:
                            tok = error(1)
                            break
                    elif tok.str == ";" or tok.family == "keyword":
                        break
                    else:
                        tok = error(1)
                        break
        else:
            tok = error(1)

def boolterm():
    global tok
    check_br()
    if type(tok) == error:
        pass
    else:
        check_br()
        if tok.family == "id" or tok.family == "number":
            tok = get_token()
            check_br()
            if type(tok) == error:
                pass
            else:
                while True:
                    if type(tok) == error:
                        break
                    elif tok.family == "Math_Operator":
                        tok = get_token()
                        check_br()
                        if type(tok) == error:
                            break
                        if tok.family == "id" or tok.family == "number":
                            tok = get_token()
                            check_br()
                            if type(tok) == error:
                                break

                            pass
                        else:
                            tok = error(1)
                            break
                    elif tok.family == "rel_Operator":
                        tok = get_token()
                        check_br()
                        if type(tok) == error:
                            pass
                        elif tok.family == "id" or tok.family == "number":
                            boolterm()
                            check_br()
                            
                        else:
                            tok = error(1)
                    elif tok.family == "bool_Operator" or tok.family == "keyword" or tok.str == ";":
                        break
                    
                    else:
                        tok = error(1)
                        break
        elif tok.family == "not_Operator":
            tok = get_token()
            check_br()
            if type(tok) == error:
                pass
            else:
                boolterm()
                check_br()
        else:
            tok = error(1)
    
def condition():
    global tok
    check_br()
    if type(tok) == error:
        pass
    else:
        boolterm()
        check_br()
        while True:
            if type(tok) == error:
                break
            elif tok.family == "bool_Operator":
                tok = get_token()
                check_br()
                if type(tok) == error:
                    break
                boolterm()
                check_br()
            elif tok.family == "keyword" or tok.str == ";":
                if count_big_br != 0 or count_br != 0:
                    tok = error(1) 
                break
            else:
                tok = error(1)
                break
   
def get_token():
    global tok
    global ind
    global f_str
    global line_ind
    ret = ""
    

    while True:
        tem = 0
        if ind >= len(f_str) -1:
                return "eof"
        if f_str[ind] == " " or f_str[ind] == "\t" or f_str[ind] =="":
            ind +=1
            pass
        elif f_str[ind] == "\n":
            line_ind +=1
            ind+=1
            pass
        else:
            ret = ret + f_str[ind]
            ind +=1
            break

    

    #Αναγωνριστικο
    if ret.isalpha():
        tem = 1
        f = "id"
        while f_str[ind].isalnum() or f_str[ind] == "_":
            ret = ret + f_str[ind]
            if ind + 1 >= len(f_str):
                break
            ind+=1

    #Αριθμος
    if ret.isnumeric():
        tem = 1
        f = "number"
        while True:
            if f_str[ind].isnumeric():
                ret = ret + f_str[ind]
                ind +=1
            elif f_str[ind].isalpha():
                ret = error(1)
                return ret
            else:
                break
        
    #delimiters
    if ret == "," or ret == ";":
        tem =1
        f = "delimiter"
    
    #group symbols
    if ret == "(" or ret == ")" or ret == "[" or ret == "]" or ret == "\"":
        tem = 1
        f = "groupSymbol"

    #math Operators
    if ret == "-" and tok.family!= "number" and tok.family != "id":
        tem = 1
        
        if f_str[ind].isnumeric():
            f = "number"
            while True:
                if f_str[ind].isnumeric():
                    ret = ret + f_str[ind]
                    ind +=1
                elif f_str[ind].isalpha():
                    ret = error(1)
                    return ret
                else:
                    break
        elif f_str[ind].isalpha():
            f = "id"
            while f_str[ind].isalnum() or f_str[ind] == "_":
                ret = ret + f_str[ind]
                if ind + 1 >= len(f_str):
                    break
                ind+=1
        else:
            f = "Math_Operator"
    elif ret == "+" or ret == "-" or ret == "*" or ret == "/" :
        tem = 1
        f = "Math_Operator"

    #Comments
    if ret == "{" or ret == "}":
        tem = 1
        f = "Comment_Operator"

    #Relational
    if ret == "<" or ret == ">" or ret == "=" :
        tem = 1
        f = "rel_Operator"
        if ret == "<" and f_str[ind] == "=":
            ret = ret + f_str[ind]
            ind +=1 
        if ret == "<" and f_str[ind] == ">":
            ret = ret + f_str[ind]
            ind +=1 
        if ret == ">" and f_str[ind] == "=":
            ret = ret + f_str[ind]
            ind +=1 

    #:
    if ret == ":":
        tem = 1
        if f_str[ind] == "=":
            ret = ret + f_str[ind]
            f = "AssignOperator"
            ind+=1
        else:
            f = "delimiter"
    
    #%
    if ret == "%":
        tem = 1
        f = "%_operator"

    if tem == 0 and isComm == False:
        tokk = error(4)
    else:
        tokk = token(ret,f,line_ind)

    if tokk == "{" and in_int == 1:
        while tokk.str != "}":
            tokk = get_token()
    return tokk
        
def block():
    global tok
    global line_ind
    global isComm
    global can_command
    prev_tok = tok
    if type(tok) == error:
        pass
    else:
        while True:
            if type(tok) == error:
                break
            else:
                if tok.str == "αρχή_προγράμματος":
                    can_command = True
                if tok.str == ";":
                    tok = get_token()
                    break
                if tok == "eof":
                    tok = prev_tok
                    break
                elif tok.str in end_keywords:
                    break
                elif tok.str == "αλλιώς": 
                    break
                elif tok.str == "δήλωση" :
                    state()
                elif tok.str == "δηλώσεις":
                    states()
                elif tok.str == "εάν":
                    if_stat()
                elif tok.str == "επανάλαβε":
                    rep_unt()
                elif tok.str == "όσο":
                    while_stat()
                elif tok.str == "για":
                    for_stat()
                elif tok.str == "διάβασε":
                    read()
                elif tok.str == "γράψε":
                    write()
                elif tok.family == "id":
                    assign()
                elif tok.str == "συνάρτηση":
                    can_command = True
                    func()
                    can_command = False
                elif tok.str == "διαδικασία":
                    can_command = True
                    procc()
                    can_command = False
                elif tok.str == "{":
                    global temp_li
                    temp_li = line_ind
                    isComm = True
                    temp = 0
                    while True:
                        tok = get_token()
                        if tok == "eof":
                            temp = 1
                            break
                        if tok.str == "}":
                            break
                    if temp == 0:
                        isComm == False
                    else:
                        tok = error(5)
     
                else:
                    tok = get_token()
            if type(tok) == error:
                break
            prev_tok = tok
  
def program():
    global tok 
    global syntax_check
    if tok.str == "πρόγραμμα":
        tok = get_token()
        
        if tok.family == "id":
            tok = get_token()
            block()
            if type(tok) != error:
                if tok.str == "τέλος_προγράμματος":
                    tok = get_token()
                    if tok == "eof":
                        print("Compilation Succesful")
                        syntax_check = 1
                    else:
                        print("Failed Compilation!\nFile did not end after program termination")
                else:
                    tok = error(3)
            else:
                pass
        else:
            tok = error(2)
    else:
        tok = error(2)
    
#Syntax Block Checkers
def state():
    global tok
    tok = get_token()
    prev_line = 1000
    if type(tok) == error:
        pass
    elif tok.family == "id":
        tok = get_token()
        if type(tok) == error:
            pass
        else:
            while tok.family != "keyword":
                if tok.str == "," or tok.str == ":":
                    tok = get_token()
                    if type(tok) == error:
                        break
                    
                    if tok.family == "id":
                        prev_line = tok.line
                        tok = get_token()
                        if type(tok) == error:
                            break
                        pass
                    else:
                        tok = error(1)
                        break
                else:
                    tok = error(1) 
                    break   
    else:   
        tok = error(1)

def states():
    global tok
    tok = get_token()
    prev_line = 1000
    if type(tok) == error:
        pass
    elif tok.family == "id":
        tok = get_token()
        if type(tok) == error:
            pass
        else:
            while tok.family != "keyword":
                if tok.str == "," or tok.str == ":":
                    tok = get_token()
                    if type(tok) == error:
                        break
                    
                    if tok.family == "id":
                        prev_line = tok.line
                        tok = get_token()
                        if type(tok) == error:
                            break
                        pass
                    else:
                        tok = error(1)
                        break
                elif tok.family == "id" and tok.line > prev_line:
                    prev_line = tok.line
                    tok = get_token()
                    if type(tok) == error:
                        break
                    pass
                else:
                    tok = error(1) 
                    break   
    else:   
        tok = error(1)

def if_stat():
    global tok
    tok = get_token()
    check_br()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    else:
        condition()
        check_br()
        if type(tok) == error:
            pass
        elif tok.str == "τότε":
            
            tok = get_token()
            check_br()
            if type(tok) == error:
                pass
            else:
                block()
                check_br()
                if type(tok) == error:
                    pass
                elif tok.str == "αλλιώς":
                    tok = get_token()
                    block()
                    check_br()
                    
                if type(tok) == error:
                    pass
                elif tok.str == "εάν_τέλος":
                    tok = get_token()
                    block()
                else:
                    error(1)
    
def rep_unt():
    global tok
    tok = get_token()
    check_br()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    else:
        block()
        check_br()
        if type(tok) == error:
            pass
        elif tok.str == "μέχρι":
            tok = get_token()
            check_br()
            condition()
            check_br()
            block()
            
        else:
            tok = error(1)

def while_stat():
    global tok
    tok = get_token()
    check_br()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    else:
        condition()
        check_br()
        if type(tok) == error:
            pass
        elif tok.str == "επανάλαβε":
            
            tok = get_token()
            check_br()
            if type(tok) == error:
                pass
            else:
                block()
                check_br()
                    
                if type(tok) == error:
                    pass
                elif tok.str == "όσο_τέλος":
                    tok = get_token()
                    block()
                else:
                    error(1)
        else:
            error(1)
    
def for_stat():
    global tok
    tok = get_token()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    else:
        if tok.family == "id":
            tok = get_token()
            if type(tok) == error:
                pass
            else:
                if tok.str == ":=":
                    tok = get_token()
                    expression()
                    if count_big_br != 0 or count_br != 0:
                        tok = error(1)
                    elif type(tok) == error:
                        pass
                    elif tok.str == "έως":
                        tok = get_token()
                        expression()
                        if count_big_br != 0 or count_br != 0:
                            tok = error(1)
                        elif type(tok) == error:
                            pass
                        elif tok.str == "με_βήμα":
                            tok = get_token()
                            expression()
                            if count_big_br != 0 or count_br != 0:
                                tok = error(1)
                            elif type(tok) == error:
                                pass
                            elif tok.str == "επανάλαβε":
                                tok = get_token()
                                block()
                                if type(tok) == error:
                                    pass
                                elif tok.str == "για_τέλος":
                                    tok = get_token()
                                    block()
                                else:
                                    tok = error(1)
                            else:
                                tok = error(1)
                        elif tok.str == "επανάλαβε":
                            tok = get_token()
                            block()
                            if type(tok) == error:
                                pass
                            elif tok.str == "για_τέλος":
                                tok = get_token()
                                block()
                            else:
                                tok = error(1)
                        else:
                            tok = error(1)
                    else:
                        tok = error(1)
                else:
                    tok = error(1)
        else:
            tok = error(1)

def read():
    global tok
    tok = get_token()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    elif tok.family == "id":
        tok = get_token()
        if type(tok) == error:
            pass
        elif tok.str in end_keywords:
            pass
        elif tok.str == ";":
            tok = get_token()
        else:
            tok = error(1)
    else:
        tok = error(1)

def write():
    global tok
    tok = get_token()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    else:
        expression()
        if type(tok) == error:
            pass
        elif tok.str == ";":
            tok = get_token()
        if count_big_br != 0 or count_br != 0:
            tok = error(1)

def assign():
    global tok
    tok = get_token()
    global can_command
    if can_command == False:
        tok = error(1)
    if type(tok) == error:
        pass
    else:
        if tok.str == ":=":
            tok = get_token()
            if type(tok) == error:
                pass
            elif tok.str in funclist:
                j = 0
                for i in range(len(funclist)):
                    if tok.str == funclist[i]:
                        j = funclist[i+1]
                tok = get_token()
                if type(tok) == error:
                    pass
                elif tok.str == "(":
                    tok = get_token()
                    if type(tok) == error:
                        pass
                    else:
                        if tok.str == "%":
                            tok = get_token()

                    if type(tok) == error:
                        pass
                    elif j == 0:
                        
                        if type(tok) == error:
                            pass
                        elif tok.str == ")":
                            tok = get_token()

                        else:
                            tok = error(1)
                    elif tok.family == "id":
                        tok = get_token()
                        k = 0
                        for k in range(j-1):
                            if type(tok) == error:
                                break
                            elif tok.str == ",":
                                tok = get_token()
                                if type(tok) == error:
                                    break
                                elif tok.str == "%":
                                    tok = get_token()
                                    if type(tok) == error:
                                        pass
                                    else:
                                        if tok.family == "id":
                                            tok = get_token()
                                elif tok.family == "id":
                                    tok = get_token()
                                else:
                                    tok = error(1)
                                    break
                            else:
                                tok = error(1)
                                break
                    else:
                        tok = error(1)

                    if type(tok) == error:
                        pass
                    elif tok.str == ")":
                        tok = get_token()
                        if type(tok) == error:
                            pass
                        elif tok.family == "keyword":
                            pass
                        elif tok.str == ";":
                            tok = get_token()
                        else:
                            tok = error(1)
                else:
                    tok = error(1)

            else:
                expression()

            if type(tok) == error:
                pass
            elif tok.str == ";":
                tok = get_token()
            if count_big_br != 0 or count_br != 0:
                tok = error(1)

def func():
    global var_count
    var_count = 0
    global tok
    tok = get_token()
    if type(tok) == error:
        pass
    elif tok.family == "id":
        funclist.append(tok.str)
        tok = get_token()
        if type(tok) == error:
            pass
        elif tok.str == "(":
            tok = get_token()
            if type(tok) == error:
                pass
            elif tok.family == "id" or  tok.str == ")":
                if tok.family == "id":
                    var_count +=1
                    tok = get_token()
                    if type(tok) == error:
                        pass
                    else:
                        while True:
                            if tok.str == ",":
                                tok = get_token()
                                if type(tok) == error:
                                    pass
                                else:
                                    if tok.family == "id":
                                        var_count+=1
                                        tok = get_token()
                                        pass
                                    if type(tok) == error:
                                        tok = error(1)
                                        break
                            elif tok.str == ")":
                                funclist.append(var_count)
                                tok = get_token()
                                break
                            else:
                                tok = error(1) 
                                break       
                else:
                    pass

                if type(tok) == error:
                    pass
                else:
                    if tok.str == "διαπροσωπεία":
                        tok = get_token()
                        if type(tok) == error:
                            pass
                        else:
                            while True:
                                if tok.str == "αρχή_συνάρτησης" :
                                    break
                                elif tok.str == "δηλώσεις":
                                    states()
                                elif tok.str == "είσοδος" or tok.str == "έξοδος" or tok.str == "δήλωση":
                                    state()
                                else:
                                    tok = error(1)
                                    break
                            
                            if type(tok) == error:
                                pass
                            else:
                                block()
                                if type(tok) == error:
                                    pass
                                elif tok.str == "τέλος_συνάρτησης":
                                    tok = get_token()
                                    pass
                                else:
                                    tok = error(1)
                    else:
                        tok = error(1)

            else:
                tok = error(1)
            
        else:
            tok = error(1)
    else:
        tok = error(1)

def procc():
    global var_count
    var_count = 0
    global tok
    tok = get_token()
    if type(tok) == error:
        pass
    elif tok.family == "id":
        funclist.append(tok.str)
        tok = get_token()
        if type(tok) == error:
            pass
        elif tok.str == "(":
            tok = get_token()
            if type(tok) == error:
                pass
            elif tok.family == "id" or  tok.str == ")":
                if tok.family == "id":
                    var_count +=1
                    tok = get_token()
                    if type(tok) == error:
                        pass
                    else:
                        while True:
                            if tok.str == ",":
                                tok = get_token()
                                if type(tok) == error:
                                    pass
                                else:
                                    if tok.family == "id":
                                        var_count+=1
                                        tok = get_token()
                                        pass
                                    if type(tok) == error:
                                        tok = error(1)
                                        break
                            elif tok.str == ")":
                                funclist.append(var_count)
                                tok = get_token()
                                break
                            else:
                                tok = error(1) 
                                break       
                else:
                    pass

                if type(tok) == error:
                    pass
                else:
                    if tok.str == "διαπροσωπεία":
                        tok = get_token()
                        if type(tok) == error:
                            pass
                        else:
                            while True:
                                if tok.str == "αρχή_διαδικασίας" :
                                    break
                                elif tok.str == "δηλώσεις":
                                    states()
                                elif tok.str == "είσοδος" or tok.str == "έξοδος" or tok.str == "δήλωση":
                                    state()
                                else:
                                    tok = error(1)
                                    break
                            
                            if type(tok) == error:
                                pass
                            else:
                                block()
                                if type(tok) == error:
                                    pass
                                elif tok.str == "τέλος_διαδικασίας":
                                    tok = get_token()
                                    pass
                                else:
                                    tok = error(1)
                    else:
                        tok = error(1)

            else:
                tok = error(1)
            
        else:
            tok = error(1)
    else:
        tok = error(1)

def exec():
    global tok
    tok = get_token()
    if type(tok) == error:
        pass
    else:
        if tok.str in funclist:
            j = 0
            for i in range(len(funclist)):
                if tok.str == funclist[i]:
                    j = funclist[i+1]

            tok = get_token()
            if type(tok) == error:
                pass
            elif tok.str == "(":
                tok = get_token()
                if type(tok) == error:
                    pass
                elif j == 0:
                    if type(tok) == error:
                        pass
                    elif tok.str == ")":
                        tok = get_token()
                    else:
                        tok = error(1)
                elif tok.family == "id":
                    tok = get_token()
                    k = 0
                    for k in range(j-1):
                        if type(tok) == error:
                            break
                        elif tok.str == ",":
                            tok = get_token()
                            if type(tok) == error:
                                break
                            elif tok.str == "%":
                                tok = get_token()
                                if type(tok) == error(1):
                                    pass
                                else:
                                    if tok.family == "id":
                                        tok = get_token()
                            elif tok.family == "id":
                                tok = get_token()
                            else:
                                tok = error(1)
                                break
                        else:
                            tok = error(1)
                            break
                else:
                    tok = error(1)
                if type(tok) == error:
                    pass
                elif tok.str == ")":
                    tok = get_token()
                    if type(tok) == error:
                        pass
                    elif tok.family == "keyword":
                        pass
                    elif tok.str == ";":
                        tok = get_token()
                        pass
                    else:
                        tok = error(1)
                else:
                    tok = error(1)
            else:
                tok = error(1)   
        else:
            tok = error(1)

def syntax_analyzer():
    global tok
    tok = get_token()
    program()

#Intermediate Code
    
#Globals
is_in_g = 0
quads = []
label_ind = 1
temp_ind = 0
pr_name = ""
interfunc_list = []
temp_len = 0
class quad:
    def __init__(self,op,op1,op2,op3):
        global label_ind
        self.label = label_ind
        label_ind+=1
        self.op = op
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __str__(self):
        return f'{self.label}: {self.op},{self.op1},{self.op2},{self.op3}'    

class interfunc:
    def __init__(self,name,fType):
        self.name = name
        self.fType = fType
#TOOLS
def log_exp(args):
    global is_in_g
    global tok
    global temp_len
    ll = []
    for i in args:
        ll.append(i)
    
    if not args:
        while tok.str == "[":
            ll.append(tok.str)
            tok = get_token()

        ll.append(math_exp([]))
        ll.append(tok.str)
        tok = get_token()
        ll.append(math_exp([]))
        while True:
            if tok.str == "και":
                ll.append(tok.str)
                tok = get_token()
                while tok.str == "]" or tok.str == "[":
                    ll.append(tok.str)
                    tok = get_token()
                ll.append(math_exp([]))
                ll.append(tok.str)
                tok = get_token()
                ll.append(math_exp([]))
                while tok.str == "]" or tok.str == "[":
                    ll.append(tok.str)
                    tok = get_token()
            elif tok.str == "ή":
                ll.append(tok.str)
                tok = get_token()
                while tok.str == "]" or tok.str == "[":
                    ll.append(tok.str)
                    tok = get_token()
                ll.append(math_exp([]))
                ll.append(tok.str)
                tok = get_token()
                ll.append(math_exp([]))
                while tok.str == "]" or tok.str == "[":
                    ll.append(tok.str)
                    tok = get_token()
            else:
                break
    
    rets = empty_list()          
    temp = empty_list()

    
    while len(ll) > 0:
        if ll[0] == "ή":
            ll.pop(0)
            backpatch(rets,next_quad())
            rets.clear()
            if ll[0] != "[":
                temp.append(next_quad())
                gen_quad(ll[1],ll[0],ll[2],"_")
                ll.pop(0)
                ll.pop(0)
                ll.pop(0)
        elif ll[0] == "και":
            ll.pop(0)
            if ll[0] != "[":
                t2 = make_list(next_quad())
                gen_quad("jump","_","_","_")
                backpatch(temp,next_quad())
                temp.clear()
                t = make_list(next_quad())
                temp.append(next_quad())
                gen_quad(ll[1],ll[0],ll[2],"_")
                rets.append(next_quad())
                backpatch(t2,next_quad())
                gen_quad("jump","_","_","_")
                backpatch(t,next_quad())
                ll.pop(0)
                ll.pop(0)
                ll.pop(0)
            else:
                backpatch(temp,next_quad())
                temp = empty_list()
        elif ll[0] == "[":
            temp_ind = len(ll) - 1
            par_ind = ll.index("[")
            new_ll = []
            i = par_ind +1
            is_open = 0
            count_of_br = 0
            while i in range(len(ll)):
                if ll[i] == "[":
                    is_open +=1
                    count_of_br +=1
                if ll[i] == "]" and is_open == 0:
                    temp_ind = i
                    break
                elif ll[i] == "]":
                    is_open -=1
                i+=1

            new_ind = par_ind +1

            while new_ind < temp_ind:
                new_ll.append(ll[new_ind])
                new_ind+=1

            is_in_g += 1
            temp_l = log_exp(new_ll)
            for i in range(len(temp_l)-temp_len):
                rets.append(temp_l[0])
                temp_l.pop(0)
            for i in temp_l:
                temp.append(i)

            is_in_g -= 1
            while ll[0] != "]" or count_of_br != 0:
                if ll[0] == "]":
                    count_of_br -=1 
                ll.pop(0)
            ll.pop(0)
        else:
            temp.append(next_quad())
            gen_quad(ll[1],ll[0],ll[2],"_")
            ll.pop(0)
            ll.pop(0)
            ll.pop(0)

    if is_in_g == 0:
        rets.append(next_quad())
        gen_quad("jump","_","_","_")
        backpatch(temp,next_quad())
    else:
        temp_len = len(temp)
        for i in temp:
            rets.append(i)
        
    return rets

def math_exp(args):
    global tok
    ll = args
    if not ll:
        ll.append(tok.str)
        if tok.str == "(":
            tok = get_token()
            ll.append(tok.str)
        tok = get_token()
    
        while True:
                if tok.family == "Math_Operator":
                    ll.append(tok.str)
                    tok = get_token()
                    if tok.family == "id" or tok.family == "number":
                        ll.append(tok.str)
                        tok = get_token()
                    if tok.str == ")":
                        ll.append(tok.str)
                        tok = get_token()
                elif  tok.str == "(" or tok.str == ")" :
                    ll.append(tok.str)
                    tok = get_token()
                    ll.append(tok.str)
                    tok = get_token()
                else:
                    break

        if ";" in ll:
            ll.remove(";")

    while len(ll) > 1:
        if "(" in ll:
            temp_ind = len(ll) - 1
            par_ind = ll.index("(")
            new_ll = []
            is_open = 0
            i = par_ind +1
            while i in range(len(ll)):
                if ll[i] == "(":
                    is_open+=1
                if ll[i] == ")" and is_open == 0:
                    temp_ind = i
                    break
                elif ll[i] == ")":
                    is_open -=1
                i+=1


            new_ind = par_ind +1

            while new_ind < temp_ind:
                new_ll.append(ll[new_ind])
                new_ind+=1
            temm = math_exp(new_ll)
            ll[par_ind] = temm
            for i in range(temp_ind - par_ind):
                ll.pop(par_ind+1)
        elif "*" in ll:
            op_ind = ll.index("*")
            t = new_temp()
            gen_quad("*",ll[op_ind - 1],ll[op_ind +1],t)
            ll[op_ind-1] = t
            ll.pop(op_ind)
            ll.pop(op_ind)
        elif "/" in ll:
            op_ind = ll.index("/")
            t = new_temp()
            gen_quad("/",ll[op_ind - 1],ll[op_ind +1],t)
            ll[op_ind-1] = t
            ll.pop(op_ind)
            ll.pop(op_ind)
        elif "+" in ll:
            op_ind = ll.index("+")
            t = new_temp()
            gen_quad("+",ll[op_ind - 1],ll[op_ind +1],t)
            ll[op_ind-1] = t
            ll.pop(op_ind)
            ll.pop(op_ind)
        elif "-" in ll:
            op_ind = ll.index("-")
            t = new_temp()
            gen_quad("-",ll[op_ind - 1],ll[op_ind +1],t)
            ll[op_ind-1] = t
            ll.pop(op_ind)
            ll.pop(op_ind)
    return ll[0]

def gen_quad(op,op1,op2,op3):
    q = quad(op,op1,op2,op3)
    quads.append(q)
    
    return q

def next_quad():
    global label_ind
    return label_ind

def new_temp():
    global temp_ind 
    t = f'T_{temp_ind}'
    temp_ind+=1
    
    scopes[curr_scope].ent_list.append(entity([3,t,offsets[curr_scope]]))
    offsets[curr_scope] +=4
    return t

def empty_list():
    return []

def make_list(label):
    l = [label]
    return l

def merge_list(l1,l2):
    for i in l2:
        l1.append(i)
    
    return l1

def backpatch(l,label):
    global quads
    for i in l:
        for j in quads:
            if i == j.label:
                j.op3 = label

#Blocks
def subblock():
    global curr_block
    global tok
    global interfunc_list
    global curr_scope
    global offsets
    global scopes
    global is_in_f
    fType = 0
    while tok.str != "αρχή_προγράμματος":
        if tok.str == "δήλωση":
            tok = get_token()
            while tok.str not in keywords:
                if tok.family == "id":
                    scopes[curr_scope].ent_list.append(entity([0,tok.str,offsets[curr_scope]]))
                    offsets[curr_scope] += 4
                    tok = get_token()
                else:
                    tok = get_token()
        elif tok.str == "συνάρτηση" or tok.str == "διαδικασία":
            is_in_f = True
            if tok.str == "διαδικασία":
                fType = 1
            tok = get_token()
            interfunc_list.append(interfunc(tok.str,fType))
            gen_quad("begin_block",tok.str,"_","_")
            ql = next_quad()
            scopes[curr_scope].ent_list.append(entity([1,tok.str,fType,ql,[]]))
            curr_block = tok.str
            offsets[curr_scope] +=4
            tok = get_token()
            count_args = 0
            if tok.str == "(":
                    while tok.str != ")":
                        tok = get_token()
                        if tok.family == "id":
                            count_args +=1
            tok = get_token()
            scope([],curr_scope+1)
            while count_args > 0:
                if tok.str == "είσοδος":
                    tok = get_token()
                    while tok.str not in keywords:
                        if tok.family == "id":
                            temp = entity([2,tok.str,"CV",offsets[curr_scope]])
                            for i in scopes[curr_scope - 1].ent_list:
                                if i.name == curr_block:
                                    i.args.append(temp)
                            scopes[curr_scope].ent_list.append(temp)
                            offsets[curr_scope]+=4
                            count_args -=1
                            tok = get_token()
                elif tok.str == "έξοδος":
                    tok = get_token()
                    if tok.family == "id":
                            temp = entity([2,tok.str,"REF",offsets[curr_scope]])
                            for i in scopes[curr_scope - 1].ent_list:
                                if i.name == curr_block:
                                    i.args.append(temp)
                            scopes[curr_scope].ent_list.append(temp)
                            offsets[curr_scope]+=4
                            count_args -=1
                            tok = get_token()
                else:
                    tok = get_token()
            subblock()

            for i in scopes[curr_scope - 1].ent_list:
                if curr_block == i.name:
                    i.framelength = offsets[curr_scope]
            if quads[len(quads) - 1].op ==  "end_block":
                produce_final_code()
            del_scopes.append(scopes[curr_scope])
            scopes.pop(curr_scope)
            offsets.pop(curr_scope)
            curr_scope -=1
            is_in_f = False
        elif tok.str == "αρχή_συνάρτησης" or tok.str == "αρχή_διαδικασίας":
            interblock()
            tok = get_token()
            break
        else:
            tok = get_token()
           
def interblock():
    global tok
    global curr_block
    end_keywords.append("αλλιώς")
    while tok.str not in end_keywords:

        if tok.family == "id":
            tt = 0
            if tok.str in funclist:
                tt =1
            
            temp = tok.str
            tok = get_token()
            if tok.str == ":=":
                temp2 = inter_assign()
                gen_quad(":=",temp2,"_",temp)
            if tt == 1:
                gen_quad("retv",temp,"_","_")
           
        elif tok.str == "διάβασε":
            tok = get_token()
            inter_read()
            tok = get_token()
        elif tok.str == "γράψε":
            tok = get_token()
            inter_write()
        elif tok.str == "εκτέλεσε":
            tok = get_token()
            inter_exec(tok.str)
        elif tok.str == "εάν":
            tok = get_token()
            inter_if()
            if tok.str!= "τέλος_προγράμματος":
                tok = get_token()
        elif tok.str == "επανάλαβε":
            tok = get_token()
            inter_repeat()
            if tok.str!= "τέλος_προγράμματος":
                tok = get_token()
        elif tok.str == "όσο":
            tok = get_token()
            inter_while()
            if tok.str!= "τέλος_προγράμματος":
                tok = get_token()
        elif tok.str == "για":
            tok = get_token()
            inter_for()
            if tok.str!= "τέλος_προγράμματος":
                tok = get_token()
        else:
            tok = get_token()

        

       

    if tok.str == "τέλος_συνάρτησης" or tok.str == "τέλος_διαδικασίας":
        gen_quad("end_block",curr_block,"_","_")

#Producers
def inter_assign():
    global tok
    tok = get_token()
    if tok.str in funclist:
        return inter_exec(tok.str)
    else:
        return math_exp([])

def inter_exec(name):
    global tok
    tok = get_token()
    myF = object
    for i in interfunc_list:
        if i.name == name:
            myF = i
    while tok.str != ")":
        if tok.str == "%":
            tok = get_token()
            gen_quad("par",tok.str,"REF","_")
            tok = get_token()
        elif tok.family == "id":
            gen_quad("par",tok.str,"CV","_")
            tok = get_token()
        else:
            tok = get_token()
    t = new_temp()
    if myF.fType == 0:
        gen_quad("RET",t,"_","_")
    gen_quad("call","_","_",name)
    return t

def inter_read():
    global tok
    gen_quad("inp",tok.str,"_","_")

def inter_write():
    temp = math_exp([])
    gen_quad("outp",temp,"_","_")

def inter_if():
    global tok
    js = log_exp([])
    interblock()
    if tok.str == "αλλιώς":
        t = make_list(next_quad())
        gen_quad("jump","_","_","_")
        backpatch(js,next_quad())
        tok = get_token()
        interblock()
        backpatch(t,next_quad())
    else:
        backpatch(js,next_quad())

def inter_repeat():
    global tok
    check_cond = make_list(next_quad())
    gen_quad("jump","_","_","_")
    bp_block = next_quad()
    interblock()
    tok = get_token()
    backpatch(check_cond,next_quad())
    js = log_exp([])
    jump = make_list(next_quad())
    gen_quad("jump","_","_","_")
    backpatch(jump,bp_block)
    backpatch(js,next_quad())

def inter_while():
    global tok
    qn = next_quad()
    js = log_exp([])
    tok = get_token()
    interblock()
    gen_quad("jump","_","_",str(qn))
    backpatch(js,next_quad())

def inter_for():
    global tok
    op = "+"
    t1 = tok.str
    tok = get_token()
    t2 = tok.str
    t3 = inter_assign()
    gen_quad(t2,t3,"_",t1)
    tok = get_token()
    con = tok.str
    check_cond = next_quad()
    js = make_list(check_cond)
    gen_quad("_",con,t1,"_")
    jump = make_list(next_quad())
    gen_quad("jump","_","_","_")
    tok = get_token()
    tok = get_token()
    if int(tok.str) < 0:
        for i in quads:
            if i.label == check_cond:
                i.op = "<="
        op = "-"
    else:
        for i in quads:
            if i.label == check_cond:
                i.op = ">="
    second = tok.str
    nq = next_quad()
    gen_quad(op,t1,second,t1)
    tl = make_list(next_quad())
    gen_quad("jump","_","_","_")
    backpatch(tl,check_cond)
    backpatch(jump,next_quad())
    tok = get_token()
    tok = get_token()
    interblock()
    nj = make_list(next_quad())
    gen_quad("jump","_","_","_")
    backpatch(nj,nq)
    backpatch(js,next_quad())
    
#Int Code Producer
def produce_int_code():
    mkfile = open("int_Code.int","w")
    global tok
    global pr_name
    scope([],0)
    tok = get_token()
    if tok.str == "πρόγραμμα":
        tok = get_token()
        pr_name = tok.str

    subblock()
    gen_quad("begin_block",pr_name,"_","_")
    interblock()
    if tok.str == "τέλος_προγράμματος":
        gen_quad("halt","_","_","_")
        gen_quad("end_block","_","_","_")
    for i in quads:
        mkfile.write(str(i)+"\n")

#Record Structures and globals
scopes = []
offsets = []
curr_scope = 0
is_in_f = False
del_scopes = []
class entity:
    def __init__(self,args):
        if args[0] == 0: #Variable
            self.ent_type = 0
            self.name = args[1]
            self.offset = args[2]
        if args[0] == 1: #function
            self.ent_type = 1
            self.name = args[1]
            self.type = args[2]
            self.start_quad = args[3]
            self.args = args[4]
            self.framelength = 0
        if args[0] == 2: #args
            self.ent_type = 2
            self.name = args[1]
            self.mode = args[2]
            self.offset = args[3]
        if args[0] == 3: #temp
            self.ent_type = 0
            self.name = args[1]
            self.offset = args[2]

class scope:
    def __init__(self,ent_list,nest_ind):
        global curr_scope
        global offsets
        global scopes
        self.ent_list = ent_list
        self.nest_ind = nest_ind
        scopes.append(self)
        offsets.append(12)
        curr_scope = nest_ind

class arguement:
    def __init__(self,par_mode,type):
        self.par_mode = par_mode
        self.type = type

#Final Code Producer
in_del_scopes = False
count_Q = 0
asm_code = []
ops = [":=","+","-","*","/"]
jumps = ["jump","=","<",">","<=",">=","<>"]
#TOOLS
def gnlvcode(var):
    global curr_scope
    global scopes
    global asm_code

    offset = 0 
    for i in scopes[curr_scope].ent_list:
        
        if i.name == var:
            if i.ent_type == 1:
                offset = i.framelength
            else:
                offset = i.offset

    asm_code.append("   lw t0,-4(sp)\n")
    temp = curr_scope - 1
    while temp >= 0:
        for i in scopes[temp].ent_list:
            if var == i.name:
                asm_code.append("   lw t0,-4(t0)\n")
                if i.ent_type == 1:
                    offset = i.framelength
                else:
                    offset = i.offset
        temp -=1
    asm_code.append("   addi t0,t0,-" + str(offset)+"\n")
    return 

def loadvr(v,r):
    global curr_scope
    global scopes
    global asm_code

    if v.isnumeric():
        asm_code.append("   li " + r +","+v+"\n" )
    else:
        type_temp = 0
        my_of = 0
        for i in scopes[curr_scope].ent_list:
            if i.name == v:
                if i.ent_type == 0 or i.ent_type == 3:
                    type_temp = 1
                    my_of = i.offset
                if i.ent_type == 2:
                    if i.mode == "CV":
                        my_of = i.offset
                        type_temp = 1
                    elif i.mode == "REF":
                        my_of = i.offset
                        type_temp = 2
                

        if type_temp == 0:
            t = curr_scope - 1
            while t >= 0:
                for i in scopes[t].ent_list:
                    if i.name == v:
                        if i.ent_type == 2:
                            if i.mode =="CV":
                                type_temp = 3
                            else:
                                type_temp = 4
                        elif i.ent_type == 1:
                            type_temp = 3
                t-=1
        if type_temp == 1:
            asm_code.append("   lw "+r+",-" +str(my_of)+"(sp)\n" )
        if type_temp == 2:
            asm_code.append("   lw t0,-" +str(my_of)+"(sp)\n" )
            asm_code.append("   lw " + r + ",(t0)\n")
        if type_temp == 3:
            gnlvcode(v)
            asm_code.append("   lw "+r+",(t0)\n")
        if type_temp == 4:
            gnlvcode(v)
            asm_code.append("   lw t0,(t0)") 
            asm_code.append("   lw " +r + ",(t0)")

def storerv(r,v):
    global curr_scope
    global scopes
    global asm_code

    type_temp = 0
    my_of = 0
    for i in scopes[curr_scope].ent_list:
        if i.name == v:
            if i.ent_type == 0 or i.ent_type == 3:
                type_temp = 1
                my_of = i.offset
            if i.ent_type == 2:
                if i.mode == "CV":
                    my_of = i.offset
                    type_temp = 1
                elif i.mode == "REF":
                    my_of = i.offset
                    type_temp = 2

    if type_temp == 0:
        t = curr_scope - 1
        while t >= 0:
            for i in scopes[t].ent_list:
                if i.name == v:
                    if i.ent_type == 2:
                        if i.mode =="CV":
                            type_temp = 3
                        else:
                            type_temp = 4
                    elif i.ent_type == 1:
                        type_temp = 3
            t-=1
    if type_temp == 1:
        asm_code.append("   sw "+r+",-" +str(my_of)+"(sp)\n" )
    if type_temp == 2:
        asm_code.append("   lw t0,-" +str(my_of)+"(sp)\n" )
        asm_code.append("   sw " + r + ",(t0)\n")
    if type_temp == 3:
        gnlvcode(v)
        asm_code.append("   sw "+r+",(t0)\n")
    if type_temp == 4:
        gnlvcode(v)
        asm_code.append("   lw t0,(t0)") 
        asm_code.append("   sw " + r + ",(t0)")

#Producers
def produce_op(myQ):
    if myQ.op == ":=":
        loadvr(myQ.op1,"t1")
        storerv("t1",myQ.op3)
    else:
        loadvr(myQ.op1,"t1") 
        loadvr(myQ.op2,"t2")

        if myQ.op == "+":
            asm_code.append("   add t1,t2,t1\n")
        elif myQ.op == "-":
            asm_code.append("   sub t1,t2,t1\n")
        elif myQ.op == "*":
            asm_code.append("   mul t1,t2,t1\n")
        elif myQ.op == "/":
            asm_code.append("   div t1,t2,t1\n")
            
        storerv("t1",myQ.op3)
   
def produce_jump(myQ):
    if myQ.op == "jump":
        asm_code.append("   j L_" + str(myQ.op3) + "\n")
    else:
        loadvr(myQ.op1,"t1")
        loadvr(myQ.op2,"t2")
        if myQ.op == "=":
            asm_code.append("   beq t1,t2,L_" + str(myQ.op3)+"\n")
        elif myQ.op == "<":
            asm_code.append("   blt t1,t2,L_" + str(myQ.op3)+"\n")
        elif myQ.op == ">":
            asm_code.append("   bgt t1,t2,L_" + str(myQ.op3)+"\n")
        elif myQ.op == "<=":
            asm_code.append("   ble t1,t2,L_" + str(myQ.op3)+"\n")
        elif myQ.op ==" >=":
            asm_code.append("   bge t1,t2,L_" + str(myQ.op3)+"\n")
        elif myQ.op == "<>" :
            asm_code.append("   bne t1,t2,L_" + str(myQ.op3)+"\n")

def produce_read(myQ):
    asm_code.append("   li a7,5\n")
    asm_code.append("   ecall\n")
    storerv("a0",myQ.op1)

def produce_write(myQ):
    loadvr(myQ.op1,"a0")
    asm_code.append("   li a7,1\n")
    asm_code.append("   ecall\n")

def produce_final_code():
    global quads
    global count_Q
    global asm_code
    mkfile = open("final.asm","w")
    addi_exists = 0
    par_count = 0
    leng = len(quads) - count_Q
    for i in range(leng):
        myQ = quads[count_Q]
        if myQ.op == "begin_block" and myQ.op1 == pr_name:
            asm_code.append("LMain:\n")
            asm_code.append("   addi sp,sp," + str(offsets[curr_scope])+"\n")
            asm_code.append("   move gp,sp\n")
        elif myQ.op == "begin_block":
            asm_code.append("L_"+ str(myQ.op1) + ":\n")
            asm_code.append("   sw ra,(sp)\n")
        else:
            asm_code.append("L_" + str(myQ.label)+":\n")
        
    

        if myQ.op in ops:
            produce_op(myQ)
        elif myQ.op in jumps:
            produce_jump(myQ)
        elif myQ.op == "halt":
            asm_code.append("   li a0,0\n")
            asm_code.append("   li a7,93\n")
            asm_code.append("   ecall\n")
        elif myQ.op == "inp":
            produce_read(myQ)
        elif myQ.op == "outp":
            produce_write(myQ)
        elif myQ.op == "par" or myQ.op == "call" or myQ.op == "RET":
            if not addi_exists:
                ind = count_Q 
                breaker = 0
                while True:
                    if quads[ind].op3 in funclist:
                        fl = 0
                        for j in scopes[curr_scope].ent_list:
                            if quads[ind].op3 == j.name:
                                fl = j.framelength
                                breaker = 1
                                break
                        asm_code.append("   addi fp,sp," + str(fl) + "\n")
                        addi_exists = 1
                    if breaker:
                        break
                    ind +=1

            if myQ.op == "par":
                if myQ.op2 == "CV":
                    par_count +=1
                    loadvr(myQ.op1,"t1")
                    off_par = 12 + (par_count - 1)*4
                    asm_code.append("   sw t1,-"+str(off_par)+"(fp)\n")
                if myQ.op2 == "REF":
                    par_count+=1
                    off_par = 12 + (par_count - 1)*4
                    my_par = None
                    
                    for j in scopes[curr_scope].ent_list:
                        if myQ.op1 == j.name:
                            my_par = j

                    if my_par is not None:

                        if my_par.ent_type == 2 and  my_par.mode == "REF":
                            asm_code.append("   lw t0,-" + str(my_par.offset)+ "(sp)\n") 
                            asm_code.append("   sw t0,-" + str(off_par) + "(fp)\n")

                        else:
                            asm_code.append("   addi t0,sp,-" + str(my_par.offset) + "\n")
                            asm_code.append("   sw t0,-" + str(off_par) + "(fp)\n")
                    else:
                        search_sc = curr_scope -1 
                        while search_sc >=0:
                            for j in scopes[search_sc].ent_list:
                                if j.name == myQ.op1:
                                    my_par = j
                            search_sc -=1

                        if my_par.ent_type == 2 and  my_par.mode == "REF":
                            gnlvcode(my_par.name)
                            asm_code.append("   lw t0,(t0)\n") 
                            asm_code.append("   sw t0,-" + str(off_par) + "(fp)\n")

                        else:
                            gnlvcode(my_par.name)
                            asm_code.append("   sw t0,-" + str(off_par) + "(fp)\n")
                            
            elif myQ.op == "RET":
                my_offset = 0
                for j in scopes[curr_scope].ent_list:
                    if myQ.op1 == j.name:
                        my_offset = j.offset
                        break
                asm_code.append("   addi t0,sp,-" + str(my_offset) + "\n")
                asm_code.append("   sw t0,-8(fp)\n")

            elif myQ.op == "call":
                is_parent = 0
                for j in scopes[curr_scope].ent_list:
                    if j.name == myQ.op3:
                        is_parent = 1
                if is_parent:
                   asm_code.append("   sw sp,‐4(fp)\n")
                else:
                    asm_code.append("   lw t0, ‐4(sp)\n")
                    asm_code.append("   sw t0, ‐4(fp)\n")

                frame_l = 0
                for m in scopes:
                    for n in m.ent_list:
                        if myQ.op3 == n.name:  
                            frame_l = n.framelength
                
                asm_code.append("   addi sp,sp," + str(frame_l) + "\n")
                asm_code.append("   jal L_" + myQ.op3 + "\n")
                asm_code.append("   addi sp,sp,-" + str(frame_l) + "\n")
                par_count = 0
                addi_exists = 0
        elif myQ.op == "retv":
            loadvr(myQ.op1,"t1")
            asm_code.append("   lw t0,-8(sp)\n")
            asm_code.append("   sw t1,(t0)\n")
        elif myQ.op == "end_block":
            asm_code.append("   lw ra,(sp)\n") 
            asm_code.append("   jr ra\n")
        
        count_Q+=1
    for i in asm_code:
        mkfile.write(i)

#********************* MAIN *********************#
in_int = 0
syntax_analyzer()
line_ind = 1
ind = 0
if syntax_check:
    in_int = 1
    asm_code.append("L0:\n  b LMain\n")
    produce_int_code()
    produce_final_code()
    

#Για τύπωση του πίνακα συμβόλων
for i in scopes[0].ent_list:
    if i.ent_type == 0:
        print("(" + i.name + " / " + str(i.offset) + ")")
    if i.ent_type == 1:
        print("(" + i.name + " / " + str(i.start_quad) + " / " + str(i.framelength) + ")")
        for j in i.args:
            if j.mode == "CV":
                print("<in>")
            elif j.mode == "REF":
                print("<inout>")
    if i.ent_type == 2:
        print("(" + i.name + " / " + i.mode + " / " + str(i.offset) + ")")

print("DELETED SCOPES")

for j in del_scopes:
    print(j.nest_ind)
    for i in j.ent_list:
        if i.ent_type == 0:
            print("(" + i.name + " / " + str(i.offset) + ")")
        if i.ent_type == 1:
            print("(" + i.name + " / " + str(i.start_quad) + " / " + str(i.framelength) + ")")
        if i.ent_type == 2:
            print("(" + i.name + " / " + i.mode + " / " + str(i.offset) + ")")

