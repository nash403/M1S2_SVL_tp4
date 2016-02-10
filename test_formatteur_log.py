"""
SVL 2015-2016
TP Transformateur de log
Authors: Honore Nintunze, Antonin Durey
Tests
"""
import unittest
from io import StringIO as sio
from mockito import *
from transformateur_log import *

# fonctionnalites:
# * parser des logs au format : "yyyy-mm-dd, p, msg" où p est un entier entre 1 et 10 et msg un message
# - tous les logs sont au bon format : on renvoie True
# - au moins un log n'est pas au bon format : on renvoie False
# * parser un log au format : "yyyy-mm-dd, p, msg" où p est un entier entre 1 et 10 et msg un message
# - le log est au bon format : on renvoie True
# - le log n'est pas au bon format : on renvoie False

class FormatteurParseUnLog(unittest.TestCase):
    """
    Tous les cas ne sont pas forcement testes car ils sont nombreux
    """

    def test_log_au_bon_format_le_parse_reussi(self):
        """
        Parse sur une ligne au bon format renvoie True
        """
        formatteur = Formatteur()
        message = mock()
        BONNE_LIGNE = "2015-02-20, 2, error in database"
        message.texte = BONNE_LIGNE

        self.assertEqual(formatteur.parse(message), True)

    def test_log_au_mauvais_format_le_parse_echoue(self):
        """
        Parse sur une ligne au mauvais format renvoie False
        """
        formatteur = Formatteur()
        message = mock()
        MAUVAISE_LIGNE = "2015-, 2, error in database"
        message.texte = MAUVAISE_LIGNE

        self.assertEqual(formatteur.parse(message), False)

class FormatteurParseListeLog(unittest.TestCase):
    """
    Tous les cas ne sont pas forcement testes car ils sont nombreux
    """

    def test_tous_les_logs_sont_au_bon_format_le_parse__reussi(self):
        """
        Toutes les lignes sont au bon format, renvoie True
        """
        formatteur = Formatteur()
        message1 = mock()
        message2 = mock()
        BONNE_LIGNE1 = "2015-02-20, 2, error in database"
        BONNE_LIGNE2 = "2015-12-04, 6, error in system"
        message1.texte = BONNE_LIGNE1
        message2.texte = BONNE_LIGNE2
        LISTE = [message1,message2]

        self.assertEqual(formatteur.parse_logs(LISTE), True)

    def test_log_au_mauvais_format_le_parse_echoue(self):
        """
        Au moins une ligne au mauvais format, renvoie False
        """
        formatteur = Formatteur()
        message1 = mock()
        message2 = mock()
        MAUVAISE_LIGNE = "2015-, 2, error in database"
        BONNE_LIGNE = "2015-02-20, 2, error in database"
        message1.texte = MAUVAISE_LIGNE
        message2.texte = BONNE_LIGNE
        LISTE = [message1,message2]

        self.assertEqual(formatteur.parse_logs(LISTE), False)
