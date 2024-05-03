


class LexerError(Exception):
  pass

class ParserError(Exception):
  pass

class TypeError(Exception):
  pass

class Token:
  def __init__(self, type, value, line, char):
    self.type = type
    self.value = value
    self.line = line
    self.char = char

  def __str__(self):
    return f"{self.type}:{self.value}:{self.line}:{self.char}"


class TokenCombinations:
  def __init__(self, type, tokens, data=[]):
    self.type = type
    self.tokens = tokens
    self.data = data

  def __str__(self):
    tokens = " ".join([str(token) for token in self.tokens])
    dataTokens = "\n\t".join([str(token) for token in self.data])
    data = f"Combination {self.type}:{tokens}"
    if len(dataTokens)>0:
      data+=f"\ndata:\n\t{dataTokens}"
    return data

def is_float(element):
  if element is None: 
      return False
  try:
      float(element)
      return True
  except ValueError:
      return False

def lexer(code):
  tokens = splitTokens(code)
  tokens = mergeTokens(tokens)
  return tokens

def splitTokens(code):
  tokens = []
  currentText = ""
  line = 1
  char = 1
  lastToken = None
  while len(code)>0:
    if code[0] == "\n":
      if (currentText != ""):
        tokens.append(getToken(currentText, line, char))
      tokens.append(getToken("newline", line, char+1))
      lastToken = tokens[-1]
      line += 1
      char = 1
      currentText = ''
    elif code[0] == " ":
      if (currentText != ""):
        tokens.append(getToken(currentText, line, char))
      tokens.append(getToken(" ", line, char+1))
      if (len(tokens)>0):
        lastToken = tokens[-1]
      char += 1
      currentText = ''
    elif (code[0] == "." and not currentText.isnumeric()) or code[0] in ["+", "-", "*", "/", "(", ")", ",", "[", "]", "{","}",'"',"'",';'] or ((code[0] in ["<",">","!", "="]) and (len(code)<=1 or code[1] in "=")):
      if (currentText != ""):
        tokens.append(getToken(currentText, line, char))
      tokens.append(getToken(code[0], line, char+1))
      lastToken = tokens[-1]
      char += 1
      currentText = ''
    elif (len(currentText) > 0 and (currentText[-1]+code[0]) in ["==", "!=", ">=", "<=", "&&", "||"]):
      if (currentText != ""):
        tokens.append(getToken(currentText[:-1], line, char))
      tokens.append(getToken(currentText[-1]+code[0], line, char+1))
      lastToken = tokens[-1]
      char += 2
      currentText = ''
    else:
      currentText += code[0]
      char += 1
    code = code[1:]
  if (currentText != ""):
    tokens.append(getToken(currentText, line, char))
    lastToken = tokens[-1]
  return tokens

def isToken(text):
  if (text):
    try:
      getToken(text, 0, 0)
      return True
    except LexerError:
      return False
  return False

