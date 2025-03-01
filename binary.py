import io
from typing import BinaryIO

class BinaryFile:

    # Méthodes
    # Constructeur
    def __init__(self, file: BinaryIO):
        """
        Prends en paramètre un fichier binaire
        Classe permettant de lire un fichier binaire
        """
        self.file = file #stocke le fichier binaire

    def goto(self, pos: int) -> None:
        """
        Permet donc de parcourir le fichier binaire
        Déplace le fichier pointeur à la position pos
            IF pos est positif, le fichier pointeur est déplacé depuis le début du fichier
            IF pos est négatif, le fichier pointeur est déplacé depuis la fin du fichier
            
        """
        if pos >= 0:
            self.file.seek(pos, io.SEEK_SET) # Déplace depuis le début du fichier
        else:
            self.file.seek(pos, io.SEEK_END) # Déplace depuis la fin du fichier
        
    def get_size(self) -> int:
        """
        Get la taille du fichier en bytes 
        et permet de vérifier combien d'espace est utilisé
        """
        current = self.file.tell() # sauvegarde la position actuelle
        self.file.seek(0, io.SEEK_END) # se déplace à la fin du fichier
        size = self.file.tell() # récupère la taille du fichier
        self.file.seek(current) # retourne à la position actuelle
        return size
    
    # Méthodes qui permettent d'utiliser la classe BinaryFile pour écrire des données
    # Ces 4 méthodes doivent toutes renvoyer le nombre de bytes écrits dans le fichier
    def write_integer(self, n: int, size: int) -> int:
        """
        Ecrit un int dans le fichier binaire sous format little-endian
        n est un entier à écrire
        la taille est le nmbre de bytes a utiliser (ex: 4 pour un int de 32 bits)
        Retourne le nombre de bytes écrits
        """
        bytes_written = n.to_bytes(size, byteorder='little', signed=True)
        self.file.write(bytes_written)
        return size
    
    def write_integer_to(self, n: int, size: int, pos: int) -> int:
        """
        Ecrit un int a une position donnée dans le fichier binaire
        n est un entier à écrire
        la taille est le nmbre de bytes a utiliser (ex: 4 pour un int de 32 bits)
        pos est la position dans le fichier
        Retourne le nombre de bytes écrits
        """
        current = self.file.tell() # sauvegarde la position actuelle
        self.goto(pos) # se déplace à la position donnée
        bytes_written = self.write_intiger(n, size) # écrit l'entier
        self.file.seek(current) # retourne à la position actuelle
        return bytes_written
    
    def write_string(self, s: str) -> int:
        """
        Ecrit un str dans le fichier binaire
        s est le str à écrire
        Retourne le nombre de bytes écrits
        """
        encoded = s.encode('utf-8') # convertit le str en bytes
        length = len(encoded) # récupère la taille du str
        # écrit la longueur du str (2 bytes, little-endian)
        self.write_integer(length, 2)
        # écrit le str
        self.file.write(encoded)
        return length + 2 # retourne le nb total de bytes écrits
    
    def write_string_to(self, s: str, pos: int) -> int:
        """
        Ecrit un str à une position donnée dans le fichier binaire
        s est le str à écrire
        pos est la position dans le fichier
        Retourne le nombre de bytes écrits
        """
        current = self.file.tell() # sauvegarde la position actuelle
        self.goto(pos) # se déplace à la position donnée
        bytes_written = self.write_string(s) # écrit le str
        self.file.seek(current) # retourne à la position actuelle
        return bytes_written # retourne le nb total de bytes écrits
    
    # Méthodes pour pouvoir lire les valeurs écrites
    def read_intiger(self, size : int) -> int:
        """
        Lit un int depuis un fichier
        size est le nombre de bytes à lire
        Retourne le int lu
        """
        data = self.file.read(size) # lit les bytes
        return int.from_bytes(data, byteorder='little', signed=True) # convertit les bytes en int
    
    def read_intiger_from(self, size: int, pos: int) -> int:
        """
        Lit un int à une position donnée dans le fichier
        size est le nombre de bytes à lire
        pos est la position dans le fichier
        Retourne le int lu
        """
        current = self.file.tell() # sauvegarde la position actuelle
        self.goto(pos) # se déplace à la position donnée
        value = self.read_intiger(size) # lit l'entier
        self.file.seek(current) # retourne à la position actuelle
        return value # retourne l'entier

    def read_string(self) -> str:
        """
        Lit un str depuis un fichier
        Retourne le str lu
        """
        length = self.read_intiger(2) # lit la longueur du str (2 bytes)
        data = self.file.read(length) # lit le str
        return data.decode('utf-8') # convertit les bytes en str

    def read_string_from(self, pos: int) -> str:
        """
        Lit un str depuis une postion donnée dans le fichier
        pos est la position à lire depuis
        Retourne le str lu
        """
        current = self.file.tell() # sauvegarde la position actuelle
        self.goto(pos) # se déplace à la position donnée
        value = self.read_string() # lit le str
        self.file.seek(current) # retourne à la positiion de base
        return value
    

# Test de la classe BinaryFile
if __name__ == "__main__":
    with open("test.bon", "wb+") as file:
        binary_file = BinaryFile(file)
        binary_file.write_integer(42, 4) # écrit 42 dans le fichier (4 bytes)
        binary_file.write_string("Hello, World!") # écrit "Hello, World!" dans le fichier
        print(binary_file.read_intiger(4)) # doit afficher 42
        print(binary_file.read_string()) # doit afficher "Hello, World!"