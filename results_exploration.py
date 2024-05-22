import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

results = pd.read_csv("./data/results.csv")

# results_grouped = (
#     results.groupby(["parameters", "generation"])["fitness"]
#     .agg(mean_fitness="mean", std_fitness="std")
#     .reset_index()
# )

# # Plotting with error bars (standard deviation)
# plt.figure(figsize=(10, 6))  # Adjust the figure size if necessary

# sns.lineplot(
#     x="generation",
#     y="mean_fitness",
#     hue="parameters",
#     data=results_grouped,
#     err_style="bars",
# )
# plt.show()
# Group by parameters and generation, and calculate mean and standard deviation of fitness
results_grouped = (
    results.groupby(["parameters", "generation"])["fitness"]
    .agg(mean_fitness="mean", std_fitness="std")
    .reset_index()
)
results_grouped["parameters"] = results_grouped["parameters"].apply(
    lambda x: "-".join(x)
)
# Plotting with error bars (standard deviation)
plt.figure(figsize=(10, 6))  # Adjust the figure size if necessary

# Use sns.lineplot with 'err_style="band"'
sns.lineplot(
    x="generation",
    y="mean_fitness",
    hue="parameters",
    data=results_grouped,
    err_style="band",  # Specify 'band' for error bars
    ci="sd",  # Confidence interval is set to standard deviation
)

plt.title("Fitness over Generations with Error Bars (Standard Deviation)")
plt.xlabel("Generation")
plt.ylabel("Mean Fitness")

plt.show()