def getToken(text, line, rchar):
  char = rchar-len(text)
  match text:
    case " ":
      return Token("SPACE", text, line, char)
    case ".":
      return Token("DOT", text, line, char)
    case "#include":
      return Token("INCLUDE", text, line, char)
    #case "print":
      return Token("PRINT", text, line, char)
    case "if":
      return Token("IF", text, line, char)
    case "else":
      return Token("ELSE", text, line, char)
    case "for":
      return Token("FOR", text, line, char)
    case "while":
      return Token("WHILE", text, line, char)
    case "function":
      return Token("DEF", text, line, char)
    case "end":
      return Token("END", text, line, char)
    case "return":
      return Token("RETURN", text, line, char)
    case "true":
      return Token("TRUE", text, line, char)
    case "false":
      return Token("FALSE", text, line, char)
    case "null":
      return Token("NULL", text, line, char)
    case "&&":
      return Token("AND", text, line, char)
    case "||":
      return Token("OR", text, line, char)
    case "!":
      return Token("NOT", text, line, char)
    case "==":
      return Token("EQUALS", text, line, char)
    case "!=":
      return Token("NOT_EQUALS", text, line, char)
    case "<":
      return Token("LESS_THAN", text, line, char)
    case ">":
      return Token("GREATER_THAN", text, line, char)
    case "<=":
      return Token("LESS_THAN_EQUALS", text, line, char)
    case ">=":
      return Token("GREATER_THAN_EQUALS", text, line, char)
    case "+":
      return Token("PLUS", text, line, char)
    case "-":
      return Token("MINUS", text, line, char)
    case "*":
      return Token("MULTIPLY", text, line, char)
    case "/":
      return Token("DIVIDE", text, line, char)
    case "%":
      return Token("MODULUS", text, line, char)
    case "(":
      return Token("LPAREN", text, line, char)
    case ")":
      return Token("RPAREN", text, line, char)
    case "[":
      return Token("LBRACKET", text, line, char)
    case "]":
      return Token("RBRACKET", text, line, char)
    case "{":
      return Token("LBRACE", text, line, char)
    case "}":
      return Token("RBRACE", text, line, char)
    case "=":
      return Token("ASSIGN", text, line, char)
    case ";":
      return Token("SEMICOLON", text, line, char)
    case "public":
      return Token("PUBLIC", text, line, char)
    case "private":
      return Token("PRIVATE", text, line, char)
    case "static":
      return Token("STATIC", text, line, char)
    case "class":
      return Token("CLASS", text, line, char)
    case "void":
      return Token("VOID", text, line, char)
    case "newline":
      return Token("NEWLINE", text, line, rchar-1)
    case "int":
      return Token("INTTYPE", text, line, char)
    case "string":
      return Token("STRINGTYPE", text, line, char)
    case "float":
      return Token("FLOATTYPE", text, line, char)
    case ",":
      return Token("COMMA", text, line, char)
    case "endprogram":
      return Token("ENDPROGRAM", text, line, char)
    case '"':
      return Token("DOUBLEQUOTE", text, line, char)
    case "'":
      return Token("SINGLEQUOTE", text, line, char)
    case "var":
      return Token("VAR", text, line, char)
    case "...":
      return Token("ARGLIST", text, line, char)
    case "extends":
      return Token("EXTENDS", text, line, char)
    case "implements":
      return Toekn("IMPLEMENTS", text, line, char)
    case "interface":
      return Token("INTERFACE", text, line, char)
    case "super":
      return Token("SUPER", text, line, char)
    case "enum":
      return Token("ENUM", text, line, char)
    case "new":
      return Token("NEW", text, line, char)
    case "<<":
      return Token("INSERT", text, line, char)
    case _:
      if (text.isnumeric()):
        return Token("INTEGER", text, line, char)
      elif (is_float(text)):
        return Token("FLOAT", text, line, char)
      elif (len(text)>0):
        return Token("IDENTIFIER", text, line, char)
      else: 
        raise LexerError(f"Unknown token: {text}, at line:{line}, char:{char}")
      
def mergeTokens(tokens):
  mergedTokens = []
  while len(tokens)>0:
    print(tokens[0])
    if (tokens[0].type == "DOUBLEQUOTE"):
      text = ""
      tokens = tokens[1:]
      while len(tokens)>0 and tokens[0].type != "DOUBLEQUOTE":
        text+=tokens[0].value
        #print(tokens[0].type)
        tokens = tokens[1:]
      if (len(tokens)>0 and tokens[0].type == "DOUBLEQUOTE"):
        tokens = tokens[1:]
      mergedTokens.append(TokenCombinations("STRING", text))
    elif (tokens[0].type == "SPACE"):
      tokens = tokens[1:]
    elif (tokens[0].type == "LESS_THAN"):
      if (len(tokens)>1 and tokens[1].type == "LESS_THAN"):
        mergedTokens.append(Token("LESS_THAN", "<<", tokens[0].line, tokens[0].char))
        tokens=tokens[2:]
      else:
        mergedTokens.append(tokens[0])
        tokens = tokens[1:]
    else:
      mergedTokens.append(tokens[0])
      tokens = tokens[1:]
  return mergedTokens

