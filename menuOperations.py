import ast
import pandas as pd
import datetime
import time
import additionalFunctions as AD

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

# Lista com nome dos produtos
productsList = ['x-salada','x-burger','cachorro quente','misto quente','salada de frutas','refrigerante','suco natural']

def switch(operation):
    # ganbiarra do comando switch case que existem em outras linguagens como C++ e Java
    # essa função recebe a operação de receiveOption e executa um dos camandos do menu dependendo do número
    if(operation == "1"): newOrder()
    elif(operation == "2"): cancelOrder()
    elif(operation == "3"): insertNewProduct()
    elif(operation == "4"): cancelProduct()
    elif(operation == "5"): orderPrice()
    elif(operation == "6"): printExtract()
    else: return operation

def receiveOption():
    # essa função pede para o usuário a operação que deseja fazer e retorna o número
    # o bloco while é responsável por verificar se o número inserido corresponde a uma das operações
    option = str(input("Escolha o número da operação desejada: "))
    while (option not in operations):
        print("Número inserido inválido !!!")
        option = str(input("Escolha o número da operação desejada: "))
    return option

def newOrder():           # finished
    print("")
    AD.formatTitle("Novo Pedido")
    cpf = int(input("CPF(apenas números): "))
    # Dataframe de clientes
    df = pd.read_csv("./clients.csv", usecols = clientAtt)
    # Dataframe de pedidos
    orderDf = pd.read_csv("./orders.csv", usecols = orderAtt)
    if(AD.verifyOrderExistance(cpf)):
        print("Esse cliente de CPF %s já possui pedido !" %cpf)
    else:
        name = str(input("Nome: "))
        password = str(input("Senha: "))
        AD.saveClientInfo(df,name,cpf,password)
        AD.showMenuImage()
        newOrder, history = AD.addProductToOrder()
        AD.saveOrder(orderDf, cpf, newOrder, history)
        print("\nPedido criado com sucesso !!!")
        print("Voltando para o menu ...", end="\n")

def cancelOrder():        # finished
    print("")
    AD.formatTitle("Cancelar Pedido")
    cpf = int(input("CPF(apenas números): "))

    if(AD.verifyOrderExistance(cpf)):
        password = str(input("Insira sua senha: "))
        while(not AD.verifyPassword(cpf, password)):
            print("\nA senha inseriada está incorreta !")
            password = str(input("Insira sua senha: "))

        # essa linha elimina a linha que contem o cpf inserido do dataframe
        clientsDf = pd.read_csv("clients.csv").set_index("cpf").drop(cpf, axis=0)
        # essa linha elimina a linha que contem o cpf inserido do dataframe
        ordersDf = pd.read_csv("orders.csv").set_index("cpf").drop(cpf, axis=0)

        clientsDf.to_csv("clients.csv") # salva o novo dataframe
        ordersDf.to_csv("orders.csv") # salva o novo dataframe
        print("\nO pedido do CPF %i foi cancelado !" %cpf)
        print("Volatando para o menu ...", end="\n")
    else:
        print("Esse CPF não possui pedido registrado !")

