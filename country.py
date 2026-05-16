import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class Country:
    """Representa un país con sus datos de la API Rest Countries."""
    
    def __init__(self, data: dict):
        self.name = data.get("name", {}).get("common", "N/A")
        self.capital = data.get("capital", ["N/A"])[0] if data.get("capital") else "N/A"
        self.population = data.get("population", 0)
        self.area = data.get("area", 0.0)
        self.region = data.get("region", "N/A")
        self.flag = data.get("flag", "")
    
    def __str__(self) -> str:
        return (
            f"{self.flag} {self.name}\n"
            f"  Capital: {self.capital}\n"
            f"  Población: {self.population:,}\n"
            f"  Área: {self.area:,.2f} km²\n"
            f"  Región: {self.region}"
        )
    
    def density(self) -> float:
        if self.area == 0:
            return 0.0
        return round(self.population / self.area, 2)
    
    def comparar(self, otros: list) -> None:
        paises = [self] + otros
        
        print("\n" + "=" * 100)
        print(f"{'País':<20} {'Población':<15} {'Área (km²)':<15} {'Densidad (hab/km²)':<20}")
        print("=" * 100)
        
        for p in paises:
            print(f"{p.name:<20} {p.population:>14,} {p.area:>14,.0f} {p.density():>19.2f}")
        
        print("=" * 100)
        
        mayor_poblacion = max(paises, key=lambda p: p.population)
        mayor_area = max(paises, key=lambda p: p.area)
        mayor_densidad = max(paises, key=lambda p: p.density())
        
        print(f"\nMayor población : {mayor_poblacion.name}")
        print(f"Mayor área      : {mayor_area.name}")
        print(f"Mayor densidad  : {mayor_densidad.name}")
        print()


class CountryAPI:
    """Encapsula todas las requests a la API Rest Countries."""

    BASE_URL = "https://restcountries.com/v3.1"

    def by_name(self, name: str) -> Country:
        """Busca un país por nombre y devuelve un objeto Country."""
        try:
            url = f"{self.BASE_URL}/name/{name}?fullText=true"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return Country(data[0])
        except Exception:
            try:
                url = f"{self.BASE_URL}/name/{name}"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                return Country(data[0])
            except Exception as e:
                print(f"Error buscando '{name}': {e}")
                return None

    def by_names(self, names: list) -> list:
        """
        Busca varios países en paralelo usando concurrencia.
        Todos los requests se lanzan al mismo tiempo — mucho más rápido.

        Args:
            names: Lista de nombres de países en inglés

        Returns:
            list[Country] en el mismo orden que la lista de entrada
        """
        results = {}

        with ThreadPoolExecutor(max_workers=len(names)) as executor:
            futures = {executor.submit(self.by_name, name): name for name in names}

            for future in as_completed(futures):
                name = futures[future]
                try:
                    results[name] = future.result()
                except Exception as e:
                    print(f"Error con '{name}': {e}")
                    results[name] = None

        return [results.get(name) for name in names]

    def by_region(self, region: str) -> list:
        """Devuelve una lista de objetos Country de una región."""
        try:
            url = f"{self.BASE_URL}/region/{region}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [Country(p) for p in data]
        except Exception as e:
            print(f"Error buscando región '{region}': {e}")
            return []