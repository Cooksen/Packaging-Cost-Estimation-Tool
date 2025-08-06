# A simple cost estimation tool for corrugated boxes

# Define base cost factors for flute types (per square meter)
flute_cost_factors = {"B-flute": 1.0, "C-flute": 1.1, "BC-flute": 1.3}

# Define box type complexity multipliers
box_type_multipliers = {"Pizza box": 1.2, "RSC": 1.0}


# Define strength adjustment factor based on BCT
def strength_multiplier(bct):
    if bct >= 600:
        return 1.3
    elif bct >= 400:
        return 1.2
    elif bct >= 300:
        return 1.1
    else:
        return 1.0


# Cost estimation function
def estimate_box_cost(box_spec):
    flute = box_spec["flute"]
    box_type = box_spec["box_type"]
    blank_size_m2 = (box_spec["blank_width_mm"] / 1000) * (
        box_spec["blank_height_mm"] / 1000
    )
    bct = box_spec["bct"]

    base_cost = flute_cost_factors.get(flute, 1.0)
    complexity = box_type_multipliers.get(box_type, 1.0)
    strength = strength_multiplier(bct)

    estimated_cost = base_cost * blank_size_m2 * complexity * strength
    return round(estimated_cost, 3)


# Example box specifications
box_specs = [
    {
        "box_type": "Pizza box",
        "flute": "B-flute",
        "ect": 44,
        "burst": 275,
        "bct": 310,
        "blank_width_mm": 1032,
        "blank_height_mm": 856,
    },
    {
        "box_type": "RSC",
        "flute": "C-flute",
        "ect": 44,
        "burst": 275,
        "bct": 350,
        "blank_width_mm": 1802,
        "blank_height_mm": 650,
    },
]

# Estimate and print costs
for spec in box_specs:
    cost = estimate_box_cost(spec)
    print(f"Estimated cost for {spec['box_type']} ({spec['flute']}): ${cost}")
