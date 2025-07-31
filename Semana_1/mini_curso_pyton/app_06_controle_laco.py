# CPNTROLE DE FLUXO

# Não imprime o número 3
for numero in range(1,11):
    if numero == 3:
        continue    # é um salto


    if numero == 8:
        break   # encerra a execução do loop
    print(numero)