#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
getJason-v1.2.py

Sistema de pagos automatizado entre dos cuentas bancarias usando patrones:
- Singleton (acceso JSON)
- Cadena de comando (procesamiento de pagos)
- Iterator (historial cronológico)

Pedidos de pago de $500 son ejecutados desde cuentas alternadas, si hay saldo.

Uso:
    python getJason-v1.2.py pagar
    python getJason-v1.2.py listar
    python getJason-v1.2.py -v

Archivo JSON necesario: sitedata.json
Archivo de estado persistente: state.json

Versión 1.2 – UADERFCyT-IS2©2025
"""

import json
import sys
from abc import ABC, abstractmethod
from collections import deque
from os.path import exists

VERSION = "versión 1.2"
JSON_FILE = "sitedata.json"
STATE_FILE = "state.json"
MONTO_PAGO = 500


class JsonKeyRetrieverInterface(ABC):
    """Interfaz abstracta para recuperación de claves desde JSON."""

    @abstractmethod
    def get_value(self, key):
        """Retorna el valor de la clave especificada."""


class JsonKeyRetrieverSingleton(JsonKeyRetrieverInterface):
    """Singleton que carga claves por token desde archivo JSON."""

    _instance = None

    def __new__(cls, filepath):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(filepath)
        return cls._instance

    def _initialize(self, filepath):
        self.filepath = filepath
        self.data = self._load_json()

    def _load_json(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as err:
            raise ValueError(f"Error cargando JSON: {err}") from err

    def get_value(self, key):
        try:
            return self.data[key]
        except KeyError as err:
            raise ValueError(f"Clave '{key}' no encontrada.") from err


class PaymentCommand:
    """Comando que representa un pago realizado."""

    def __init__(self, order_number, token, amount):
        self.order_number = order_number
        self.token = token
        self.amount = amount

    def to_dict(self):
        """Devuelve una representación serializable."""
        return {
            "order_number": self.order_number,
            "token": self.token,
            "amount": self.amount
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["order_number"], data["token"], data["amount"])

    def __str__(self):
        return f"Pedido #{self.order_number}: ${self.amount} desde '{self.token}'"


class PaymentHistoryIterator:
    """Iterador para recorrer el historial de pagos."""

    def __init__(self, history):
        self._history = deque(history)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._history:
            raise StopIteration
        return self._history.popleft()


class PaymentProcessor:
    """Clase que procesa pagos y mantiene estado persistente."""

    def __init__(self, retriever):
        self.retriever = retriever
        self.accounts = {"token1": 1000, "token2": 2000}
        self.order_counter = 1
        self.history = []
        self.last_used_token = None
        self._load_state()

    def _load_state(self):
        if exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.accounts = data["balances"]
                self.order_counter = data["order_counter"]
                self.history = [PaymentCommand.from_dict(p) for p in data["history"]]
                self.last_used_token = data.get("last_used_token")

    def _save_state(self):
        data = {
            "balances": self.accounts,
            "order_counter": self.order_counter,
            "history": [p.to_dict() for p in self.history],
            "last_used_token": self.last_used_token
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _next_token(self, amount):
        tokens = ["token1", "token2"]
        if self.last_used_token == "token1":
            tokens.reverse()
        for token in tokens:
            if self.accounts[token] >= amount:
                return token
        return None

    def realizar_pago(self):
        """Realiza un pago de $500 si hay saldo suficiente en alguna cuenta."""
        token = self._next_token(MONTO_PAGO)
        if not token:
            print("No hay saldo suficiente en ninguna cuenta.")
            return

        self.accounts[token] -= MONTO_PAGO
        clave = self.retriever.get_value(token)
        command = PaymentCommand(self.order_counter, token, MONTO_PAGO)
        self.history.append(command)
        print(f"{command} (clave utilizada: {clave})")

        self.order_counter += 1
        self.last_used_token = token
        self._save_state()

    def listar_pagos(self):
        """Muestra todos los pagos realizados en orden cronológico."""
        if not self.history:
            print("No hay pagos registrados.")
            return

        print("Historial de pagos:")
        for pago in PaymentHistoryIterator(self.history.copy()):
            print(pago)


def mostrar_version():
    """Imprime la versión del programa."""
    print(VERSION)


def mostrar_uso():
    """Imprime ayuda de uso."""
    print(
        "Uso:\n"
        "  python getJason-v1.2.py pagar     # Realiza un pago de $500\n"
        "  python getJason-v1.2.py listar    # Muestra historial de pagos\n"
        "  python getJason-v1.2.py -v        # Muestra versión"
    )


def main():
    args = sys.argv[1:]

    if not args:
        mostrar_uso()
        return

    if args[0] == "-v":
        mostrar_version()
        return

    try:
        retriever = JsonKeyRetrieverSingleton(JSON_FILE)
        processor = PaymentProcessor(retriever)

        if args[0] == "pagar":
            processor.realizar_pago()
        elif args[0] == "listar":
            processor.listar_pagos()
        else:
            print("Comando no reconocido.")
            mostrar_uso()
    except ValueError as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
