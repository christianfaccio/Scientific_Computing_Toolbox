
import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Add the build folder to sys.path
script_dir = os.path.dirname(__file__)  # Directory of the current script
build_dir = os.path.join(script_dir, '../build/src/Interpolation_Module/')  # Adjust the relative path
sys.path.append(build_dir)

# Now you can import your module
import interpolation 

# Function to generate random data
def random_data_generator(min, max, num_points, seed=None):
    x = np.linspace(min, max, num_points)
    y = np.random.rand(num_points)
    return pd.DataFrame({'x': x, 'y': y})

# Function to generate the data
def data_generator(min, max, num_points, function):
    x = np.linspace(min, max, num_points)
    y = function(x)
    return pd.DataFrame({'x': x, 'y': y})

def sparse_points_generator(min, max, n):
    sparse_x = np.linspace(min, max, n)
    sparse_y = [np.sin(x_i) for x_i in sparse_x]
    sparse_data = pd.DataFrame({'x': sparse_x, 'y': sparse_y})
    return interpolation.df_to_set_of_points(sparse_data)

# Function to sample values without repetition and ordering them
def sample_values(values, num_samples):
    values = np.array(values)  # Ensure values is a NumPy array
    x = np.random.choice(values, num_samples-2, replace=False)
    x = list(x)  # Convert NumPy array to list
    # Ensure the first and last elements of values are included
    if values[0] not in x:
        x.append(values[0])
    if values[-1] not in x:
        x.append(values[-1])
    x.sort()
    y = [np.sin(x_i) for x_i in x]
    data = pd.DataFrame({'x': x, 'y': y})
    return data





# Testing interpolations
interpolation.InterpolationTester().run_tests()

print("Testing the interpolation module with random data in the interval (0,10)...")

# Generating some random data and interpolating it
random_data = random_data_generator(0, 10, 20, seed = 17)
random_points = interpolation.df_to_set_of_points(random_data)
plt.plot(random_data['x'], random_data['y'], 'ro', label='Data points')
plt.title("Random Data")
plt.legend()
plt.savefig('../output/random_data_generated.png')

# Interpolating the data
linear_interpolation = interpolation.LinearInterpolation(random_points)
lagrange_interpolation = interpolation.Lagrange(random_points)
newton_interpolation = interpolation.Newton(random_points)
spline_interpolation = interpolation.SplineInterpolation(random_points)


x = np.linspace(0, 10, 1000)
y_linear = [linear_interpolation.interpolate(x_i) for x_i in x]
y_lagrange = [lagrange_interpolation.interpolate(x_i) for x_i in x]
y_newton = [newton_interpolation.interpolate(x_i) for x_i in x]
y_spline = [spline_interpolation.interpolate(x_i) for x_i in x]

print("Plotting interpolations for 1000 random points in the interval [0, 10]...")

fig, axs = plt.subplots(2, 2)
fig.suptitle('Interpolations')

# External legend elements
external_legend_elements = [plt.Line2D([0], [0], color='red', marker='o', linestyle='None', label='Data points')]

# Subplot 1: Linear interpolation
axs[0, 0].plot(random_data['x'], random_data['y'], 'ro')  # Red points without legend
axs[0, 0].plot(x, y_linear, label='Linear interpolation')
axs[0, 0].legend()

# Subplot 2: Lagrange interpolation
axs[0, 1].plot(random_data['x'], random_data['y'], 'ro')  # Red points without legend
axs[0, 1].plot(x, y_lagrange, label='Lagrange interpolation')
axs[0, 1].legend()

# Subplot 3: Newton interpolation
axs[1, 0].plot(random_data['x'], random_data['y'], 'ro')  # Red points without legend
axs[1, 0].plot(x, y_newton, label='Newton interpolation')
axs[1, 0].legend()

# Subplot 4: Spline interpolation
axs[1, 1].plot(random_data['x'], random_data['y'], 'ro')  # Red points without legend
axs[1, 1].plot(x, y_spline, label='Spline interpolation')
axs[1, 1].legend()

# Add the external legend in the top-left corner
fig.legend(handles=external_legend_elements, loc='upper left', bbox_to_anchor=(0, 1), frameon=False)

plt.tight_layout()
plt.savefig('../output/random_data_interpolations.png')



print("Analyzing the interpolations with y=sin(x) as generator function...")

# Generating data with sin function
data = data_generator(0, 10, 20, np.sin)
points = interpolation.df_to_set_of_points(data)

sparse_data = sample_values(data['x'], 5)
sparse_points = interpolation.df_to_set_of_points(sparse_data)

