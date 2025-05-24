def player(prev_play, opponent_history=[]):
    import random
    from collections import Counter

    # Inicializar estado persistente
    if not hasattr(player, "round"):
        player.round = 0
        player.patterns = {}
        player.last_pattern = ""
        player.opponent_history = []
        player.own_history = []
        player.is_abbey = False

    # Avanzar turno
    player.round += 1
    if prev_play:
        opponent_history.append(prev_play)
        player.opponent_history.append(prev_play)

    # Guardar tus propias jugadas para detectar Abbey
    if player.round > 1:
        player.own_history.append(player.last_move)

    # Detectar a Abbey (opcional y mejorable)
    if player.round == 15:
        # Si el oponente está contrarrestando nuestra jugada pasada de forma precisa
        abbey_like = 0
        for i in range(1, len(player.own_history)):
            expected = {"R": "P", "P": "S", "S": "R"}[player.own_history[i-1]]
            if opponent_history[i] == expected:
                abbey_like += 1
        if abbey_like / (len(player.own_history) - 1) > 0.6:
            player.is_abbey = True

    # Estrategia especial contra Abbey
    if player.is_abbey:
        # Juega aleatorio para romper su predicción
        move = random.choice(["R", "P", "S"])
        player.last_move = move
        return move

    # Tu lógica original de predicción
    if len(opponent_history) >= 4:
        pattern = "".join(opponent_history[-4:-1])
        next_move = opponent_history[-1]

        if pattern not in player.patterns:
            player.patterns[pattern] = {"R": 0, "P": 0, "S": 0}
        player.patterns[pattern][next_move] += 1

        player.last_pattern = "".join(opponent_history[-3:])

    # Predecir y contrarrestar
    prediction = "R"
    if player.last_pattern in player.patterns:
        pred_counts = player.patterns[player.last_pattern]
        prediction = max(pred_counts, key=pred_counts.get)

    counter_moves = {"R": "P", "P": "S", "S": "R"}
    move = counter_moves[prediction]
    player.last_move = move
    return move
