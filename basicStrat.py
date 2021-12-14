## @package cryptostuff
# Estimation staking vs trading autour du coin Harmony
 
import math
import csv

montantInitiale = 1000
nbJourAnnee = 365
# [Est. APY, jours] !! Deux derniers jamais disponibles !!
binanceStaking = [[0.0852, 30], [0.129, 60], [0.2051, 90]]
bianceFees = 0.005

##      Calcul de staking annuel
#
# \param recompensePrct (int) recompense en % proposée par la plateforme
# \param dureeContrat (int) duree du contrat en jours
# \param reStakeRecPrct (int) depot en stake de la récompense en %
# \return (int) summary
#
def totalAnnuelViaStaking(recompensePrct, dureeContrat, reStakeRecPrct):
    nbContratsAnnuel = nbJourAnnee / dureeContrat
    recompenseContratPrct = (dureeContrat * recompensePrct) / nbJourAnnee
    #print("Nb de contrats/an : ", nbContratsAnnuel)

    # Premier contrat
    soldeFinContrat = montantInitiale
    soldeNonStake = 0
    
    # Contrats suivants avec pourcentage de staking des recompenses (auto stake = 100%)
    for i in range(math.trunc(nbContratsAnnuel)):
        recompenseFinContrat = soldeFinContrat * recompenseContratPrct
        soldeFinContrat = soldeFinContrat + (recompenseFinContrat * reStakeRecPrct)
        soldeNonStake = soldeNonStake + (recompenseFinContrat * (1 - reStakeRecPrct))
        #print("Solde fin contrat ", i + 1, ":", soldeFinContrat + soldeNonStake)
    
    # Dernier morceau du contrat fin d'annee, abstraction le contrat n'est pas fini ! 
    jourRestants = (nbContratsAnnuel % 1) * dureeContrat
    recompenseDernier = soldeFinContrat * ((jourRestants * recompensePrct) / nbJourAnnee)
    soldeFinContrat = soldeFinContrat + (recompenseDernier * reStakeRecPrct)
    soldeNonStake = soldeNonStake + (recompenseDernier * (1 - reStakeRecPrct))

    soldeFinContrat = soldeFinContrat + soldeNonStake
    #print("Dernier morceau : ", soldeFinContrat)

    return round(soldeFinContrat, 2)

##      Bot basique achat -10%, vente +10% par rapport à une valeur statique
#
# \param dateInitiale (string) date de mise en service du bot
# \param prctAchat (int) seuil d'achat en % chute du cours par rapport à valeur init
# \param prctVente (int) seuil de vente en % envolée du cours par rapport à valeur init
# \param prctCommission (int) commission achat/vente en % prélevée par la plateforme
# \return soldeFinal (int) solde en ONE à la fin de la simulation
# \return nombreDeJours (int) nombre de jours de fonctionnement du bot
#
def botAchatVenteSurHistorique(dateInitiale, prctAchat, prctVente, prctCommission):
    flagDeclanchement = False
    nombreDeJours = 0
    soldeOne = montantInitiale
    soldeUsd = 0
    soldeFinal = 0
    with open('data_harmony_messari.csv', 'r') as file:
        reader = csv.reader(file)
        for each_row in reader:
            if each_row[0] == dateInitiale:
                flagDeclanchement = True
                prixInitial = float(each_row[4]) # Prix initial valeur d'ouverture du jour 1 en $
                #print("Solde One : ", soldeOne, " Solde Usd :" , soldeUsd)
            if flagDeclanchement == True and nombreDeJours < 365:
                nombreDeJours += 1
                # Si minimum journée < -x% du prix initial on achete du One
                #print("Prix haut : ", round(float(each_row[2]), 3), "Prix Bas : ", 
                #    round(float(each_row[3]),3),"Prix achat : ", round(prixInitial, 3))
                if (float(each_row[3]) < (1 - prctAchat) * prixInitial) and soldeUsd > 0:
                    soldeOne = (soldeUsd / ((1 - prctAchat) * prixInitial))*(1-prctCommission)
                    soldeUsd = 0
                    #print("Ordre achat : ", (1 - prctAchat) * prixInitial)
                    #print("Solde One : ", soldeOne, "solde Usd :" , soldeUsd)                 
                # Si maximum journée < +y% du prix initial on vent le One
                if (float(each_row[2]) > (1 + prctVente) * prixInitial) and soldeOne > 0:
                    soldeUsd = (soldeOne * (1 + prctVente) * prixInitial)*(1-prctCommission)
                    soldeOne = 0
                    #print("Ordre vente : ", (1 + prctAchat) * prixInitial)
                    #print("Solde One : ", soldeOne, "solde Usd :" , soldeUsd)             
                soldeFinal = soldeOne + (soldeUsd / float(each_row[4]))
                #print("gain : ", soldeFinal)
    return soldeFinal,nombreDeJours