def parser(tokens):
  
  combinations = parserPass1(tokens)

  combinations = parserPass2(combinations)
  combinations = parseFunctionCall(combinations)
  combinations = parseFunctionDef(combinations)
  combinations = parseClassDef(combinations)
  return orderOfOperations(combinations)

def parserPass1(tokens):
  combinations = []
  while len(tokens)>0 and tokens[0].type != "ENDPROGRAM":
    tokenList = []
    if tokens[0].type == "IDENTIFIER":
      tokenList.append(tokens[0])
      tokens = tokens[1:]
      while len(tokens)>0 and (tokens[0].type == "IDENTIFIER" or tokens[0].type == "DOT"):
        if tokens[0].type != tokenList[-1].type:
          tokenList.append(tokens[0])
          tokens = tokens[1:]
        else:
          break;
      if tokenList[-1].type == "DOT":
        raise ParserError("Unexpected token: " + tokenList[-1])
      combinations.append(TokenCombinations("IDENTIFIER", tokenList))
      tokenList = []
    elif tokens[0].type == "DOT":
      if len(tokens)>=3:
        if tokens[1].type == "DOT" and tokens[2].type == "DOT":
          tokens=tokens[3:]
          combinations.append(TokenCombinations("ARGLIST", tokens))
    else:
      combinations.append(tokens[0])
      tokens = tokens[1:]
  return combinations

def parserPass2(tokens):
  combinations = []
  while len(tokens)>0 and tokens[0].type != "ENDPROGRAM":
    tokenList = []
    if tokens[0].type == "INCLUDE":
      tokenList.append(tokens[0])
      tokens = tokens[1:]
      while len(tokens)>0 and tokens[0].type != "NEWLINE":
        tokenList.append(tokens[0])
        tokens = tokens[1:]
      """
      if (len(tokens) == 0):
        raise ParserError("Expected file name")
      if tokens[0].type == "IDENTIFIER":
        tokenList.append(tokens[0])
        tokens = tokens[1:]
      #printTokens(tokenList)
      #print(tokenList[-1].type)
      if (tokenList[-1].type != "IDENTIFIER"):
        raise ParserError("Last token must be an identifier for include statement")
      if (tokens[0].type != "NEWLINE" and tokens[1].type != "NEWLINE"):
        raise ParserError("Expected newline after include")
      """
      combinations.append(TokenCombinations("INCLUDE", tokenList))
    else:
      combinations.append(tokens[0])
      tokens = tokens[1:]
  return combinations

def parseFunctionCall(tokens):
  
  #printTokens(tokens)
  comb = []
  while len(tokens)>0:
    tokenList = []
    if len(tokens)>1 and (tokens[0].type == "IDENTIFIER" or (tokens[0].type in "STRINGTYPE" and tokens[1].type == "LPAREN")):
      if tokens[0].type != "IDENTIFIER":
        tokens[0] = TokenCombinations("IDENTIFIER", [Token("IDENTIFIER", tokens[0].value, tokens[0].line, tokens[0].char)])
      if tokens[1].type == "LPAREN":
        tokenList.append(tokens[0])
        tokenList.append(tokens[1])
        functionTokens = []
        tokens = tokens[2:]
        level = 1
        while len(tokens)>0 and level>0:
          if (tokens[0].type == "LPAREN"):
            level+=1
          if (tokens[0].type == "RPAREN"):
            level-=1
          if level>0:
            functionTokens.append(tokens[0])
          tokenList.append(tokens[0])
          tokens = tokens[1:]
        if (len(tokens) > 0):
          if (tokenList[-1].type == "RPAREN"):
            functionTokens = parseFunctionCall(functionTokens)
          else:
            raise ParserError("Expected closing parenthesis")
        comb.append(TokenCombinations("FUNCTION", tokenList, functionTokens))
      else:
        comb.append(tokens[0])
        tokens = tokens[1:]
    else:
      comb.append(tokens[0])
      tokens = tokens[1:]
  return comb

