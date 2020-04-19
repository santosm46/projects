def descobrePrimos(procurarAte):
    # declarando variáveis e funções
    
    primos = [2]

    def temDivisivel(valor):
        for aux in primos:
            if((valor % aux) == 0):
                return True
        return False

    ## verifica se o número é válido, retorna o número se válido, None se inválido
    def numeroValido(numero):
        if(not numero.isnumeric()):
            print('Erro! Digite apenas números')
            return None
        numero = int(numero)
        
        if(numero < 2):
            print('Erro! Digite um número maior que um')
            return None
        return numero
    
    # processo
    procurarAte = numeroValido(procurarAte)
    if(procurarAte is None):
        exit(0)
    
    for numero in range(3, procurarAte+1):
        if(not temDivisivel(numero)):
            primos.append(numero)

    return primos

# execução (main)
procurarAte = input('Até que número deseja procurar números primos? ')
primos = descobrePrimos(procurarAte)
print('\nEsta é a lista de números primos até {}'.format(procurarAte))
print(primos)
