import math

import streamlit as st

# --- Cost Factors ---
flute_cost_factors = {"B-flute": 1.0, "C-flute": 1.15, "BC-flute": 1.1, "E-flute": 1.2}

box_type_multipliers = {"Pizza box": 1.1, "RSC (Regular Slotted Container)": 1.0}


def volume_discount_factor(vol_k):
    # Logarithmic discount model
    alpha = 0.07
    log_v = math.log10(vol_k)
    discount = 1 - alpha * log_v
    # Clamp between 0.7 and 1.0
    return max(0.7, min(discount, 1.0))


kraft_multiplier = 1.075  # 7.5% cost increase if using kraft paper


def strength_multiplier(bct):
    if bct >= 600:
        return 1.05
    elif bct >= 400:
        return 1.02
    elif bct >= 300:
        return 1.00
    else:
        return 1.0


# --- Estimation Function ---
def estimate_box_cost(
    flute, box_type, width_mm, height_mm, bct, burst, ect, kraft, tam, vol_k
):
    blank_size_m2 = (width_mm / 1000) * (height_mm / 1000)
    base_cost = flute_cost_factors.get(flute, 1.0)
    complexity = box_type_multipliers.get(box_type, 1.0)
    strength = strength_multiplier(bct)
    vol_discount = volume_discount_factor(vol_k)
    cost = base_cost * blank_size_m2 * complexity * strength

    # Optional: Include burst and ECT influence (can be scaled more realistically)
    cost *= 1 + burst / 1000  # burst effect (small increment)
    cost *= 1 + ect / 1000  # ECT effect (small increment)
    discount = 1 - 0.2 * (tam / 100)
    logistic = 1.05
    if kraft:
        cost *= kraft_multiplier

    return round(cost * discount * vol_discount * logistic, 3)


# --- Streamlit UI ---
st.set_page_config(page_title="Box Cost Estimator", layout="centered")
st.title("Box Cost Estimator")
st.write("Customize the box specifications below to estimate the unit production cost.")

# --- Input Widgets ---
flute = st.selectbox("Flute Type", list(flute_cost_factors.keys()))
box_type = st.selectbox("Box Type", list(box_type_multipliers.keys()))

bct = st.slider(
    "Box Compression Test (BCT)", min_value=100, max_value=800, value=350, step=5
)
burst = st.slider("Burst Strength", min_value=100, max_value=500, value=275, step=5)
ect = st.slider("Edge Crush Test (ECT)", min_value=20, max_value=70, value=44, step=1)
tam = st.slider("TAM (%)", min_value=30, max_value=100, value=100, step=20)
volumn = st.slider("Volumn (k)", min_value=0, max_value=5000, value=1900, step=100)
kraft = st.checkbox("Use Kraft Paper?", value=True)

st.subheader("Blank Dimensions (mm)")
width_mm = st.number_input(
    "Width (mm)", min_value=100, max_value=3000, value=1000, step=10
)
height_mm = st.number_input(
    "Height (mm)", min_value=100, max_value=3000, value=800, step=10
)

# --- Estimate Cost ---
if st.button("Estimate Cost"):
    cost = estimate_box_cost(
        flute, box_type, width_mm, height_mm, bct, burst, ect, kraft, tam, volumn
    )

    st.subheader("Estimation Result")
    st.metric(label="Estimated Unit Cost (USD)", value=f"${cost}")

    st.markdown("#### Specification Summary")
    st.json(
        {
            "Flute": flute,
            "Box Type": box_type,
            "BCT": bct,
            "Burst": burst,
            "ECT": ect,
            "Kraft": "Yes" if kraft else "No",
            "Width (mm)": width_mm,
            "Height (mm)": height_mm,
            "TAM": tam,
        }
    )

    st.info(
        "**Note:** This is a relative estimation. Actual costs vary with materials, quantity, and supplier."
    )