def parseFunctionDef(tokens):
  comb = []
  while len(tokens)>0:
    if tokens[0].type == "DEF":
      tokenList = []
      token = [tokens[0], tokens[1]]
      if len(tokens) > 1:
        if tokens[1].type == "FUNCTION":
          tokens = tokens[2:]
          level = 1
          while len(tokens)>0 and level > 0:
            if (tokens[0].type in ["DEF", "FOR", "WHILE", "IF", "ELSE"]):
              level+=1
            elif (tokens[0].type == "END"):
              level-=1;
            tokenList.append(tokens[0])
            token.append(tokens[0])
            tokens = tokens[1:]
        else:
          raise ParserError("Expected function name")
        comb.append(TokenCombinations("FUNCTIONDEF", token, tokenList))
    else:
      comb.append(tokens[0])
      tokens = tokens[1:]
  return comb

def parseClassDef(tokens):
  comb = []
  while len(tokens)>0:
    if tokens[0].type == "CLASS":
      tokenList = []
      token = [tokens[0], tokens[1]]
      if len(tokens) > 1:
        if tokens[1].type == "IDENTIFIER":
          tokens = tokens[2:]
          level = 1
          while len(tokens)>0 and level > 0:
            if (tokens[0].type in ["DEF", "FOR", "WHILE", "IF", "ELSE", "RETURN"]):
              level+=1
            elif (tokens[0].type == "END"):
              level-=1;
            tokenList.append(tokens[0])
            token.append(tokens[0])
            tokens = tokens[1:]
        else:
          raise ParserError("Expected class name")
        comb.append(TokenCombinations("CLASS", token, tokenList))
    else:
      comb.append(tokens[0])
      tokens = tokens[1:]
  return comb

def orderOfOperations(tokens):
  for i in range(len(tokens)):
    if (tokens[i].type == "FUNCTION"):
      tokens[i].data = orderOfOperations(tokens[i].data)
    if (tokens[i].type == "FUNCTIONDEF"):
      tokens[i].data = orderOfOperations(tokens[i].data)
    if (tokens[i].type == "CLASS"):
      tokens[i].data = orderOfOperations(tokens[i].data)
  tokens = mathOrder(tokens)
  tokens = booleanOrder(tokens)
  tokens = assignmentParser(tokens)
  return tokens


def booleanOrder(tokens):

  tokens = booleanOrderNotCheck(tokens)
  tokens = booleanOrderHelper(tokens, ["EQUALS", "NOT_EQUALS", "LESS_THAN", "GREATER_THAN", "LESS_THAN_EQUALS", "GREATER_THAN_EQUALS"])
  tokens = booleanOrderHelper(tokens, ["AND", "OR"])
  return tokens

def booleanOrderHelper(tokens, checks):
  for i in range(len(tokens)):
    if (i>0 and i<len(tokens)-1):
      if tokens[i].type in checks:
        second = tokens.pop(i+1)
        first = tokens.pop(i-1)
        i-=1
        tokens[i] = TokenCombinations(tokens[i].type, [first, second])
        
  return tokens

def booleanOrderNotCheck(tokens):
  for i in range(len(tokens)):
    if i<len(tokens)-1:
      if tokens[i].type == "NOT":
        val = tokens.pop(i+1)
        tokens[i] = TokenCombinations("NOT", val)
  return tokens

