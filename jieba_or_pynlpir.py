# -*-coding:utf-8 -*
"""
Alexander DELAPORTE - CRLAO
https://tekipaki.hypotheses.org/
https://github.com/alxdrdelaporte/
https://gitlab.com/alxdrdelaporte/
https://gitlab.huma-num.fr/alxdrdelaporte/

Ligne de commande avec Python
https://tekipaki.hypotheses.org/3300

Pour le fonctionnement de Jieba et PyNLPIR, voir respectivement :
- https://tekipaki.hypotheses.org/115
- https://tekipaki.hypotheses.org/117
"""

import argparse
import jieba.posseg as pseg
import pynlpir

def recuperer_arguments():
    """Fonction pour création d'un parser pour les arguments passés en ligne de commande"""
    # Instance d'ArgumentParser()
    parser = argparse.ArgumentParser()
    # Ajout d'un argument pour chemin du fichier d'entrée
    parser.add_argument("--fichier_entree", "-e",
                        help="Chemin d'accès du fichier d'entrée, défaut = ./input.txt",
                        default="./input.txt",
                        type=str)
    # Ajout d'un argument pour choix du segmenteur, entre Jieba et PyNLPIR
    parser.add_argument("--segmenteur", "-s",
                        help="Choix du segmenteur (jieba ou j pour utiliser Jieba, pynlpir ou p pour utiliser PyNLPIR),"
                             " défaut = jieba",
                        choices=["j", "jieba", "p", "pynlpir"],
                        default="j",
                        type=str)
    # Parsing des arguments
    args = parser.parse_args()
    return args


def debut_programme(fichier, segmenteur):
    """Fonction pour affichage d'un message au début de l'exécution du programme"""
    print(f"**SEGMENTATION ET ÉTIQUETAGE DU FICHIER {fichier} AVEC {segmenteur}**")


if __name__ == '__main__':

    arguments = recuperer_arguments()

    with open(arguments.fichier_entree, "r", encoding="utf-8") as source:

        jieba_args = ["jieba", "j"]
        pynlpir_args = ["pynlpir", "p"]

        tagged_text = []

        # Utilisation de Jieba
        if arguments.segmenteur in jieba_args:

            nom_segmenteur = "Jieba"
            debut_programme(arguments.fichier_entree, nom_segmenteur)

            # https://tekipaki.hypotheses.org/115
            for line in source:
                if len(line) > 1:
                    line = line.replace("\n", "")
                    words = pseg.cut(line)
                    tagged_segment = ""
                    for w in words:
                        tagged_segment += f"{w} "
                    tagged_segment = f"{tagged_segment}\n"
                    tagged_text.append(tagged_segment)

        # Utilisation de PyNLPIR
        elif arguments.segmenteur in pynlpir_args:

            nom_segmenteur = "PyNLPIR"
            debut_programme(arguments.fichier_entree, nom_segmenteur)

            # https://tekipaki.hypotheses.org/117
            pynlpir.open(encoding_errors="replace")
            for line in source:
                if len(line) > 1:
                    postag = pynlpir.segment(line, pos_names='raw')
                    for segment in postag:
                        tagged_segment = ""
                        for word, part_of_speech in postag:
                            try:
                                tagged_word = f"{word}/{part_of_speech} "
                            except TypeError:
                                tagged_word = f"{word}/None "
                            tagged_segment += tagged_word
                    tagged_segment = f"{tagged_segment}\n"
                    tagged_text.append(tagged_segment)
    print("".join(tagged_text))
