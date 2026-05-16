from country import CountryAPI

api = CountryAPI()

# HEISSER: H, E, I, S, S, E, R
# RAMIRO: R, A, M, I, R, O
heisser = ["hungary", "egypt", "iceland", "sweden", "slovakia", "ethiopia", "romania"]
ramiro  = ["russia", "argentina", "mexico", "indonesia", "rwanda", "oman"]

print("Buscando paises en paralelo...\n")
paises = api.by_names(heisser + ramiro)
paises = [p for p in paises if p]

for p in paises:
    print(p)
    print()

paises[0].comparar(paises[1:])