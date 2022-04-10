from enum import Enum


class PricingRequest(Enum):
    Price = "Price"
    Delta = "Delta"
    Gamma = "Gamma"
    Theta = "Theta"
    Vega = "Vega"
    Rho = "Rho"
    Phi = "Phi"
