"""estimate_page.py
This page allows users to estimate the total cost based on trained models.
It provides inputs for standard components and custom components,
and displays the estimated total cost along with a detailed report.
It also allows users to download the cost report as an Excel file.
"""

from io import BytesIO

import joblib
import numpy as np
import pandas as pd
import streamlit as st


def render():
    if not st.session_state.get("model_trained", False):
        st.info("⚠️ Please complete Step 3 (Train & Validate) first.")
        return

    st.header("Step 4: Estimate Total Cost")

    model_selection = st.session_state.get("model_selection")
    if not model_selection:
        st.error("❌ Model selection not found. Please complete Step 3 first.")
        return

    try:
        corrugate_model = joblib.load(
            f"trained_models/corrugate_{model_selection['corrugate']}_model.pkl"
        )
        epe_model = joblib.load(
            f"trained_models/epe_{model_selection['epe']}_model.pkl"
        )
        mpp_model = joblib.load(
            f"trained_models/mpp_{model_selection['mpp']}_model.pkl"
        )
        bag_model = joblib.load(
            f"trained_models/bag_{model_selection['bag']}_model.pkl"
        )
        freight_model = joblib.load(
            f"trained_models/freight_{model_selection['freight']}_model.pkl"
        )
    except Exception as e:
        st.error(f"❌ Failed to load trained models: {e}")
        return

    def render_corrugate_box(title, key_prefix):
        st.header(title)
        weight = st.number_input(
            "Weight (g)", min_value=0.0, key=f"{key_prefix}_weight"
        )
        qty = st.number_input("Quantity", min_value=0, key=f"{key_prefix}_qty")
        return {"name": title, "material": "Corrugate", "weight": weight, "qty": qty}

    sb_info = render_corrugate_box("System Box", "sb")
    ac_info = render_corrugate_box("Accessory Box", "ac")
    kb_info = render_corrugate_box("KB Tray", "kb")

    st.subheader("📦 System Box Dimensions (for Freight Calculation)")
    length = st.number_input("Length (mm)", min_value=0.0)
    width = st.number_input("Width (mm)", min_value=0.0)
    height = st.number_input("Height (mm)", min_value=0.0)
    OD = (
        (length * width * height) / 1000000000
        if length > 0 and width > 0 and height > 0
        else 0
    )

    st.header("EPE")
    epe_weight = st.number_input("EPE Weight (g)", min_value=0.0)
    epe_qty = st.number_input("EPE Quantity", min_value=0)

    st.header("MPP")
    mpp_weight = st.number_input("MPP Weight (g)", min_value=0.0)
    mpp_qty = st.number_input("MPP Quantity", min_value=0)

    st.header("Bag")
    bag_width = st.number_input("Bag Width(mm)", min_value=0.0)
    bag_length = st.number_input("Bag Length(mm)", min_value=0.0)
    bag_area = bag_width * bag_length
    bag_qty = st.number_input("Bag Quantity", min_value=0)

    st.header("Custom Components")
    if "custom_components" not in st.session_state:
        st.session_state.custom_components = []

    if st.button("➕ Add Custom Component"):
        st.session_state.custom_components.append(
            {
                "name": f"Component {len(st.session_state.custom_components)+1}",
                "material": "Corrugate",
                "weight": 0.0,
                "qty": 0,
            }
        )

    custom_inputs = []
    deleted_indices = []

    for i, comp in enumerate(st.session_state.custom_components):
        with st.expander(f"Custom Component #{i+1}", expanded=True):
            comp["name"] = st.text_input(
                "Component Name", comp["name"], key=f"name_{i}"
            )
            comp["material"] = st.selectbox(
                "Material Type", ["Corrugate", "MPP", "Bag"], key=f"material_{i}"
            )
            if comp["material"] == "Bag":
                bw = st.number_input(
                    "Bag Width (mm)", min_value=0.0, key=f"bag_width_{i}"
                )
                bl = st.number_input(
                    "Bag Length (mm)", min_value=0.0, key=f"bag_length_{i}"
                )
                comp["feature"] = bw * bl  # Area in mm²
                comp["qty"] = st.number_input(
                    "Quantity", min_value=0, key=f"bag_qty_{i}"
                )
            else:
                comp["weight"] = st.number_input(
                    "Weight (g)", min_value=0.0, key=f"weight_{i}"
                )
                comp["qty"] = st.number_input("Quantity", min_value=0, key=f"qty_{i}")
                comp["feature"] = comp["weight"]  # Weight in g

            custom_inputs.append(comp)
            if st.button(f"❌ Remove this component", key=f"delete_{i}"):
                deleted_indices.append(i)

    if deleted_indices:
        for i in sorted(deleted_indices, reverse=True):
            st.session_state.custom_components.pop(i)
        st.rerun()

    if st.button("💰 Estimate Total Cost"):
        component_rows = []

        def add_row(name, material, feature, qty, model):
            if feature > 0:

                if material == "Bag":
                    x = feature
                    input_label = "Area (mm²)"
                else:
                    x = feature / 1000  # g → kg
                    input_label = "Weight (g)"

                unit_price = float(model.predict(np.array([[x]]))[0])
                total = unit_price * qty
                component_rows.append(
                    {
                        "Component": name,
                        "Material": material,
                        # "Weight (g)": feature,
                        "Spec": input_label,
                        "Spec Value": feature,
                        "Quantity": qty,
                        "Unit Price (USD)": round(unit_price, 2),
                        "Total Price (USD)": round(total, 2),
                    }
                )
                return total
            return 0

        add_row(
            "System Box",
            "Corrugate",
            sb_info["weight"],
            sb_info["qty"],
            corrugate_model,
        )
        add_row(
            "Accessory Box",
            "Corrugate",
            ac_info["weight"],
            ac_info["qty"],
            corrugate_model,
        )
        add_row(
            "KB Tray", "Corrugate", kb_info["weight"], kb_info["qty"], corrugate_model
        )
        add_row("EPE", "EPE", epe_weight, epe_qty, epe_model)
        add_row("MPP", "MPP", mpp_weight, mpp_qty, mpp_model)
        add_row("Bag", "Bag", bag_area, bag_qty, bag_model)

        for comp in custom_inputs:
            model = {
                "Corrugate": corrugate_model,
                "EPE": epe_model,
                "MPP": mpp_model,
                "Bag": bag_model,
            }.get(comp["material"])
            add_row(comp["name"], comp["material"], comp["feature"], comp["qty"], model)

        df_material = pd.DataFrame(
            [row for row in component_rows if row["Material"] != "Freight"]
        )

        # Add subtotal row for materials
        material_total = df_material["Total Price (USD)"].sum()
        df_material.loc[len(df_material.index)] = {
            "Component": "Materials Total",
            "Material": None,
            "Spec": None,
            "Spec Value": None,
            "Quantity": None,
            "Unit Price (USD)": None,
            "Total Price (USD)": material_total,
        }

        st.subheader("📦 Material Cost Report")
        st.dataframe(df_material)

        # Freight summary text
        st.subheader("🚚 Freight Summary")
        if OD > 0:
            freight_price = freight_model.predict(np.array([[OD]]))[0]
            st.success(
                f"Based on the entered dimensions, the box volume is {OD:.5f} m³, resulting in a predicted freight cost of ${freight_price:.2f}."
            )
        else:
            freight_price = 0
            st.info("No valid freight dimensions entered. Freight cost not included.")

        # Generate final downloadable report
        df_freight = pd.DataFrame()
        if OD > 0:
            df_freight = pd.DataFrame(
                [
                    {
                        "Component": f"Freight (OD = {OD:.5f})",
                        "Material": "Freight",
                        # "Weight (g)": np.nan,
                        "Spec": "Volume(m³)",
                        "Spec Value": OD,
                        "Quantity": 1,
                        "Unit Price (USD)": np.nan,
                        "Total Price (USD)": round(freight_price, 2),
                    }
                ]
            )

        df_report = pd.concat([df_material, df_freight], ignore_index=True)
        total_cost = df_report["Total Price (USD)"].sum()
        df_report.loc[len(df_report.index)] = {
            "Component": "Total",
            "Material": None,
            # "Weight (g)": None,
            "Spec": None,
            "Spec Value": None,
            "Quantity": None,
            "Unit Price (USD)": None,
            "Total Price (USD)": total_cost,
        }

        towrite = BytesIO()
        df_report.to_excel(
            towrite, index=False, sheet_name="CostEstimate", engine="openpyxl"
        )
        towrite.seek(0)

        st.download_button(
            label="📥 Download Cost Report (Excel)",
            data=towrite,
            file_name="cost_estimate_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        st.subheader("✅ Estimated Total Price")
        st.success(
            f"Material cost: {material_total:.2f} + Freight cost: {freight_price:.2f} = {material_total + freight_price:.2f} USD"
        )
