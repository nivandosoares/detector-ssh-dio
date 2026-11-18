"""Detecta sequências de autenticação suspeitas em registros normalizados."""

import csv
import sys
from collections import defaultdict, deque
from datetime import datetime, timedelta

WINDOW = timedelta(minutes=5)
THRESHOLD = 5


def detectar(eventos):
    falhas = defaultdict(deque)
    for horario, conta, origem, resultado in sorted(eventos):
        recentes = falhas[conta, origem]
        while recentes and horario - recentes[0] > WINDOW:
            recentes.popleft()

        if resultado == "falha":
            recentes.append(horario)
            if len(recentes) == THRESHOLD:
                yield horario, conta, origem, "falhas repetidas"
        elif resultado == "sucesso":
            if len(recentes) >= THRESHOLD:
                yield horario, conta, origem, "sucesso após falhas repetidas"
            recentes.clear()
        else:
            raise ValueError(f"Resultado desconhecido: {resultado!r}")


def main(caminho):
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        eventos = [
            (
                datetime.fromisoformat(linha["horario"]),
                linha["conta"],
                linha["origem"],
                linha["resultado"],
            )
            for linha in csv.DictReader(arquivo)
        ]

    for horario, conta, origem, alerta in detectar(eventos):
        print(f"{horario.isoformat()} | {conta} | {origem} | {alerta}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python3 detectar.py eventos.csv")
    main(sys.argv[1])
