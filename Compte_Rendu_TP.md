# 📝 Compte rendu – TP Ordonnancement de tâches

## 1️⃣ Modélisation du problème

### 📌 Variables de décision
- **Affectation des opérations**  
  x_{j,o,m} = 1 si l’opération o du job j est effectuée sur la machine m, 0 sinon.

- **Début d’exécution de chaque opération**  
  S_{j,o} : heure de début de l’opération o du job j.

- **Statut d’allumage des machines**  
  Y_{m,t} = 1 si la machine m est allumée à l’instant t, 0 sinon.

- **Heures de démarrage et d’arrêt des machines**  
  - start_{m,k} : heure de démarrage du k-ième allumage de la machine m.  
  - stop_{m,k} : heure d’arrêt du k-ième allumage de la machine m.

---

### 📌 Contraintes

✅ **Séquence d’opérations (ordre interne des jobs)**  
Pour chaque job j :  
S_{j,o+1} >= S_{j,o} + somme sur m ( x_{j,o,m} * processing_time_{j,o,m} )

✅ **Affectation unique**  
Chaque opération doit être affectée à exactement une machine :  
somme sur m ( x_{j,o,m} ) = 1

✅ **Pas de chevauchement**  
Une machine ne peut pas exécuter plusieurs opérations en même temps.  
Si une machine est en cours d’exécution, elle doit être allumée.

✅ **Allumage et extinction**  
Lorsqu’une machine est allumée, on ajoute le temps de démarrage et le coût énergétique correspondant.  
De même pour l’extinction.

✅ **Durée maximale des machines**  
Le planning global de chaque machine ne doit pas dépasser la durée maximale fixée (end_time).

---

### 📌 Objectifs

- **Minimiser la consommation d’énergie totale** :
  - Consommation liée au démarrage et à l’extinction (set_up_energy et tear_down_energy)
  - Consommation à vide (min_consumption)
  - Consommation en fonctionnement (energy_consumption)

- **Minimiser la durée totale du planning (makespan)** :
  - Réduire la date de fin du dernier job.

---

## 2️⃣ Fonction objectif

L’entreprise souhaite équilibrer la consommation d’énergie et la durée totale du planning.

**Forme proposée (fonction objectif multi-critère)** :  
Z = alpha * E_total + beta * C_max

Où :
- E_total = consommation d’énergie totale :  
    somme sur m (  
      somme sur k (set_up_energy_m + tear_down_energy_m)  
      + somme sur t ( min_consumption_m * Y_{m,t} )  
    )  
    + somme sur j,o,m ( x_{j,o,m} * energy_consumption_{j,o,m} )

- C_max = durée totale du planning (makespan) :  
    max sur j ( S_{j,last} + processing_time_{j,last} )

- alpha et beta sont des coefficients de pondération fixés selon la priorité donnée à la consommation ou à la durée.

**Remarque** :  
- Si l’entreprise privilégie l’énergie => alpha > beta  
- Si elle privilégie la rapidité => beta > alpha

---

## 📊 Résumé

| Élément                     | Description                                                                                                                    |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Variables de décision       | x_{j,o,m}, S_{j,o}, Y_{m,t}, start_{m,k}, stop_{m,k}                                                                           |
| Contraintes                 | Séquence des opérations, affectation unique, pas de chevauchement, gestion allumage/extinction, durée maximale des machines    |
| Objectifs                   | Consommation d’énergie + durée totale (makespan)                                                                              |
| Fonction objectif proposée  | Z = alpha * E_total + beta * C_max                                                                                            |

---