# plotting the data
plt.plot(data['x'], data['y'], 'ro', label='Data points')
plt.plot(sparse_data['x'], sparse_data['y'], 'bo', label='Sampled points')
plt.title("Data with sin(x) as generator function")
plt.legend()
plt.savefig('../output/sin_data_generated.png')

linear_interpolation = interpolation.LinearInterpolation(sparse_points)
lagrange_interpolation = interpolation.Lagrange(sparse_points)
newton_interpolation = interpolation.Newton(sparse_points)
spline_interpolation = interpolation.SplineInterpolation(sparse_points)

x = np.linspace(min(sparse_data['x']), max(sparse_data['x']), 1000)
y_linear = [linear_interpolation.interpolate(x_i) for x_i in x]
y_lagrange = [lagrange_interpolation.interpolate(x_i) for x_i in x]
y_newton = [newton_interpolation.interpolate(x_i) for x_i in x]
y_spline = [spline_interpolation.interpolate(x_i) for x_i in x]

print("Plotting interpolations for 1000 points in the interval [0, 10]...")

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle('Interpolations')

# External legend elements
external_legend_elements = [
    plt.Line2D([0], [0], color='red', marker='o', linestyle='None', label='True points'),
    plt.Line2D([0], [0], color='blue', marker='o', linestyle='None', label='Sampled points'),
    plt.Line2D([0], [0], color='green', linestyle='-', label='Interpolation')
]

# Subplot 1: Linear interpolation
axs[0, 0].plot(data['x'], data['y'], 'ro')  # True points
axs[0, 0].plot(sparse_data['x'], sparse_data['y'], 'bo')  # Sampled points
axs[0, 0].plot(x, y_linear, 'g-')  # Interpolation
axs[0, 0].set_title("Linear Interpolation")

# Subplot 2: Lagrange interpolation
axs[0, 1].plot(data['x'], data['y'], 'ro')  # True points
axs[0, 1].plot(sparse_data['x'], sparse_data['y'], 'bo')  # Sampled points
axs[0, 1].plot(x, y_lagrange, 'g-')  # Interpolation
axs[0, 1].set_title("Lagrange Interpolation")

# Subplot 3: Newton interpolation
axs[1, 0].plot(data['x'], data['y'], 'ro')  # True points
axs[1, 0].plot(sparse_data['x'], sparse_data['y'], 'bo')  # Sampled points
axs[1, 0].plot(x, y_newton, 'g-')  # Interpolation
axs[1, 0].set_title("Newton Interpolation")

# Subplot 4: Spline interpolation
axs[1, 1].plot(data['x'], data['y'], 'ro')  # True points
axs[1, 1].plot(sparse_data['x'], sparse_data['y'], 'bo')  # Sampled points
axs[1, 1].plot(x, y_spline, 'g-')  # Interpolation
axs[1, 1].set_title("Spline Interpolation")

# Add the external legend outside the subplots
fig.legend(handles=external_legend_elements, loc='upper left', bbox_to_anchor=(0.1, 1), frameon=False)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit the legend and title
plt.savefig('../output/sin_data_interpolations.png')



print("Starting Accuracy Analysis...")
print("Linear Interpolation mae: " + str(interpolation.AnalysisInterpolation().AccuracyAnalysis(points, sparse_points, "linear")))
print("Lagrange Interpolation mae: " + str(interpolation.AnalysisInterpolation().AccuracyAnalysis(points, sparse_points, "lagrange")))
print("Newton Interpolation mae: " + str(interpolation.AnalysisInterpolation().AccuracyAnalysis(points, sparse_points, "newton")))
print("Spline Interpolation mae: " + str(interpolation.AnalysisInterpolation().AccuracyAnalysis(points, sparse_points, "cubic_spline")))

print("Starting Efficiency Analysis...")
interpolation.AnalysisInterpolation().EfficiencyAnalysis(points, sparse_points, "linear")
interpolation.AnalysisInterpolation().EfficiencyAnalysis(points, sparse_points, "lagrange")
interpolation.AnalysisInterpolation().EfficiencyAnalysis(points, sparse_points, "newton")
interpolation.AnalysisInterpolation().EfficiencyAnalysis(points, sparse_points, "cubic_spline")

print("Starting Order of Convergence Analysis duplicating points for 5 times starting from 4...")

n_points = [4, 8, 16, 32, 64]

vec_sparse_points = []
linear_ooc = []
lagrangge_ooc = []
newton_ooc = []
spline_ooc = []

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle('Interpolations')

n_colors = ['green', 'orange', 'purple', 'brown', 'pink']  # Ensure the colors are sufficient

