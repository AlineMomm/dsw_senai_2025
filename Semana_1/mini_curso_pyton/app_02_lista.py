frutas =["maçã","banana","laranja"]
#          0,      1,        2
print(frutas)

print(frutas[1])

frutas[1] = "Abacaxi"
print(frutas)


print("LOOP FOR:")
for fruta in frutas:
    print(fruta)

print("REMOVER 'LARANJA':")
frutas.remove("laranja")
print(frutas)