def insertNewProduct():   # finished
    print("")
    AD.formatTitle("Inserir Produto")
    cpf = int(input("CPF(apenas números): "))
    if(AD.verifyOrderExistance(cpf)):
        # Enquanto a senha inserida estiver errada o programa não executa os próximos passos
        password = str(input("Insira sua senha: "))
        while(not AD.verifyPassword(cpf, password)):
            print("\nA senha inseriada está incorreta !")
            password = str(input("Insira sua senha: "))
        updatedOrder = {}
        updatedHistory = []
        # creat a new dictionary with the products the client wants to add
        # and a new list to register new operations
        AD.showMenuImage()
        addToOrder, addToHistory = AD.addProductToOrder()
        df = pd.read_csv("orders.csv", usecols=orderAtt)
        # list of the cpf elements
        cpfList = df.cpf.to_list()
        # list of the order elements
        orderList = df.order.to_list()
        # list of the history elements
        historyList = df.history.to_list()
        # get the index of the entry CPF, that is the same of the order
        index = cpfList.index(cpf)

        currentOrder = ast.literal_eval(orderList[index])
        currentHistory = ast.literal_eval(historyList[index])
        # sum both dictionaries
        for key in productsList:
            # Se key estiver no novo pedido(addToOrder) adiciona ao histórico novo
            if (key in addToOrder):
                auxList = [key, "Added", addToOrder[key]["Quantidade"]]
                updatedHistory.append(auxList)
            
            # Se key pertencer tanto ao pedido novo como ao antigo é feito a soma das quantidades
            if ((key in addToOrder) and (key in currentOrder)):
                updatedOrder[key] = {}
                updatedOrder[key]["Quantidade"] = currentOrder[key]["Quantidade"] + addToOrder[key]["Quantidade"]
            
            # Se key pertencer apenas ao pedido antigo, a quantidade nova é igual a quantidade do pedido antigo
            elif ((key not in addToOrder) and (key in currentOrder)):
                updatedOrder[key] = {}
                updatedOrder[key]["Quantidade"] = currentOrder[key]["Quantidade"]

            # Se key pertencer apenas ao pedido novo, a quantidade nova é igual a quantidade do pedido novo
            elif ((key in addToOrder) and (key not in currentOrder)):
                updatedOrder[key] = {}
                updatedOrder[key]["Quantidade"] = addToOrder[key]["Quantidade"]

            # Se key não pertencer a nenhum pedido, pula
            else:
                pass
        
        # percorre as operações novas e as adiciona ao histórico antigo
        for item in addToHistory:
            currentHistory.append(item)

        updatedOrder["Total"] = addToOrder["Total"] + currentOrder["Total"]
        # update as colunas do dataframe
        df.at[index, "date"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        df.at[index, "order"] = updatedOrder
        df.at[index, "history"] = currentHistory
        # salva o dataframe
        df.to_csv("orders.csv", index = False)
        print("\nProdutos adicionados com sucesso !")
        print("Voltando para o menu ...", end="\n")
    else:
        print("Esse CPF não possui pedido registrado !")

def cancelProduct():      # finished
    print("")
    AD.formatTitle("Cancelar Produto")
    cpf = int(input("CPF(apenas números): "))
    if (AD.verifyOrderExistance(cpf)):
        password = str(input("Insira sua senha: "))
        while(not AD.verifyPassword(cpf, password)):
            print("\nA senha inseriada está incorreta !")
            password = str(input("Insira sua senha: "))
        while(True):
            print("\nCaso queira finalizar a operação inserir o número 0")
            productCode = str(input("Insira o código do produto: "))
            df = pd.read_csv("orders.csv", usecols = orderAtt)
            # Attributes Lists
            cpfList = df.cpf.to_list()
            orderList = df.order.to_list()
            historyList = df.history.to_list()
            index = cpfList.index(cpf)
            currentOrder = ast.literal_eval(orderList[index])
            currentHistory = ast.literal_eval(historyList[index])
            if(productCode not in menuDict):
                print("")
                print("Voltando para o menu ...")
                time.sleep(1)
                break
            elif(menuDict[productCode].get("produto") not in currentOrder):
                print("Esse produto não consta no pedido.")
                break
            else:
                productName = menuDict[productCode]["produto"]
                productQtd = int(input("Quantidade: "))
                currentOrder[productName]["Quantidade"] -= productQtd
                # caso a quantidade do produto depois do cancelamento for menor que zero, 
                # remover do dict com .pop()
                if(currentOrder[productName]["Quantidade"] <= 0):
                    currentOrder.pop(productName)
                currentOrder["Total"] -= menuDict[productCode]["preço"]*productQtd
                auxList = [productName, "Removed", productQtd]
                currentHistory.append(auxList)
                df.at[index, "date"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                df.at[index, "order"] = currentOrder
                df.at[index, "history"] = currentHistory
                df.to_csv("orders.csv", index = False)
                print("\nO produto foi cancelado com sucesso !!!")
                print("Voltando para o menu ...", end="\n")
    else:
        print("Esse CPF não possui pedido registrado !")

def orderPrice():         # finished
    print("")
    AD.formatTitle("Preço do Pedido")
    cpf = int(input("CPF(apenas números): "))
    if (AD.verifyOrderExistance(cpf)):
        password = str(input("Insira sua senha: "))
        while(not AD.verifyPassword(cpf, password)):
            print("\nA senha inseriada está incorreta !")
            password = str(input("Insira sua senha: "))
        df = pd.read_csv("orders.csv", usecols = orderAtt)
        orderList = df.order.to_list()
        index = df.cpf.to_list().index(cpf)
        currentOrder = ast.literal_eval(orderList[index])
        print("O total de seu pedido é R$ %.2f" %currentOrder["Total"])
    else:
        print("Esse CPF não possui pedido registrado !")

def printExtract():       # finished
    print("")
    AD.formatTitle("Imprimir Extrado")
    cpf = int(input("CPF(apenas números): "))
    if (AD.verifyOrderExistance(cpf)):
        password = str(input("Insira sua senha: "))
        while(not AD.verifyPassword(cpf, password)):
            print("\nA senha inseriada está incorreta !")
            password = str(input("Insira sua senha: "))
        dfClients = pd.read_csv("clients.csv", usecols = clientAtt)
        dfOrder = pd.read_csv("orders.csv", usecols = orderAtt)
        # transforma a coluna CPF em index do dataframe
        dfClients.set_index("cpf", inplace = True)
        dfOrder.set_index("cpf", inplace = True)
        # pega o nome do cliente
        clientName = dfClients.loc[cpf]['name']
        # pega o pedido
        # nesse caso ast.literal_eval() transforma string em dict
        order = ast.literal_eval(dfOrder.loc[cpf]["order"])
        orderPrice = order["Total"]
        # nesse caso ast.literal_eval() transforma string em lista
        historyOperations = ast.literal_eval(dfOrder.loc[cpf]["history"])

        print("\nNome: %s" %clientName)
        print("CPF: %i" %cpf)
        print("Total: R$ %.2f" %orderPrice)
        print("Data: %s" %dfOrder.loc[cpf]["date"])
        print("Itens pedidos: ")
        for operation in historyOperations:
            productName = operation[0]
            productOperation = operation[1]
            productQtd = operation[2]
            productCode = AD.getCodeKey(productName)
            # get product code from product name
            productPrice = float(menuDict[productCode]["preço"])
            
            AD.formatExtractLine(productQtd, productName, productPrice,
                                 productPrice*productQtd, productOperation)
        
    else:
        print("Esse CPF não possui pedido registrado !") 