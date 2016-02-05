"""
SVL 2015-2016
TP Transformateur de log
Authors: Honore Nintunze, Antonin Durey
"""

import sys
from io import StringIO as sio

class TransformateurLog:

    def __init__(self,transformateurIO, formatteur):
        self.io = transformateurIO
        self.formatteur = formatteur

    def get_logs(self,nom_fichier):
        liste_message = self.io.read_file(nom_fichier)
        if not self.formatteur.parse_logs(liste_message):
            raise MauvaisFormatLigneError()

        return liste_message

    def filtre(self, liste_message):
        return [x for x in liste_message if x.priorite >= 5]

    def write_logs(self, nom_fichier, liste):
        self.io.write_file(nom_fichier, liste)

    def transform(self, entree, sortie):
        self.write_logs(sortie,self.filtre(self.get_logs(entree)))

class EntreeSortieLog:

    def __init__(self,factory_message, fs=sys.stdin):
        self.factory_message = factory_message
        self.file_system = fs


    def read_file(self, nom_fichier):
        res = []
        for line in self.file_system:
            res.append(self.factory_message.create_message(line))

        return res

class FactoryMessage:
    pass


class Message:
    pass

class MauvaisFormatLigneError(Exception):
    pass
