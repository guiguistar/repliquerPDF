#!/usr/bin/env python3
# coding: utf-8

import sys
import os
import shutil
import PyPDF2

if __name__ == '__main__':
    n_arg = len(sys.argv)
    assert n_arg == 3, f"Le nombdre d'arguments doit être 2 et non {n_arg-1}"

    nom_fichier = sys.argv[1]
    print(f"Le nom du fichier est {nom_fichier}")
    assert nom_fichier.endswith('.pdf'), "Le nom du fichier doit finir par .pdf"

    n_copies = int(sys.argv[2])
    assert 0 < n_copies < 100, f"Le nombre de copies doit être compris entre 0 et 100 et non {n_copies}"

    concateneur = PyPDF2.PdfMerger()
    
    with open(nom_fichier, 'r') as source:
        for i in range(n_copies):
            nom_destination = f"{nom_fichier[:-4]}_{i:02}.pdf"
            print(f"Traitement du fichier {nom_destination}")

            # Produit une i eme copie du fichier source
            shutil.copy(os.path.join(".", nom_fichier), os.path.join(".", nom_destination))

            # Ouvre puis ajoute la i eme copie au concateneur
            with open(nom_destination, 'rb') as dest:
                concateneur.append(PyPDF2.PdfReader(dest))

            # Supprime la i eme copie
            os.remove(nom_destination)

        # Enregistre le résultat        
        concateneur.write(f"{nom_fichier[:-4]}_{n_copies}.pdf")
        concateneur.close()
