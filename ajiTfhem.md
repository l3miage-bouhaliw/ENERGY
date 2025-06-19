# Modélisation du Problème de Planification avec Contraintes Énergétiques

## 1. Variables de décision, contraintes et objectifs

### Variables de décision

**Variables principales :**
- `x_{i,j,k}` ∈ {0,1} : variable binaire indiquant si l'opération j de la tâche i est effectuée sur la machine k
- `t_{i,j}` ∈ ℝ⁺ : temps de début de l'opération j de la tâche i
- `s_k` ∈ ℝ⁺ : temps de démarrage de la machine k
- `e_k` ∈ ℝ⁺ : temps d'arrêt de la machine k

**Variables auxiliaires :**
- `on_{k,t}` ∈ {0,1} : variable binaire indiquant si la machine k est allumée au temps t
- `C_{max}` ∈ ℝ⁺ : makespan (durée totale du planning)
- `C_i` ∈ ℝ⁺ : temps de completion de la tâche i

### Contraintes

**Contraintes de précédence :**
- `t_{i,j+1} ≥ t_{i,j} + Σ_k (x_{i,j,k} × d_{i,j,k})` pour toute tâche i et opération j
  (Une opération ne peut commencer qu'après la fin de la précédente)

**Contraintes de capacité des machines :**
- `Σ_i x_{i,j,k} ≤ 1` pour chaque machine k et chaque intervalle de temps
  (Une machine ne peut effectuer qu'une opération à la fois)

**Contraintes d'affectation :**
- `Σ_k x_{i,j,k} = 1` pour chaque opération j de chaque tâche i
  (Chaque opération doit être affectée à exactement une machine)
- `x_{i,j,k} = 0` si la machine k ne peut pas effectuer l'opération j de la tâche i

**Contraintes temporelles :**
- `C_{max} ≥ t_{i,j} + Σ_k (x_{i,j,k} × d_{i,j,k})` pour toute opération
- `C_{max} ≤ T_{max}` (durée maximale imposée par l'entreprise)

**Contraintes énergétiques :**
- Les machines doivent être allumées avant d'effectuer des opérations
- Temps de démarrage et d'arrêt des machines pris en compte

### Objectifs

**Objectifs principaux :**
1. **Minimiser la consommation énergétique totale** : E_total
2. **Minimiser la durée totale** : C_max (makespan)
3. **Minimiser la durée moyenne des tâches** : (1/n) × Σ_i C_i

## 2. Fonction objectif agrégée

Nous proposons une fonction objectif multicritère pondérée :

```
f(x) = α × E_total + β × C_max + γ × (1/n) × Σ_i C_i
```

Où :
- **E_total** = Énergie de démarrage + Énergie d'arrêt + Énergie en veille + Énergie d'opération
- **α, β, γ** sont des coefficients de pondération avec α + β + γ = 1
- **n** est le nombre total de tâches

**Calcul détaillé de l'énergie :**
```
E_total = Σ_k (E_startup_k + E_shutdown_k) + 
          Σ_k (E_idle_k × temps_veille_k) + 
          Σ_i,j,k (x_{i,j,k} × E_operation_{i,j,k})
```

**Variante avec méthode ε-contrainte :**
Alternativement, on peut minimiser l'énergie sous contraintes temporelles :
```
Minimiser E_total
Sous contraintes : C_max ≤ ε₁ et (1/n) × Σ_i C_i ≤ ε₂
```

## 3. Évaluation des solutions

### Solution réalisable
Une solution est évaluée par :
```
Score = α × E_normalized + β × C_max_normalized + γ × C_mean_normalized
```

Où les valeurs normalisées sont calculées par rapport aux bornes connues :
- `E_normalized = (E_total - E_min) / (E_max - E_min)`
- `C_max_normalized = (C_max - C_max_min) / (C_max_max - C_max_min)`
- `C_mean_normalized = (C_mean - C_mean_min) / (C_mean_max - C_mean_min)`

### Solution non réalisable
Pour une solution non réalisable, on utilise une fonction de pénalité :
```
Score = Score_base + Σ_contraintes P_i × violation_i²
```

**Types de violations et pénalités :**
- **Violation de précédence** : P₁ × max(0, t_{i,j} + d_{i,j,k} - t_{i,j+1})²
- **Dépassement de capacité** : P₂ × nombre_conflits_machines²
- **Dépassement temporel** : P₃ × max(0, C_max - T_max)²
- **Opération non affectée** : P₄ × nombre_opérations_non_affectées

Les coefficients P_i doivent être suffisamment élevés pour rendre les solutions non réalisables moins attractives que les solutions réalisables.

## 4. Instance sans solution réalisable

### Description de l'instance

**Tâches :**
- Tâche 1 : 2 opérations (O₁₁, O₁₂)
- Tâche 2 : 2 opérations (O₂₁, O₂₂)

**Machines et capacités :**
- Machine M₁ : peut effectuer O₁₁, O₂₁
- Machine M₂ : peut effectuer O₁₂, O₂₂

**Durées et énergies :**
- Toutes les opérations : durée = 10 unités
- Démarrage/arrêt de chaque machine : 5 unités de temps chacun

**Contrainte temporelle :**
- T_max = 25 unités de temps

### Explication de l'infaisabilité

**Analyse temporelle :**
1. **Temps minimum requis pour une machine :**
   - Démarrage : 5 unités
   - Opération 1 : 10 unités  
   - Opération 2 : 10 unités
   - Arrêt : 5 unités
   - **Total : 30 unités**

2. **Contrainte violée :**
   - Temps minimum nécessaire (30) > Temps maximum autorisé (25)

3. **Solutions alternatives impossibles :**
   - **Une seule machine par type d'opération** : pas de parallélisation possible
   - **Contraintes de précédence strictes** : O₁₂ ne peut commencer qu'après O₁₁
   - **Temps incompressibles** : démarrage et arrêt obligatoires

**Conclusion :**
Cette instance est structurellement infaisable car le temps minimum requis pour exécuter toutes les opérations sur les machines disponibles dépasse la contrainte temporelle maximale imposée par l'entreprise.

### Généralisation

Une instance est généralement infaisable quand :
```
Σ_i (temps_minimum_tâche_i) + temps_démarrage_arrêt > T_max
```

Ou quand il existe des goulots d'étranglement dans l'affectation des opérations aux machines disponibles.