##      Bot basique achat -10%, vente +10% par rapport à une valeur myenne des x dernies jours
#
# \param dateInitiale (string) date de mise en service du bot
# \param prctAchat (int) seuil d'achat en % chute du cours par rapport à valeur init
# \param prctVente (int) seuil de vente en % envolée du cours par rapport à valeur init
# \param prctCommission (int) commission achat/vente en % prélevée par la plateforme
# \param moyenneJours (int) nombre jours précédent 
# \return soldeFinal (int) solde en ONE à la fin de la simulation
# \return nombreDeJours (int) nombre de jours de fonctionnement du bot
#
def botMoyenneur(dateInitiale, prctAchat, prctVente, prctCommission, moyenneJours):
    flagDeclanchement = False
    nombreDeJours = 0
    soldeOne = montantInitiale
    soldeUsd = 0
    soldeFinal = 0
    with open('data_harmony_messari.csv', 'r') as file:
        reader = csv.reader(file)
        # Calcul du moyenne dans une liste
        for each_row in reader:
            bite = 1
            

        for each_row in reader:
            if each_row[0] == dateInitiale:
                flagDeclanchement = True
                prixInitial = float(each_row[4]) # Prix initial valeur d'ouverture du jour 1 en $
                #print("Solde One : ", soldeOne, " Solde Usd :" , soldeUsd)
            if flagDeclanchement == True and nombreDeJours < 365:
                nombreDeJours += 1
                # Si minimum journée < -x% du prix initial on achete du One
                #print("Prix haut : ", round(float(each_row[2]), 3), "Prix Bas : ", 
                #    round(float(each_row[3]),3),"Prix achat : ", round(prixInitial, 3))
                if (float(each_row[3]) < (1 - prctAchat) * prixInitial) and soldeUsd > 0:
                    soldeOne = (soldeUsd / ((1 - prctAchat) * prixInitial))*(1-prctCommission)
                    soldeUsd = 0
                    #print("Ordre achat : ", (1 - prctAchat) * prixInitial)
                    #print("Solde One : ", soldeOne, "solde Usd :" , soldeUsd)                 
                # Si maximum journée < +y% du prix initial on vent le One
                if (float(each_row[2]) > (1 + prctVente) * prixInitial) and soldeOne > 0:
                    soldeUsd = (soldeOne * (1 + prctVente) * prixInitial)*(1-prctCommission)
                    soldeOne = 0
                    #print("Ordre vente : ", (1 + prctAchat) * prixInitial)
                    #print("Solde One : ", soldeOne, "solde Usd :" , soldeUsd)             
                soldeFinal = soldeOne + (soldeUsd / float(each_row[4]))
                #print("gain : ", soldeFinal)
    return soldeFinal,nombreDeJours


