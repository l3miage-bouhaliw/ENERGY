# 📝 Compte rendu – TP Ordonnancement de tâches

## 1️⃣ Modélisation du problème

### 📌 Variables de décision

#### Variable d'affectation des opérations
$$x_{j,o,m} = \begin{cases} 
1 & \text{si l'opération } o \text{ du job } j \text{ est effectuée sur la machine } m \\ 
0 & \text{sinon} 
\end{cases}$$

#### Variable de début d'exécution
$$S_{j,o} \text{ : heure de début de l'opération } o \text{ du job } j$$

#### Variable de statut d'allumage des machines
$$Y_{m,t} = \begin{cases} 
1 & \text{si la machine } m \text{ est allumée à l'instant } t \\ 
0 & \text{sinon} 
\end{cases}$$

#### Variables de gestion des machines
- $start_{m,k}$ : heure de démarrage du $k$-ème allumage de la machine $m$
- $stop_{m,k}$ : heure d'arrêt du $k$-ème allumage de la machine $m$

---

## 📌 Contraintes du problème

### 🔄 Contrainte de séquence d'opérations
**Respect de l'ordre interne des jobs :**

Pour chaque job $j$ et chaque opération $o$ :
$$S_{j,o+1} \geq S_{j,o} + \sum_{m} x_{j,o,m} \cdot \text{processing\_time}_{j,o,m}$$

> Cette contrainte garantit qu'une opération ne peut commencer qu'après la fin de l'opération précédente du même job.

### 🎯 Contrainte d'affectation unique
**Chaque opération doit être affectée à exactement une machine :**
$$\sum_{m} x_{j,o,m} = 1 \quad \forall j, o$$

### ⚠️ Contrainte de non-chevauchement
**Une machine ne peut pas exécuter plusieurs opérations simultanément :**
- Si une machine $m$ exécute une tâche à l'instant $t$, alors $Y_{m,t} = 1$
- Les intervalles d'exécution des opérations sur une même machine ne doivent pas se chevaucher

### 🔌 Contraintes d'allumage et d'extinction
**Gestion de l'état des machines :**
- Lorsqu'une machine démarre : coût de démarrage et temps de mise en route
- Lorsqu'une machine s'arrête : coût d'arrêt et temps de mise à l'arrêt
- Une machine en fonctionnement doit être dans l'état "allumée"

### ⏰ Contrainte de durée maximale
**Le planning global ne doit pas dépasser la durée limite :**
$$\max_{j,o} \left( S_{j,o} + \text{processing\_time}_{j,o} \right) \leq \text{end\_time}$$

---

## 2️⃣ Fonction objectif

### 🎯 Objectifs du problème

L'entreprise souhaite optimiser deux critères principaux :

1. **🔋 Minimiser la consommation d'énergie totale**
2. **⏱️ Minimiser la durée totale du planning (makespan)**

### 📊 Formulation mathématique

#### Consommation d'énergie totale
$$E_{\text{total}} = E_{\text{démarrage}} + E_{\text{fonctionnement}} + E_{\text{veille}}$$

Où :
- **Énergie de démarrage/arrêt :**
  $$E_{\text{démarrage}} = \sum_{m} \sum_{k} \left( \text{set\_up\_energy}_{m} + \text{tear\_down\_energy}_{m} \right)$$

- **Énergie de fonctionnement :**
  $$E_{\text{fonctionnement}} = \sum_{j,o,m} x_{j,o,m} \cdot \text{energy\_consumption}_{j,o,m}$$

- **Énergie de veille :**
  $$E_{\text{veille}} = \sum_{m} \int_{t} \text{min\_consumption}_{m} \cdot Y_{m,t} \, dt$$

#### Durée totale du planning (Makespan)
$$C_{\max} = \max_{j} \left( S_{j,\text{dernière}} + \text{processing\_time}_{j,\text{dernière}} \right)$$

### 🎯 Fonction objectif multi-critère

$$\boxed{Z = \alpha \cdot E_{\text{total}} + \beta \cdot C_{\max}}$$

**Paramètres de pondération :**
- $\alpha$ : coefficient de pondération pour l'énergie
- $\beta$ : coefficient de pondération pour la durée

**Stratégies d'optimisation :**
- **Priorité à l'efficacité énergétique :** $\alpha > \beta$
- **Priorité à la rapidité d'exécution :** $\beta > \alpha$
- **Équilibre :** $\alpha = \beta$

---

## 📊 Récapitulatif du modèle

| **Composant** | **Description** | **Notation** |
|---------------|-----------------|--------------|
| **Variables principales** | Affectation des opérations | $x_{j,o,m}$ |
| | Temps de début des opérations | $S_{j,o}$ |
| | État des machines | $Y_{m,t}$ |
| **Contraintes clés** | Séquence des opérations | $S_{j,o+1} \geq S_{j,o} + \sum_m x_{j,o,m} \cdot t_{j,o,m}$ |
| | Affectation unique | $\sum_m x_{j,o,m} = 1$ |
| | Non-chevauchement | Pas de conflit sur les machines |
| **Objectifs** | Consommation énergétique | $E_{\text{total}}$ |
| | Durée totale | $C_{\max}$ |
| **Fonction objectif** | Optimisation multi-critère | $Z = \alpha \cdot E_{\text{total}} + \beta \cdot C_{\max}$ |

---

## 💡 Points clés à retenir

1. **Modélisation complète** : Le problème intègre à la fois l'ordonnancement classique et la gestion énergétique
2. **Flexibilité** : Les coefficients $\alpha$ et $\beta$ permettent d'adapter la stratégie selon les priorités
3. **Complexité** : La prise en compte des coûts énergétiques ajoute une dimension supplémentaire au problème
4. **Applicabilité** : Le modèle est adapté aux environnements industriels modernes soucieux d'efficacité énergétique