def mathOrder(tokens):
  for i in range(len(tokens)):
    if (i>0 and i<len(tokens)-1):
      if (tokens[i].type == "MULTIPLY" or tokens[i].type == "DIVIDE"):
        if (tokens[i].type == "MULTIPLY"):
          second = tokens.pop(i+1)
          first = tokens.pop(i-1)
          i-=1
          tokens[i] = TokenCombinations("MULTIPLY", [first, second])
        else:
          second = tokens.pop(i+1)
          first = tokens.pop(i-1)
          i-=1
          tokens[i] = TokenCombinations("DIVIDE", [first, second])
  for i in range(len(tokens)):
    if (i>0 and i<len(tokens)-1):
      if (tokens[i].type == "PLUS" or tokens[i].type == "SUBTRACT"):
        if (tokens[i].type == "PLUS"):
          second = tokens.pop(i+1)
          first = tokens.pop(i-1)
          i-=1
          tokens[i] = TokenCombinations("PLUS", [first, second])
        else:
          second = tokens.pop(i+1)
          first = tokens.pop(i-1)
          i-=1
          tokens[i] = TokenCombinations("SUBTRACT", [first, second])
  return tokens

def assignmentParser(tokens):
  comb = []
  while len(tokens)>0:
    if (tokens[0].type == "VAR"):
      tokenList = []
      while len(tokens)>0 and (tokens[0].type not in ["NEWLINE"]):
        tokenList.append(tokens[0])
        tokens = tokens[1:]
      comb.append(TokenCombinations("VARCREATION", tokenList))
    else:
      comb.append(tokens[0])
      tokens = tokens[1:]
  return comb

def printTokens(tokens):
  for token in tokens:
    print(token)
    if (token.type == "NEWLINE"):
      print()

def compile(tokens, level=0):
  #print(tokens)
  code = ""
  for i in range(len(tokens)):
    token = tokens[i]
    match token.type:
      case "IDENTIFIER":
        code += "".join([t.value for t in token.tokens])
        if (i<len(tokens)-1 and tokens[i+1].type in ["STRINGTYPE", "INTTYPE", "FLOATTYPE", "IDENTIFIER", "ASSIGN", "FUNCTION", "INSERT"]):
          code += " ";
      case "INCLUDE":
        #print(token.tokens)
        val = compile(token.tokens[1:])
        #val = "".join([t.value for t in token.tokens[-1].tokens])
        data = f"#include {val}"
        code += data
      case "NEWLINE":
        code+="\n"
        code += "\t"*level
      case "FUNCTION":
        param = compile(token.data)
        name = "".join([t.value for t in token.tokens[0].tokens])
        code += name+"("+param+")"
      case "INTEGER":
        code += token.value
      case "PLUS":
        code += compile([token.tokens[0]])+"+"+compile([token.tokens[1]])
      case "SUBTRACT":
        code += compile([token.tokens[0]])+"-"+compile([token.tokens[1]])
      case "MULTIPLY":
        #print(token)
        code += compile([token.tokens[0]])+"*"+compile([token.tokens[1]])
      case "DIVIDE":
        code += compile([token.tokens[0]])+"/"+compile([token.tokens[1]])
      case "FUNCTIONDEF":
        code += f"{compile([token.tokens[1]])}{{"
        code += compile(token.data, level+1)
        code = code[:-1]+"}"
      case "CLASS":
        #print(token)
        code += f"class {compile([token.tokens[1]])}{{"
        code += compile(token.data, level+1)
        code = code[:-1]+"}"
      case "COMMA":
        code += ","
      case "STRING":
        code += '"'+token.tokens+'"'
      case "DOT":
        code += '.'
      case "ASSIGN":
        code += '= '
      case "PUBLIC":
        code += "public "
      case "PRIVATE":
        code += "private "
      case "STATIC":
        code += "static "
      case "VOID":
        code += "void "
      case "INTTYPE":
        code += "int "
      case "FLOATTYPE":
        code += "double "
      case "RPAREN":
        code += ")"
      case "LPAREN":
        code += "("
      case "DOUBLEQUOTE":
        code+='"'
      case "STRINGTYPE":
        code+="string "
      case "SEMICOLON":
        code+=";"
      case "ARGLIST":
        code = code[:-1]+"... "
      case "VARCREATION":
        code+=compile(token.tokens[1:], level)
      case "NEW":
        code+="new"
        if len(tokens)>1 and tokens[1].type in ["STRINGTYPE", "INTTYPE", "FLOATTYPE", "FUNCTION", "IDENTIFIER", "ASSIGN"]:
          code+=" "
      case "GREATER_THAN":
        try:
          code+=token.tokens[0].value+">"+token.tokens[1].value
        except Exception:
          code+=">"
      case "LESS_THAN":
        try:
          code+=token.tokens[0].value+"<"+token.tokens[1].value
        except Exception:
          code+="<"
      case "RETURN":
        code+="return "
      case "INSERT":
        code+="<< "
  return code

