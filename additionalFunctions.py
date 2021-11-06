import pandas as pd
from PIL import Image
import datetime
import time

# Operações possíveis
operations = ["0", "1", "2", "3", "4", "5", "6", "7"]

# Atributos de um cliente
clientAtt = ["name", "cpf", "password"]
# Atributos de um pedido
orderAtt = ["cpf", "date", "order", "history"]

# Dicionário com o menu
menuDict = {"1":{"produto":'x-salada', "preço":10},
            "2":{"produto":'x-burger', "preço":10},
            "3":{"produto":'cachorro quente', "preço":7.5},
            "4": {"produto":'misto quente', "preço":8},
            "5":{"produto":'salada de frutas', "preço":5.5},
            "6":{"produto":'refrigerante', "preço":4.5},
            "7":{"produto":'suco natural', "preço":6.25}}

# Função para o display do menu de opções --------------------
def optionsMenu():
    formatTitle("Bem vindo(a) ao BurgerFEI!")
    formatTitle("Menu de Opções")
    print("1 - Novo Pedido")
    print("2 - Cancela Pedido")
    print("3 - Insere Produto")
    print("4 - Cancela Produto")
    print("5 - Valor do Pedido")
    print("6 - Extrato do Pedido")
    print("\n0 - Sair")
    formatTitle("")
#-------------------------------------------------------------

# Funções para formatar/manipular String----------------------
def formatTitle(string):
    totalLength = 45
    stringLength = len(string)
    sidesLength = int((totalLength - stringLength)/2)
    print("-"*sidesLength + string + "-"*sidesLength)

def formatExtractLine(productQtd, productName, productPrice, totalPrice, operation):
    # transformar todas as variáveis em string para fazer manipulação de string
    productQtd = str(productQtd)
    productPrice = str("%.2f"%productPrice)
    totalPrice = str("%.2f"%totalPrice)
    textLimit = 17
    numberLimit = 5
    if (len(productQtd) <= 2):
        productQtd = (2 - len(productQtd))*" " + productQtd
    if (len(productName) <= textLimit):
        productName = productName + (textLimit - len(productName))*" "
    if (len(productPrice) <= numberLimit):
        productPrice = (numberLimit - len(productPrice))*" " + productPrice + 2*" "
    if (len(totalPrice) <= numberLimit):
        if (operation == "Added"):
            totalPrice = "+ " + (numberLimit - len(totalPrice))*" " + totalPrice
        elif (operation == "Removed"):
            totalPrice = "- " + (numberLimit - len(totalPrice))*" " + totalPrice + " - Cancelado"
    print("%s - %s - Preço unitário: %s Valor: %s" %(productQtd, productName, productPrice, totalPrice))
#-------------------------------------------------------------


# Funções para salvar informação do cliente e do pedido-------
def saveClientInfo(df, name, cpf, password):
    # Essa função é resnponsável por salvar os dados do cliente 
    # no arquivo clients.csv quando vai criar o pedido
    new_row = [name,cpf,password]
    new_df = pd.DataFrame([new_row], columns = clientAtt)
    df = pd.concat([df, new_df], ignore_index = True)
    df.to_csv("clients.csv", index=False)

def saveOrder(df, cpf, order, history):
    # Essa função salva as informações do pedido no arquivo orders.csv 
    # quando vai criar o pedido
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    new_row = [cpf,now,order, history]
    new_df = pd.DataFrame([new_row], columns = orderAtt)
    df = pd.concat([df, new_df], ignore_index = True)
    df.to_csv("orders.csv", index=False)
#-------------------------------------------------------------


# Função auxiliar para obter o código do produto, que é chave- 
# do menuDict, através do nome do produto --------------------
def getCodeKey(productName):
    # função criada para a partir do nome do produto conseguirmos obter o código
    for codeKey, prodInfo in menuDict.items():
        for key in prodInfo:
            if (productName == prodInfo[key]):
                return codeKey
#-------------------------------------------------------------


# Função para abrir a imagem num app de fotos do proprio sistema
def showMenuImage():
    # mostrar a imagem do menu
    img = Image.open("./menu.png")
    img.show()
#-------------------------------------------------------------


# Função para realizar adição de produtos em loop-------------
def addProductToOrder(): 
    # Essa função faz a adição de produtos ao pedido 
    order = {}
    history = [] # usamos lista para o histórioco porque dict não pode ter elementos com a mesma chave, ao tentar criar outro elemento com a 
                 # mesma chave apenas irá atualizar o valor do elemento já existente, portanto, o histórico de 
                 # operações será salvo numa lista
    total = 0
    # while(True) faz com que esse bloco sempre seja executado
    while(True):
        print("\nCaso queira finalizar o pedido inserir o número 0")
        productCode = str(input("Insira o código do produto: "))
        if (productCode not in menuDict):
            # caso o código inserido não pertencer ao dicionário do menu, é executado o comando break
            # que sai do loop infinito while(True)
            time.sleep(1)
            break
        else:
            productQtd = int(input("Quantidade do produto: "))
            preco = menuDict[productCode].get("preço")
            total += preco*productQtd

            # menuDict[productCode].get("produto") retorna o nome do produto que corresponde ao código inserido
            order[menuDict[productCode].get("produto")] = {} # dicionário dentro de um dicionário
            order[menuDict[productCode].get("produto")]["Quantidade"] = productQtd
            
            history.append([menuDict[productCode]["produto"] ,"Added", productQtd])

    order["Total"] = total

    return order, history
#-------------------------------------------------------------


# Funções para validar e verificar as informações forneceidas-
def verifyPassword(cpf, password):
    # Essa função verifica se a senha inserida corresponde ao cpf inserido
    df = pd.read_csv("clients.csv", usecols = clientAtt)
    # to_list() transforma uma coluna em uma lista, portanto, 
    # df.cpf.to_list() transforma a coluna dos cpf em lista
    cpfList = df.cpf.to_list()
    passwordList = df.password.to_list()
    
    index = cpfList.index(cpf)

    if(password == passwordList[index]):
        return True
    else:
        return False

def verifyOrderExistance(cpf):
    # Essa função verifica se o cpf inserido já existe no registro
    df = pd.read_csv("./clients.csv", usecols = clientAtt)
    cpf_list = df.cpf.to_list()

    if(cpf in cpf_list):
        return True
    else:
        return False
#-------------------------------------------------------------