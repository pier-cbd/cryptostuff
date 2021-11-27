## @package cryptostuff
# Estimation staking vs trading autour du coin Harmony
 
import math

montantInitiale = 1000
nbJourAnnee = 365.25
# [Est. APY, jours] !! Deux derniers jamais disponibles !!
binanceStaking = [[0.0852, 30], [0.129, 60], [0.2051, 90]]

##      Calcul de staking annuel
#
# \param recompensePrct (int) recompense en % proposé par la plateforme
# \param dureeContrat (int) duree du contrat en jours
# \param reStakeRecPrct (int) depot en stake de la récompense en %
# \return (int) summary
#
def totalAnnuelViaStaking(recompensePrct, dureeContrat, reStakeRecPrct):
    nbContratsAnnuel = nbJourAnnee / dureeContrat
    recompenseContratPrct = (dureeContrat * recompensePrct) / nbJourAnnee
    print("Nb de contrats/an : ", nbContratsAnnuel)

    # Premier contrat
    soldeFinContrat = montantInitiale
    soldeNonStake = 0
    
    # Contrats suivants avec pourcentage de staking des recompenses (auto stake = 100%)
    for i in range(math.trunc(nbContratsAnnuel)):
        recompenseFinContrat = soldeFinContrat * recompenseContratPrct
        soldeFinContrat = soldeFinContrat + (recompenseFinContrat * reStakeRecPrct)
        soldeNonStake = soldeNonStake + (recompenseFinContrat * (1 - reStakeRecPrct))
        print("Solde fincontrat 1 : ", soldeFinContrat + soldeNonStake)
    
    # Dernier morceau du contrat fin d'annee, abstraction le contrat n'est pas fini ! 
    jourRestants = (nbContratsAnnuel % 1) * dureeContrat
    recompenseDernier = soldeFinContrat * ((jourRestants * recompensePrct) / nbJourAnnee)
    soldeFinContrat = soldeFinContrat + (recompenseDernier * reStakeRecPrct)
    soldeNonStake = soldeNonStake + (recompenseDernier * (1 - reStakeRecPrct))

    soldeFinContrat = soldeFinContrat + soldeNonStake
    print("Dernier morceau : ", soldeFinContrat)

    return round(soldeFinContrat, 2)




def rapportStaking(t):
    t.write("\n  1) Staking des recompenses entre contrats\n")
    for i in range(3):
        t.write("\n\tContrat Binance Est. APY : " + str(binanceStaking[i][0] * 100) + "% durée de " + 
                str(binanceStaking[i][1]) + " jours  ")
        t.write("\n\t\tSolde au bout d'une année : " +
                str(totalAnnuelViaStaking(binanceStaking[i][0], binanceStaking[i][1], 1)) + " ONE")
    t.write("\n\n  2) 50% de staking des recompenses entre contrats\n")
    for i in range(3):
        t.write("\n\tContrat Binance Est. APY : " + str(binanceStaking[i][0] * 100) + "% durée de " + 
                str(binanceStaking[i][1]) + " jours  ")
        t.write("\n\t\tSolde au bout d'une année : " +
                str(totalAnnuelViaStaking(binanceStaking[i][0], binanceStaking[i][1], 0.5)) + " ONE")
    t.write("\n\n  3) Pas de staking des recompenses entre contrats\n")
    for i in range(3):
        t.write("\n\tContrat Binance Est. APY : " + str(binanceStaking[i][0] * 100) + "% durée de " + 
                str(binanceStaking[i][1]) + " jours  ")
        t.write("\n\t\tSolde au bout d'une année : " +
                str(totalAnnuelViaStaking(binanceStaking[i][0], binanceStaking[i][1], 0)) + " ONE")

def genereRapport():
    with open("rapport.txt", 'r+') as f:
        f.truncate(4)
        f.write("Montant initial : " + str(montantInitiale) + " ONE\n")
        f.write("\n\nI) Stratégie Staking\n")
        rapportStaking(f)
        f.close()

def main():
    genereRapport()
    print("Rapport genere")

if __name__ == "__main__":
    main()