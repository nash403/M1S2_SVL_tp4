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

# fonctionnalites
# lire fichier de log
# - fichier vide retourne liste vide
# - ficher correct renvoie la liste des log
# - ficher au mauvais format renvoie un erreur
# filtrer message de log
# - on trouve aucun message
# - on renvoie les messages qui correspondent
# ecrire fichier de log



class TestTransformateurLectureLog(unittest.TestCase):

    def test_lire_fichier_vide_retourne_liste_vide(self):
        """
        Fichier vide.
        """
        NOM_FICHIER = 'toto'
        VIDE = []
        es = mock()
        formatteur = mock()
        when(es).read_file(NOM_FICHIER).thenReturn(VIDE)
        when(formatteur).parse_logs(VIDE).thenReturn(True)

        transformateur = TransformateurLog(es, formatteur)

        self.assertEqual(transformateur.get_logs(NOM_FICHIER),VIDE)


    def test_lire_fichier_au_mauvais_format_renvoie_erreur(self):
        """
        Mauvais format: Pour parser un message, on ne testera pas tout les cas de mauvais parsing
        """
        NOM_FICHIER = 'toto'
        es = mock()
        formatteur = mock()
        transformateur = TransformateurLog(es, formatteur)
        LIGNE = mock()
        MAUVAISE_LIGNE = [LIGNE]
        when(es).read_file(NOM_FICHIER).thenReturn(MAUVAISE_LIGNE)
        when(formatteur).parse_logs(MAUVAISE_LIGNE).thenReturn(False)

        self.assertRaises(MauvaisFormatLigneError, transformateur.get_logs, NOM_FICHIER)


    def test_lire_fichier_correct_renvoie_liste_logs(self):
        """
        Fichier correct.
        """
        NOM_FICHIER = 'toto'
        es = mock()
        formatteur = mock()
        transformateur = TransformateurLog(es, formatteur)
        LIGNE = mock()
        BONNE_LIGNE = [LIGNE]
        when(es).read_file(NOM_FICHIER).thenReturn(BONNE_LIGNE)
        when(formatteur).parse_logs(BONNE_LIGNE).thenReturn(True)

        self.assertEqual(transformateur.get_logs(NOM_FICHIER), BONNE_LIGNE)

class TestTransformateurFiltrageLog(unittest.TestCase):

    def test_aucun_message_correspond_renvoie_liste_vide(self):
        """
        Aucun message correspond
        """
        NOM_FICHIER = 'toto'
        es = mock()
        formatteur = mock()
        VIDE = []
        transformateur = TransformateurLog(es, formatteur)
        MAUVAISE_LIGNE1 = mock()
        MAUVAISE_LIGNE2 = mock()
        MAUVAISE_LIGNE3 = mock()
        LIGNES = [MAUVAISE_LIGNE1,MAUVAISE_LIGNE2,MAUVAISE_LIGNE3]

        MAUVAISE_LIGNE1.priorite = 1
        MAUVAISE_LIGNE2.priorite = 2
        MAUVAISE_LIGNE3.priorite = 3

        self.assertEqual(transformateur.filtre(LIGNES), VIDE)


    def test_quand_des_messages_correspondent_renvoie_liste_filtree(self):
        """
        Des messages correspondent
        """
        es = mock()
        formatteur = mock()
        transformateur = TransformateurLog(es, formatteur)
        BONNE_LIGNE1 = mock()
        MAUVAISE_LIGNE2 = mock()
        BONNE_LIGNE3 = mock()
        LIGNES = [BONNE_LIGNE1,MAUVAISE_LIGNE2,BONNE_LIGNE3]

        BONNE_LIGNE1.priorite = 5
        MAUVAISE_LIGNE2.priorite = 2
        BONNE_LIGNE3.priorite = 8
        LISTE_FILTREE = [BONNE_LIGNE1,BONNE_LIGNE3]

        self.assertEqual(transformateur.filtre(LIGNES), LISTE_FILTREE)

class TestTransformateurEcritureLog(unittest.TestCase):

    def test_ecriture_de_log(self):
        """
        Des messages correspondent
        """
        NOM_FICHIER = 'toto'
        es = mock()
        formatteur = mock()
        transformateur = TransformateurLog(es, formatteur)
        LIGNE1 = mock()
        LIGNE2 = mock()
        LIGNE3 = mock()
        LIGNES = [LIGNE1,LIGNE2,LIGNE3]

        transformateur.write_logs(NOM_FICHIER, LIGNES)

        verify(es).write_file(NOM_FICHIER, LIGNES)

class TestInputLogs(unittest.TestCase):

    def test_lecture_de_logs_vide_renvoie_liste_vide(self):
        """
        Le fichier est vide
        """
        NOM_FICHIER = 'toto'
        factory_message = mock()
        es = EntreeSortieLog(factory_message,sio(""))
        VIDE = []

        self.assertEqual(es.read_file(NOM_FICHIER),VIDE)

    def test_lecture_de_logs_renvoie_liste_messages(self):
        """
        Le fichier contient des logs
        """

        factory_message = mock()
        NOM_FICHIER = 'toto'
        MESSAGE1 = mock()
        MESSAGE2 = mock()
        MESSAGE1.texte = "2010-02-25, 5, error in database\n"
        MESSAGE2.texte = "2010-02-25, 5, error in system\n"

        when(factory_message).create_message(MESSAGE1.texte).thenReturn(MESSAGE1)
        when(factory_message).create_message(MESSAGE2.texte).thenReturn(MESSAGE2)

        es = EntreeSortieLog(factory_message, sio(MESSAGE1.texte + MESSAGE2.texte))
        LISTE = [MESSAGE1, MESSAGE2]

        self.assertEqual(es.read_file(NOM_FICHIER),LISTE)
