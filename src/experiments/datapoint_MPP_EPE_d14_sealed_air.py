import matplotlib.pyplot as plt

# Define the data
weight_MPP = [45, 185]
weight_EPE = [30, 95]

qty_MPP = [1, 2]
qty_EPE = [1, 2]

price_MPP = [0.255, 0.77]
price_EPE = [0.99, 0.66]

labels = ["MFF", "SFF"]


def plot_price_vs_weight(material="EPE"):

    data_list_MPP = [
        (weight_MPP[i], price_MPP[i], labels[i]) for i in range(len(weight_MPP))
    ]
    data_list_EPE = [
        (weight_EPE[i], price_EPE[i], labels[i]) for i in range(len(weight_EPE))
    ]

    plt.figure(figsize=(10, 6))

    if material == "MPP":
        if data_list_MPP:
            x_mpp, y_mpp, label_mpp = zip(*data_list_MPP)
            plt.scatter(x_mpp, y_mpp, label="MPP", color="blue")
            for i in range(len(x_mpp)):
                plt.text(
                    x_mpp[i],
                    y_mpp[i],
                    label_mpp[i],
                    fontsize=9,
                    ha="right",
                    va="bottom",
                )

    else:
        if data_list_EPE:
            x_epe, y_epe, label_epe = zip(*data_list_EPE)
            plt.scatter(x_epe, y_epe, label="EPE", color="green")
            for i in range(len(x_epe)):
                plt.text(
                    x_epe[i],
                    y_epe[i],
                    label_epe[i],
                    fontsize=9,
                    ha="right",
                    va="bottom",
                )

    plt.xlabel("Weight (g)")
    plt.ylabel("Price")
    plt.title(f"Sealed Air Price vs. Weight for {material}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_vs_weight.png")
    plt.show()


# Run the plot function
plot_price_vs_weight(material="MPP")
