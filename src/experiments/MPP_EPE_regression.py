import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Define the data
weight_MPP = [185, 195, 240, 45, 433, 723, 132]
weight_EPE = [95, 95, 100, 30, 420, 525, 85, 605, 300, 250, 25]

qty_MPP = [2, 2, 1, 1, 1, 1, 1]
qty_EPE = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]

price_MPP = [0.540, 0.66, 0.698, 0.210, 1.254, 2.230, 0.560]
price_EPE = [1.86, 2.59, 1.333, 0.859, 6.75, 6.75, 1.25, 14.8, 8.55, 6.84, 2.138]

labels_MPP = ["SFF", "MT", "CFF", "MFF", "AiO_top", "AiO_Bottom", "AiO_insert"]
labels_EPE = [
    "SFF",
    "MT",
    "CFF",
    "MFF",
    "DT_front",
    "DT_rear",
    "DT_top",
    "DT_exp_outer",
    "DT_exp_top_front",
    "DT_exp_top_back",
    "DT_exp_filler",
]


def plot_price_vs_weight_with_regression(material="EPE"):
    if material == "MPP":
        weights = np.array(weight_MPP).reshape(-1, 1)
        prices = np.array([price_MPP[i] / qty_MPP[i] for i in range(len(price_MPP))])
        labels = labels_MPP
        color = "blue"
    else:
        weights = np.array(weight_EPE).reshape(-1, 1)
        prices = np.array([price_EPE[i] / qty_EPE[i] for i in range(len(price_EPE))])
        labels = labels_EPE
        color = "green"

    # Fit linear regression model
    model = LinearRegression()
    model.fit(weights, prices)
    predicted_prices = model.predict(weights)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.scatter(weights, prices, label=material, color=color)
    for i in range(len(weights)):
        plt.text(weights[i], prices[i], labels[i], fontsize=9, ha="right", va="bottom")

    # Plot regression line
    x_range = np.linspace(min(weights), max(weights), 100).reshape(-1, 1)
    y_range = model.predict(x_range)
    plt.plot(x_range, y_range, color="black", linestyle="--", label="Regression Line")

    # Regression equation
    coef = model.coef_[0]
    intercept = model.intercept_
    equation = f"Price = {coef:.4f} * Weight + {intercept:.4f}"
    plt.text(
        0.05,
        0.95,
        equation,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment="top",
    )

    plt.xlabel("Weight (g)")
    plt.ylabel("Price per Unit")
    plt.title(f"YFY Price vs. Weight with Regression for {material}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"price_vs_weight_regression_{material}.png")
    plt.show()


# Generate plots for both materials
plot_price_vs_weight_with_regression(material="MPP")
plot_price_vs_weight_with_regression(material="EPE")
