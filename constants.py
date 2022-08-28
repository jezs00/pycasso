# Enums for constants to be used throughout pycasso

from enum import Enum


class Providers(Enum):
    HISTORIC = 0
    STABLE = 1
    DALLE = 2
    HISTORIC_AMOUNT = 1
    STABLE_AMOUNT = 0
    DALLE_AMOUNT = 0


class Stability(Enum):
    KEY = "STABILITY_KEY"
    HOST = "STABILITY_HOST"
    DEFAULT_HOST = "grpc.stability.ai:443"
