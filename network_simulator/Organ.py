class Organ:
    """
    A class representing a given organ which is available for transplant.

    Each organ has a name, a unique ID, lifetime (a maximum out of body duration),
    type matching, and a location.
    """
    def __init__(self, organ_id, organ_category, organ_type, viability, location):
        self.organ_id = organ_id
        self.organ_category = organ_category
        self.organ_type = organ_type
        self.viability = viability
        self.location = location

    def move_organ(self, new_location, cost):
        if self.viability < cost:
            print('ERROR: organ no longer viable!')
            return

        self.location = new_location
        self.viability -= cost
