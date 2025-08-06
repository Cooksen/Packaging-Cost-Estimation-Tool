import matplotlib.pyplot as plt

# Define the data
# SFF MT CFF MFF AiO_top AiO_Bottom AiO_insert DT_Top DT_Bottom_wo_DiB_KB DT_DiB_KB_System
weight_MPP = [185, 195, 240, 45, 433, 723, 132]
# , 41, 77, 77]
# SFF MT CFF MFF DT_front DT_rear DT_top DT_exp_outer DT_exp_top_front DT_exp_top_back DT_exp_filler
weight_EPE = [95, 95, 100, 30, 420, 525, 85, 605, 300, 250, 25]

qty_MPP = [2, 2, 1, 1, 1, 1, 1]
# , 1, 1, 1]
qty_EPE = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]

price_MPP = [0.540, 0.66, 0.698, 0.210, 1.254, 2.230, 0.560]
# , 2.2, 2.2, 2]
price_EPE = [1.86, 2.59, 1.333, 0.859, 6.75, 6.75, 1.25, 14.8, 8.55, 6.84, 2.138]

labels_MPP = ["SFF", "MT", "CFF", "MFF", "AiO_top", "AiO_Bottom", "AiO_insert"]
#   , 'DT_Top', 'DT_Bottom', 'DT_DiB_KB_System']
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


def plot_price_vs_weight(material="EPE"):

    data_list_MPP = [
        (weight_MPP[i], price_MPP[i] / qty_MPP[i], labels_MPP[i])
        for i in range(len(weight_MPP))
    ]
    data_list_EPE = [
        (weight_EPE[i], price_EPE[i] / qty_EPE[i], labels_EPE[i])
        for i in range(len(weight_EPE))
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
    plt.title(f"YFY Price vs. Weight for {material}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("price_vs_weight.png")
    plt.show()


# Run the plot function
plot_price_vs_weight(material="MPP")
plot_price_vs_weight(material="EPE")