#
##      Génération du rapport.txt
#
def rapportStaking(t):
    t.write("\n  1) 100% de staking des recompenses entre contrats\n")
    for i in range(3):
        soldeAnnuel = totalAnnuelViaStaking(binanceStaking[i][0], binanceStaking[i][1], 1)
        t.write("\n\tContrat Binance Est. APY : " + str(binanceStaking[i][0] * 100) + "% durée de " + 
                str(binanceStaking[i][1]) + " jours  ")
        t.write("\n\t\tSolde au bout d'une année : " +
                str(soldeAnnuel) + " ONE (rendement " + 
                str(round(((soldeAnnuel - montantInitiale) / montantInitiale) * 100, 2)) + "%)")
    t.write("\n\n  2) 50% de staking des recompenses entre contrats\n")
    for i in range(3):
        soldeAnnuel = totalAnnuelViaStaking(binanceStaking[i][0], binanceStaking[i][1], 0.5)
        t.write("\n\tContrat Binance Est. APY : " + str(binanceStaking[i][0] * 100) + "% durée de " + 
                str(binanceStaking[i][1]) + " jours  ")
        t.write("\n\t\tSolde au bout d'une année : " +
                str(soldeAnnuel) + " ONE (rendement " + 
                str(round(((soldeAnnuel - montantInitiale) / montantInitiale) * 100, 2)) + "%)")
    t.write("\n\n  3) Pas de staking des recompenses entre contrats\n")
    for i in range(3):
        soldeAnnuel = totalAnnuelViaStaking(binanceStaking[i][0], binanceStaking[i][1], 0)
        t.write("\n\tContrat Binance Est. APY : " + str(binanceStaking[i][0] * 100) + "% durée de " + 
                str(binanceStaking[i][1]) + " jours  ")
        t.write("\n\t\tSolde au bout d'une année : " +
                str(soldeAnnuel) + " ONE (rendement " + 
                str(round(((soldeAnnuel - montantInitiale) / montantInitiale) * 100, 2)) + "%)")

def rapportDummyTrading(t):
    t.write("\n  1) Bot de trading achat -10% vente +10% journalier par rapport à valeur d'ouverture du jour de mise en service \n")
    t.write("\n\tMise en sevice le 2021-11-21")
    soldeFinale,nbJours = botAchatVenteSurHistorique("2021-11-21", 0.1, 0.1, bianceFees)
    t.write("\n\t\tSolde au bout de " + str(nbJours) + " jours " + str(round(soldeFinale, 0))  + " ONE (rendement " + 
            str(round(((soldeFinale - montantInitiale) / montantInitiale) * 100, 2)) + "%)")
    t.write("\n\tMise en sevice le 2021-11-15")
    soldeFinale,nbJours = botAchatVenteSurHistorique("2021-11-15", 0.1, 0.1, bianceFees)
    t.write("\n\t\tSolde au bout de " + str(nbJours) + " jours " + str(round(soldeFinale, 0))  + " ONE (rendement " + 
            str(round(((soldeFinale - montantInitiale) / montantInitiale) * 100, 2)) + "%)")
    t.write("\n\tMise en sevice le 2021-09-15")
    soldeFinale,nbJours = botAchatVenteSurHistorique("2021-09-15", 0.1, 0.1, bianceFees)
    t.write("\n\t\tSolde au bout de " + str(nbJours) + " jours " + str(round(soldeFinale, 0))  + " ONE (rendement " + 
            str(round(((soldeFinale - montantInitiale) / montantInitiale) * 100, 2)) + "%)")
    t.write("\n\tMise en sevice le 2020-11-15")
    soldeFinale,nbJours = botAchatVenteSurHistorique("2020-11-15", 0.1, 0.1, bianceFees)
    t.write("\n\t\tSolde au bout de " + str(nbJours) + " jours " + str(round(soldeFinale, 0))  + " ONE (rendement " + 
            str(round(((soldeFinale - montantInitiale) / montantInitiale) * 100, 2)) + "%)")
    t.write("\n\t(Note : fonctionne mal sur la duree car les cours s'envolent et le bot ne peut plus acheter)")

def genereRapport():
    with open("rapport.txt", 'r+') as f:
        f.truncate(4)
        f.write("Montant initial : " + str(montantInitiale) + " ONE\n")
        f.write("\n\nI) Stratégie Staking (contrats 60 et 90 jours indispolibles sur Binance)\n")
        rapportStaking(f)
        f.write("\n\nII) Stratégie Trading conversion vers stable coin\n")
        rapportDummyTrading(f)
        f.close()

def main():
    genereRapport()
    print("Rapport genere")

if __name__ == "__main__":
    main()
