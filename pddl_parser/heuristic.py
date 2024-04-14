import random

def h(state, goal_pos, goal_not, name='base', weights=None, history_length=None):
    h_value = 0
    if weights is None:
        weights = {'default': 1}  # Poids par défaut pour chaque condition

    if name == 'base':
        # Conditions positives avec poids
        for condition in goal_pos:
            weight = weights.get(condition, weights['default'])
            if condition not in state:
                h_value += weight
        # Conditions négatives avec poids
        for condition in goal_not:
            weight = weights.get(condition, weights['default'])
            if condition in state:
                h_value += weight

    elif name == 'unsatisfied_predicates':
        # Seulement les conditions positives non satisfaites
        for condition in goal_pos:
            weight = weights.get(condition, weights['default'])
            if condition not in state:
                h_value += weight

    elif name == 'complex_conditions':
        # Évaluation basée sur des combinaisons spécifiques de conditions
        for combo in goal_pos:
            if isinstance(combo, tuple):  # Supposons qu'un tuple représente une combinaison de conditions
                combo_weight = sum(weights.get(cond, weights['default']) for cond in combo)
                if all(cond not in state for cond in combo):
                    h_value += combo_weight

    elif name == 'adaptive':
        # Ajuste les poids en fonction de la longueur de l'historique
        if history_length is not None:
            for condition in goal_pos:
                adaptive_weight = weights.get(condition, weights['default']) * (1 + 0.1 * history_length)
                if condition not in state:
                    h_value += adaptive_weight

    return h_value
