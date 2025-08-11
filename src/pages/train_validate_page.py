"""train_validate_page.py
This page allows users to train and validate models for cost estimation.
It provides options to select model types and initiate training.
It also displays validation results after training is complete.
"""

import os
import subprocess

import streamlit as st
from PIL import Image


def render():
    st.header("Step 3: Train & Validate Models")

    st.subheader("📦 Component Model Selection")
    model_corrugate = st.selectbox("Corrugate model", ["linear", "svr"])
    model_epe = st.selectbox("EPE model", ["linear", "svr"])
    model_mpp = st.selectbox("MPP model", ["linear", "svr"])
    model_bag = st.selectbox("Bag model", ["linear", "svr"])

    st.subheader("🚚 Freight Cost Estimator")
    model_freight = st.selectbox("Freight model", ["linear", "svr"])

    train_button = st.button("🚀 Train All Models")

    if train_button:
        st.session_state["model_selection"] = {
            "corrugate": model_corrugate,
            "epe": model_epe,
            "mpp": model_mpp,
            "bag": model_bag,
            "freight": model_freight,
        }
        with st.status("Training & validating models...", expanded=True) as status:

            # Component training
            for component, model_type in zip(
                ["corrugate", "epe", "mpp", "bag"], [model_corrugate, model_epe, model_mpp, model_bag]
            ):
                st.write(f"🔧 Training {component} with {model_type} model...")
                subprocess.run(
                    [
                        "poetry",
                        "run",
                        "python",
                        "src/core/train_multi_input.py",
                        "--model",
                        model_type,
                        "--component",
                        component,
                    ]
                )
                subprocess.run(
                    [
                        "poetry",
                        "run",
                        "python",
                        "src/core/validate_multi_input.py",
                        "--model",
                        model_type,
                        "--component",
                        component,
                    ]
                )

            # Freight training
            st.write(f"🚚 Training freight with {model_freight} model...")
            subprocess.run(
                [
                    "poetry",
                    "run",
                    "python",
                    "src/core/train_multi_input.py",
                    "--model",
                    model_freight,
                    "--component",
                    "freight",
                ]
            )
            subprocess.run(
                [
                    "poetry",
                    "run",
                    "python",
                    "src/core/validate_multi_input.py",
                    "--model",
                    model_freight,
                    "--component",
                    "freight",
                ]
            )

            status.update(
                label="✅ All models trained!", state="complete", expanded=False
            )

        st.session_state["model_trained"] = True

        st.subheader("📈 Validation Results")
        for component, model_type in zip(
            ["corrugate", "epe", "mpp", "bag", "freight"],
            [model_corrugate, model_epe, model_mpp, model_freight],
        ):
            path = f"validation_fig/validate_{component}_{model_type}_model.png"
            if os.path.exists(path):
                st.image(
                    Image.open(path),
                    caption=f"{component.capitalize()} ({model_type.upper()})",
                )