# External legend elements
external_legend_elements = [
    plt.Line2D([0], [0], color='red', marker='o', linestyle='None', label='True points'),
    plt.Line2D([0], [0], color=n_colors[0], linestyle='-', label='4 points'),
    plt.Line2D([0], [0], color=n_colors[1], linestyle='-', label='8 points'),
    plt.Line2D([0], [0], color=n_colors[2], linestyle='-', label='16 points'),
    plt.Line2D([0], [0], color=n_colors[3], linestyle='-', label='32 points'),
    plt.Line2D([0], [0], color=n_colors[4], linestyle='-', label='64 points')
]

# Plotting original data points
axs[0, 0].plot(data['x'], data['y'], 'ro', label='Data points')
axs[0, 1].plot(data['x'], data['y'], 'ro', label='Data points')
axs[1, 0].plot(data['x'], data['y'], 'ro', label='Data points')
axs[1, 1].plot(data['x'], data['y'], 'ro', label='Data points')

for i in range(len(n_points)):
    sparse_points = sparse_points_generator(0, 10, n_points[i])
    vec_sparse_points.append(sparse_points)
    if i != 0:
        linear_ooc.append(interpolation.AnalysisInterpolation().OrderConvergenceAnalysis(points, vec_sparse_points[i-1], vec_sparse_points[i], "linear"))
        lagrangge_ooc.append(interpolation.AnalysisInterpolation().OrderConvergenceAnalysis(points, vec_sparse_points[i-1], vec_sparse_points[i], "lagrange"))
        newton_ooc.append(interpolation.AnalysisInterpolation().OrderConvergenceAnalysis(points, vec_sparse_points[i-1], vec_sparse_points[i], "newton"))
        spline_ooc.append(interpolation.AnalysisInterpolation().OrderConvergenceAnalysis(points, vec_sparse_points[i-1], vec_sparse_points[i], "cubic_spline"))
    linear_interpolation = interpolation.LinearInterpolation(sparse_points)
    lagrange_interpolation = interpolation.Lagrange(sparse_points)
    newton_interpolation = interpolation.Newton(sparse_points)
    spline_interpolation = interpolation.SplineInterpolation(sparse_points)
    y_linear = [linear_interpolation.interpolate(x_i) for x_i in x]
    y_lagrange = [lagrange_interpolation.interpolate(x_i) for x_i in x]
    y_newton = [newton_interpolation.interpolate(x_i) for x_i in x]
    y_spline = [spline_interpolation.interpolate(x_i) for x_i in x]
    axs[0, 0].plot(x, y_linear, color=n_colors[i % len(n_colors)], label=f'n = {n_points[i]}')
    axs[0, 1].plot(x, y_lagrange, color=n_colors[i % len(n_colors)], label=f'n = {n_points[i]}')
    axs[1, 0].plot(x, y_newton, color=n_colors[i % len(n_colors)], label=f'n = {n_points[i]}')
    axs[1, 1].plot(x, y_spline, color=n_colors[i % len(n_colors)], label=f'n = {n_points[i]}')

# Adding subtitles
axs[0, 0].set_title('Linear Interpolation')
axs[0, 1].set_title('Lagrange Interpolation')
axs[1, 0].set_title('Newton Interpolation')
axs[1, 1].set_title('Spline Interpolation')

# Add the external legend
fig.legend(handles=external_legend_elements, loc='upper left', bbox_to_anchor=(0.1, 1), ncol=3, frameon=False, fontsize='small')

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for the legend
plt.savefig('../output/interpolations_with_different_npoints.png')


# Printing ooc
print("Linear Interpolation Order of Convergence: " + str(linear_ooc))
print("Lagrange Interpolation Order of Convergence: " + str(lagrangge_ooc))
print("Newton Interpolation Order of Convergence: " + str(newton_ooc))
print("Spline Interpolation Order of Convergence: " + str(spline_ooc))

# Plotting ooc
fig, axs = plt.subplots(2, 2)
fig.suptitle('Order of Convergence')
external_legend_elements = [
    plt.Line2D([0], [0], color = 'blue',marker = 'o', linestyle='-', label = 'Error')
]
axs[0, 0].plot(n_points[1:], linear_ooc, 'o-', color = 'blue')
axs[0, 1].plot(n_points[1:], lagrangge_ooc, 'o-', color = 'blue')
axs[1, 0].plot(n_points[1:], newton_ooc, 'o-', color = 'blue')
axs[1, 1].plot(n_points[1:], spline_ooc, 'o-', color = 'blue')
axs[0, 0].set_title('Linear Interpolation')
axs[0, 1].set_title('Lagrange Interpolation')
axs[1, 0].set_title('Newton Interpolation')
axs[1, 1].set_title('Spline Interpolation')
fig.legend(handles=external_legend_elements, loc='upper left', bbox_to_anchor=(0, 1), frameon=False)
plt.tight_layout()
plt.savefig('../output/order_of_convergence.png')

