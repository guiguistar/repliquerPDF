#!/usr/bin/env python3
# coding: utf-8

import sys
import os
import tempfile
import PyPDF2

def afficherExemples():
    print('Exemples d\'utilisation :\n')
    print(' ./repliquerPDF.py exemple.pdf 10')
    print(' ./repliquerPDF.py exemple2.pdf 20')
    print()
    print('Le nom du fichier .pdf et le nombre d\'exemplaires que doit contenir le résultat sont obligatoires.')

if __name__ == '__main__':
    n_arg = len(sys.argv)
    if not n_arg == 3:
        print(f'Le nombdre d\'arguments doit être 2 et non {n_arg-1}.\n')
        afficherExemples()
        exit()

    nom_fichier = sys.argv[1]
    print(f"Le nom du fichier est {nom_fichier}")
    assert nom_fichier.endswith('.pdf'), "Le nom du fichier doit finir par .pdf"

    n_copies = int(sys.argv[2])
    assert 0 < n_copies < 100, f"Le nombre de copies doit être compris entre 0 et 100 et non {n_copies}"

    concateneur = PyPDF2.PdfMerger()

    with open(nom_fichier, 'rb') as source:
        lecteur = PyPDF2.PdfReader(source)
        nPages = len(lecteur.pages)

        print(f'Le fichier a {nPages} page(s).')

        if nPages % 2:
            _, _, w, h = lecteur.pages[0]['/MediaBox']
            ecriveur = PyPDF2.PdfWriter()
            ecriveur.add_blank_page(w,h)

        for i in range(n_copies):
            concateneur.append(lecteur)
            if nPages % 2:
                # fichier temporaire virtuel; évite d'écrire sur le disque
                with tempfile.SpooledTemporaryFile() as f:
                    ecriveur.write(f)
                    pageBlanche = PyPDF2.PdfReader(f)
                    concateneur.append(pageBlanche)

        # Enregistre le résultat        
        concateneur.write(f"{nom_fichier[:-4]}_{n_copies}.pdf")
        concateneur.close()
