import time
import additionalFunctions as AD
import menuOperations as MO

def main():
    while(True):
        print("")
        AD.optionsMenu()
        operation = MO.receiveOption()
        if (operation == "0"):
            # se o cliente inserir "0" encerra o programa
            break
        else:
            MO.switch(operation)
            # time.sleep foi usado para gerar um delay na repetição do loop, para que 
            # o cliente tenha tempo de analisar a mensagem
            time.sleep(2)
main()