def checker(tokens):
  defaultTypes = ["INTTYPE", "FLOATTYPE", "STRINGTYPE", "BOOLEANTYPE"]
  customTypes = []
  for i in range(len(tokens)):
    token = tokens[i]
    if (token.type == "INCLUDE"):
      customTypes.append(token.tokens[1].tokens[-1].value)
    if (token.type == "CLASS"):
      customTypes.append(token.tokens[1].tokens[0].value)
  allTypes = defaultTypes + customTypes
  functions = findFunctions(tokens)
  #print("DefaultTypes:", defaultTypes)
  #print("CustomTypes:", customTypes)
  #print("Types:", allTypes)
  checkCode([defaultTypes, customTypes, allTypes], tokens)

def findFunctions(tokens, loc=[]):
  functions = []
  for i in range(len(tokens)):
    token = tokens[i]
    if (token.type == "FUNCTIONDEF"):
      functions+=findFunctions(token.data, loc+[token])
      functions.append([token, loc])
    if (token.type == "CLASS"):
      functions+=findFunctions(token.data, loc+[token])
  return functions

def checkCode(types, tokens):
  for i in range(len(tokens)):
    if (tokens[i].type == "FUNCTION"):
      checkCode(types, tokens[i].data)
    elif (tokens[i].type == "FUNCTIONDEF"):
      checkCode(types, tokens[i].data)
    elif (tokens[i].type == "CLASS"):
      checkCode(types, tokens[i].data)
  firstCheck(types, tokens)


def firstCheck(types, tokens):
  defaultTypes = types[0]
  customTypes = types[1]
  allTypes = types[2]
  types = defaultTypes+["IDENTIFIER"]
  for i in range(len(tokens)):
    token = tokens[i]
    if (token.type == "VARCREATION"):
      if (token.tokens[1].type not in types):
        raise TypeError("Type " + token.tokens[1].type + " is not defined")
      else:
        if (token.tokens[1].type == "IDENTIFIER" and token.tokens[1].tokens[0].value not in customTypes):
          raise TypeError("Type " + token.tokens[1].tokens[0].value + " is not defined")
    if (token.type == "FUNCTIONDEF" and i>0):
      if not (tokens[i-1].type in types or tokens[i-1].type == "VOID"):
        raise TypeError("Type " + tokens[i-1].type + " is not defined")
      else:
        if (tokens[i-1].type == "IDENTIFIER" and tokens[i-1].tokens[0].value not in customTypes):
          raise TypeError("Type " + tokens[i-1].tokens[0].value + " is not defined")
          


def main():
  print("Starting to compile")
  code = open("test.txt", "r").read()
  
  tokens = lexer(code)
  
  printTokens(tokens)
  print("\n\n\n")
  
  combinations = parser(tokens)
  
  for i in combinations:
    print(str(i)+"\n")

  #checker(combinations)
  
  result = compile(combinations)
  open("test.cpp", "w").write(result)

debugMode = True


try:
  main()
except Exception as e:
  if debugMode:
    raise e
  print(e)