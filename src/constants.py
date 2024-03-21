from dataclasses import dataclass

STERILIZER_COORDINATES = (450, 80, 50)  # Micrometers  # TODO
PINHOLE_COORDINATES = (71, 0, 50)
PETRI_DISH_DEPTH = 110  # Micrometers # TODO Check depth
WELL_DEPTH = 90  # Micrometers # TODO Check depth
CAMERA_POS_OFFSET = 50  # Micrometers # TODO Find real value
IMAGE_COORDINATES = [
    [136, 62],
    [136, -58],
    [250, 62],
    [250, -58],
    [364, -58],
    [480, -58],
]


@dataclass
class Colony:
    dish: str
    x: float
    y: float


@dataclass
class PetriDish:
    id: int
    x: int
    y: int


@dataclass
class Well:
    id: str
    x: float
    y: float
    has_sample: bool
    origin: str


PETRI_DISHS = [
    PetriDish(id=1, x=2600, y=-2460),
    PetriDish(id=2, x=7100, y=-2460),
    PetriDish(id=3, x=11600, y=-2460),
    PetriDish(id=4, x=16100, y=-2460),
    PetriDish(id=5, x=2600, y=2290),
    PetriDish(id=6, x=7100, y=2290),
]

WELLS = [
    Well(id="A1", x=256.94, y=21.56, has_sample=False, origin=None),
    Well(id="A2", x=266.01, y=21.56, has_sample=False, origin=None),
    Well(id="A3", x=275.08, y=21.56, has_sample=False, origin=None),
    Well(id="A4", x=284.15, y=21.56, has_sample=False, origin=None),
    Well(id="A5", x=293.22, y=21.56, has_sample=False, origin=None),
    Well(id="A6", x=302.29, y=21.56, has_sample=False, origin=None),
    Well(id="A7", x=311.36, y=21.56, has_sample=False, origin=None),
    Well(id="A8", x=320.43, y=21.56, has_sample=False, origin=None),
    Well(id="A9", x=329.5, y=21.56, has_sample=False, origin=None),
    Well(id="A10", x=338.57, y=21.56, has_sample=False, origin=None),
    Well(id="A11", x=347.64, y=21.56, has_sample=False, origin=None),
    Well(id="A12", x=356.71, y=21.56, has_sample=False, origin=None),
    Well(id="B1", x=256.95, y=30.63, has_sample=False, origin=None),
    Well(id="B2", x=266.01, y=30.63, has_sample=False, origin=None),
    Well(id="B3", x=275.08, y=30.63, has_sample=False, origin=None),
    Well(id="B4", x=284.15, y=30.63, has_sample=False, origin=None),
    Well(id="B5", x=293.22, y=30.63, has_sample=False, origin=None),
    Well(id="B6", x=302.29, y=30.63, has_sample=False, origin=None),
    Well(id="B7", x=311.36, y=30.63, has_sample=False, origin=None),
    Well(id="B8", x=320.43, y=30.63, has_sample=False, origin=None),
    Well(id="B9", x=329.5, y=30.63, has_sample=False, origin=None),
    Well(id="B10", x=338.57, y=30.63, has_sample=False, origin=None),
    Well(id="B11", x=347.64, y=30.63, has_sample=False, origin=None),
    Well(id="B12", x=356.71, y=30.63, has_sample=False, origin=None),
    Well(id="C1", x=256.95, y=39.7, has_sample=False, origin=None),
    Well(id="C2", x=266.01, y=39.7, has_sample=False, origin=None),
    Well(id="C3", x=275.08, y=39.7, has_sample=False, origin=None),
    Well(id="C4", x=284.15, y=39.7, has_sample=False, origin=None),
    Well(id="C5", x=293.22, y=39.7, has_sample=False, origin=None),
    Well(id="C6", x=302.29, y=39.7, has_sample=False, origin=None),
    Well(id="C7", x=311.36, y=39.7, has_sample=False, origin=None),
    Well(id="C8", x=320.43, y=39.7, has_sample=False, origin=None),
    Well(id="C9", x=329.5, y=39.7, has_sample=False, origin=None),
    Well(id="C10", x=338.57, y=39.7, has_sample=False, origin=None),
    Well(id="C11", x=347.64, y=39.7, has_sample=False, origin=None),
    Well(id="C12", x=356.71, y=39.7, has_sample=False, origin=None),
    Well(id="D1", x=256.95, y=48.77, has_sample=False, origin=None),
    Well(id="D2", x=266.01, y=48.77, has_sample=False, origin=None),
    Well(id="D3", x=275.08, y=48.77, has_sample=False, origin=None),
    Well(id="D4", x=284.15, y=48.77, has_sample=False, origin=None),
    Well(id="D5", x=293.22, y=48.77, has_sample=False, origin=None),
    Well(id="D6", x=302.29, y=48.77, has_sample=False, origin=None),
    Well(id="D7", x=311.36, y=48.77, has_sample=False, origin=None),
    Well(id="D8", x=320.43, y=48.77, has_sample=False, origin=None),
    Well(id="D9", x=329.5, y=48.77, has_sample=False, origin=None),
    Well(id="D10", x=338.57, y=48.77, has_sample=False, origin=None),
    Well(id="D11", x=347.64, y=48.77, has_sample=False, origin=None),
    Well(id="D12", x=356.71, y=48.77, has_sample=False, origin=None),
    Well(id="E1", x=256.95, y=57.84, has_sample=False, origin=None),
    Well(id="E2", x=266.01, y=57.84, has_sample=False, origin=None),
    Well(id="E3", x=275.08, y=57.84, has_sample=False, origin=None),
    Well(id="E4", x=284.15, y=57.84, has_sample=False, origin=None),
    Well(id="E5", x=293.22, y=57.84, has_sample=False, origin=None),
    Well(id="E6", x=302.29, y=57.84, has_sample=False, origin=None),
    Well(id="E7", x=311.36, y=57.84, has_sample=False, origin=None),
    Well(id="E8", x=320.43, y=57.84, has_sample=False, origin=None),
    Well(id="E9", x=329.5, y=57.84, has_sample=False, origin=None),
    Well(id="E10", x=338.57, y=57.84, has_sample=False, origin=None),
    Well(id="E11", x=347.64, y=57.84, has_sample=False, origin=None),
    Well(id="E12", x=356.71, y=57.84, has_sample=False, origin=None),
    Well(id="F1", x=256.95, y=66.91, has_sample=False, origin=None),
    Well(id="F2", x=266.01, y=66.91, has_sample=False, origin=None),
    Well(id="F3", x=275.08, y=66.91, has_sample=False, origin=None),
    Well(id="F4", x=284.15, y=66.91, has_sample=False, origin=None),
    Well(id="F5", x=293.22, y=66.91, has_sample=False, origin=None),
    Well(id="F6", x=302.29, y=66.91, has_sample=False, origin=None),
    Well(id="F7", x=311.36, y=66.91, has_sample=False, origin=None),
    Well(id="F8", x=320.43, y=66.91, has_sample=False, origin=None),
    Well(id="F9", x=329.5, y=66.91, has_sample=False, origin=None),
    Well(id="F10", x=338.57, y=66.91, has_sample=False, origin=None),
    Well(id="F11", x=347.64, y=66.91, has_sample=False, origin=None),
    Well(id="F12", x=356.71, y=66.91, has_sample=False, origin=None),
    Well(id="G1", x=256.95, y=75.98, has_sample=False, origin=None),
    Well(id="G2", x=266.01, y=75.98, has_sample=False, origin=None),
    Well(id="G3", x=275.08, y=75.98, has_sample=False, origin=None),
    Well(id="G4", x=284.15, y=75.98, has_sample=False, origin=None),
    Well(id="G5", x=293.22, y=75.98, has_sample=False, origin=None),
    Well(id="G6", x=302.29, y=75.98, has_sample=False, origin=None),
    Well(id="G7", x=311.36, y=75.98, has_sample=False, origin=None),
    Well(id="G8", x=320.43, y=75.98, has_sample=False, origin=None),
    Well(id="G9", x=329.5, y=75.98, has_sample=False, origin=None),
    Well(id="G10", x=338.57, y=75.98, has_sample=False, origin=None),
    Well(id="G11", x=347.64, y=75.98, has_sample=False, origin=None),
    Well(id="G12", x=356.71, y=75.98, has_sample=False, origin=None),
    Well(id="H1", x=256.95, y=85.05, has_sample=False, origin=None),
    Well(id="H2", x=266.01, y=85.05, has_sample=False, origin=None),
    Well(id="H3", x=275.08, y=85.05, has_sample=False, origin=None),
    Well(id="H4", x=284.15, y=85.05, has_sample=False, origin=None),
    Well(id="H5", x=293.22, y=85.05, has_sample=False, origin=None),
    Well(id="H6", x=302.29, y=85.05, has_sample=False, origin=None),
    Well(id="H7", x=311.36, y=85.05, has_sample=False, origin=None),
    Well(id="H8", x=320.43, y=85.05, has_sample=False, origin=None),
    Well(id="H9", x=329.5, y=85.05, has_sample=False, origin=None),
    Well(id="H10", x=338.57, y=85.05, has_sample=False, origin=None),
    Well(id="H11", x=347.64, y=85.05, has_sample=False, origin=None),
    Well(id="H12", x=356.71, y=85.05, has_sample=False, origin=None),
]
