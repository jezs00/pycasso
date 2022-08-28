# Enums for constants to be used throughout pycasso

from enum import Enum


class Providers(Enum):
    STABLE = 1
    DALLE = 2


class StabilityVariables(Enum):
    ENVIRONMENT = "STABILITY_KEY"
    HOST = "STABILITY_HOST"
    DEFAULT_HOST = "grpc.stability.ai:443"
