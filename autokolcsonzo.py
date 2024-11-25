from abc import ABC, abstractmethod


# Auto (absztrakt osztály)
class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.foglalt = False

    @abstractmethod
    def display_info(self):
        pass


# Személyautó osztály
class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ulesek_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ulesek_szama = ulesek_szama

    def display_info(self):
        return (f"Személyautó: Rendszám: {self.rendszam}, Típus: {self.tipus}, "
                f"Bérleti díj: {self.berleti_dij} Ft/nap, Ülések száma: {self.ulesek_szama}")


# Teherautó osztály
class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def display_info(self):
        return (f"Teherautó: Rendszám: {self.rendszam}, Típus: {self.tipus}, "
                f"Bérleti díj: {self.berleti_dij} Ft/nap, Teherbírás: {self.teherbiras} kg")


# Berles osztály
class Berles:
    def __init__(self, auto, ugyfel_nev, napok_szama):
        if auto.foglalt:
            raise ValueError("Az autó már foglalt!")
        self.auto = auto
        self.ugyfel_nev = ugyfel_nev
        self.napok_szama = napok_szama
        self.koltseg = auto.berleti_dij * napok_szama
        auto.foglalt = True

    def visszaadas(self):
        self.auto.foglalt = False

    def display_info(self):
        return (f"Bérlés: Ügyfél: {self.ugyfel_nev}, Autó: {self.auto.rendszam}, "
                f"Napok száma: {self.napok_szama}, Összköltség: {self.koltseg} Ft")


# Autokolcsonzo osztály
class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadas(self, auto):
        self.autok.append(auto)

    def autok_listazasa(self):
        return [auto.display_info() for auto in self.autok]

    def elerheto_autok(self):
        return [auto for auto in self.autok if not auto.foglalt]

    def auto_berles(self, rendszam, ugyfel_nev, napok_szama):
        auto = next((auto for auto in self.elerheto_autok() if auto.rendszam == rendszam), None)
        if not auto:
            return f"Az autó {rendszam} rendszámmal nem elérhető!"
        berles = Berles(auto, ugyfel_nev, napok_szama)
        self.berlesek.append(berles)
        return f"Bérlés sikeres! Ára: {berles.koltseg} Ft"

    def berles_lemondasa(self, rendszam, ugyfel_nev):
        berles = next((b for b in self.berlesek if b.auto.rendszam == rendszam and b.ugyfel_nev == ugyfel_nev), None)
        if not berles:
            return f"Nincs ilyen bérlés: {rendszam} - {ugyfel_nev}!"
        berles.visszaadas()
        self.berlesek.remove(berles)
        return f"Bérlés lemondva: {rendszam} - {ugyfel_nev}!"

    def berlesek_listazasa(self):
        if not self.berlesek:
            return "Nincs aktív bérlés."
        return [berles.display_info() for berles in self.berlesek]


# Inicializálás
def inicializalas():
    kolcsonzo = Autokolcsonzo("DreamCars")
    auto1 = Szemelyauto("ABC-123", "Toyota Corolla", 10000, 5)
    auto2 = Szemelyauto("DEF-456", "Honda Civic", 12000, 5)
    auto3 = Teherauto("GHI-789", "Ford Transit", 15000, 1000)
    kolcsonzo.auto_hozzaadas(auto1)
    kolcsonzo.auto_hozzaadas(auto2)
    kolcsonzo.auto_hozzaadas(auto3)
    kolcsonzo.berlesek.append(Berles(auto1, "Kiss János", 3))
    kolcsonzo.berlesek.append(Berles(auto2, "Nagy Éva", 5))
    kolcsonzo.berlesek.append(Berles(auto3, "Szabó Péter", 1))
    return kolcsonzo


# Felhasználói interfész
def menu():
    kolcsonzo = inicializalas()
    while True:
        print("\n=== Autókölcsönző rendszer ===")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Aktuális bérlések listázása")
        print("4. Kilépés")

        valasztas = input("Válassz egy opciót (1-4): ")

        if valasztas == "1":
            rendszam = input("Add meg a bérlendő autó rendszámát: ").upper()
            ugyfel_nev = input("Add meg az ügyfél nevét: ")
            try:
                napok_szama = int(input("Add meg a bérlés napjainak számát: "))
                print(kolcsonzo.auto_berles(rendszam, ugyfel_nev, napok_szama))
            except ValueError:
                print("Hiba: A napok számának egész számnak kell lennie!")

        elif valasztas == "2":
            rendszam = input("Add meg a lemondani kívánt bérlés rendszámát: ").upper()
            ugyfel_nev = input("Add meg az ügyfél nevét: ")
            print(kolcsonzo.berles_lemondasa(rendszam, ugyfel_nev))

        elif valasztas == "3":
            berlesek = kolcsonzo.berlesek_listazasa()
            if isinstance(berlesek, str):
                print(berlesek)
            else:
                for berles in berlesek:
                    print(berles)

        elif valasztas == "4":
            print("Kilépés a rendszerből. Viszlát!")
            break

        else:
            print("Hiba: Érvénytelen opció! Válassz 1-4 között.")


# Futtatás
if __name__ == "__main__":
    menu()
