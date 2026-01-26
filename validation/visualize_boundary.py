#!/usr/bin/env python3
"""
Visualization tools for the X=0.15 boundary in LUFT framework.

This script generates plots showing:
1. Chi (χ) distribution in parameter space
2. Zero-violation regions
3. 2D to 3D transformation visualization
4. Boundary contours
"""

import numpy as np
from x_boundary_validation import XBoundaryValidator

try:
    import matplotlib.pyplot as plt
    from matplotlib import cm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available. Generating text-based visualizations only.")


def visualize_chi_distribution(validator, resolution=100):
    """
    Visualize the chi distribution in 2D parameter space.
    
    Args:
        validator: XBoundaryValidator instance
        resolution: Grid resolution for visualization
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib required for graphical visualization")
        return
    
    # Create parameter space grid
    x_vals = np.linspace(-1.0, 1.0, resolution)
    y_vals = np.linspace(-1.0, 1.0, resolution)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    # Calculate chi for all points
    chi_grid = np.zeros_like(X)
    for i in range(resolution):
        for j in range(resolution):
            chi_grid[i, j] = validator.calculate_chi(X[i, j], Y[i, j])
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: Chi distribution with boundary contour
    im1 = ax1.contourf(X, Y, chi_grid, levels=50, cmap='viridis')
    contour = ax1.contour(X, Y, chi_grid, levels=[0.15], colors='red', linewidths=2)
    ax1.clabel(contour, inline=True, fontsize=10, fmt='χ=0.15')
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_title('χ (Chi) Distribution in Parameter Space', fontsize=14)
    ax1.grid(True, alpha=0.3)
    cbar1 = plt.colorbar(im1, ax=ax1)
    cbar1.set_label('χ (causality/stability ratio)', fontsize=10)
    
    # Plot 2: Valid/invalid regions
    valid_grid = chi_grid <= 0.15
    im2 = ax2.contourf(X, Y, valid_grid.astype(float), levels=[0, 0.5, 1], 
                       colors=['red', 'green'], alpha=0.6)
    ax2.contour(X, Y, chi_grid, levels=[0.15], colors='black', linewidths=2)
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel('y', fontsize=12)
    ax2.set_title('Zero-Violation Regions (χ ≤ 0.15)', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', alpha=0.6, label='Valid (χ ≤ 0.15)'),
        Patch(facecolor='red', alpha=0.6, label='Invalid (χ > 0.15)')
    ]
    ax2.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('chi_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: chi_distribution.png")
    plt.close()


def visualize_2d_to_3d_transformation(validator, num_points=50):
    """
    Visualize the 2D to 3D transformation.
    
    Args:
        validator: XBoundaryValidator instance
        num_points: Number of points to visualize
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib required for graphical visualization")
        return
    
    # Create figure with 3D projection
    fig = plt.figure(figsize=(14, 6))
    
    # Subplot 1: 2D parameter space
    ax1 = fig.add_subplot(121)
    
    # Generate points
    x_2d = np.linspace(-0.5, 0.5, num_points)
    y_2d = np.linspace(-0.5, 0.5, num_points)
    X_2d, Y_2d = np.meshgrid(x_2d, y_2d)
    
    # Calculate chi for coloring
    chi_vals = np.zeros_like(X_2d)
    for i in range(num_points):
        for j in range(num_points):
            chi_vals[i, j] = validator.calculate_chi(X_2d[i, j], Y_2d[i, j])
    
    # Plot 2D space
    scatter1 = ax1.scatter(X_2d, Y_2d, c=chi_vals, cmap='coolwarm', s=20, alpha=0.6)
    ax1.set_xlabel('x (2D)', fontsize=12)
    ax1.set_ylabel('y (2D)', fontsize=12)
    ax1.set_title('2D Parameter Space', fontsize=14)
    ax1.grid(True, alpha=0.3)
    cbar1 = plt.colorbar(scatter1, ax=ax1)
    cbar1.set_label('χ', fontsize=10)
    
    # Subplot 2: 3D physical space
    ax2 = fig.add_subplot(122, projection='3d')
    
    # Transform to 3D
    X_3d = np.zeros_like(X_2d)
    Y_3d = np.zeros_like(Y_2d)
    Z_3d = np.zeros_like(X_2d)
    
    for i in range(num_points):
        for j in range(num_points):
            x3, y3, z3 = validator.transform_2d_to_3d(X_2d[i, j], Y_2d[i, j])
            X_3d[i, j] = x3
            Y_3d[i, j] = y3
            Z_3d[i, j] = z3
    
    # Plot 3D space
    scatter2 = ax2.scatter(X_3d, Y_3d, Z_3d, c=chi_vals, cmap='coolwarm', s=20, alpha=0.6)
    ax2.set_xlabel('x (3D)', fontsize=10)
    ax2.set_ylabel('y (3D)', fontsize=10)
    ax2.set_zlabel('z (3D)', fontsize=10)
    ax2.set_title('3D Physical Space', fontsize=14)
    cbar2 = plt.colorbar(scatter2, ax=ax2, pad=0.1, shrink=0.8)
    cbar2.set_label('χ', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('2d_to_3d_transformation.png', dpi=300, bbox_inches='tight')
    print("Saved: 2d_to_3d_transformation.png")
    plt.close()


def visualize_radial_profile(validator, max_radius=1.0, num_points=1000):
    """
    Visualize the radial profile of chi and identify the critical radius.
    
    Args:
        validator: XBoundaryValidator instance
        max_radius: Maximum radius to plot
        num_points: Number of points in radial direction
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Matplotlib required for graphical visualization")
        return
    
    # Calculate chi along radial direction (x=y case for simplicity)
    r_vals = np.linspace(0, max_radius, num_points)
    chi_vals = np.array([validator.calculate_chi(r/np.sqrt(2), r/np.sqrt(2)) for r in r_vals])
    
    # Find critical radius where chi = 0.15
    critical_idx = np.argmin(np.abs(chi_vals - 0.15))
    r_critical = r_vals[critical_idx]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(r_vals, chi_vals, 'b-', linewidth=2, label='χ(r)')
    ax.axhline(y=0.15, color='r', linestyle='--', linewidth=2, label='χ = 0.15 (boundary)')
    ax.axvline(x=r_critical, color='g', linestyle=':', linewidth=2, 
               label=f'Critical radius r_c ≈ {r_critical:.3f}')
    
    # Shade valid region
    ax.fill_between(r_vals, 0, 0.15, where=(chi_vals <= 0.15), 
                    alpha=0.3, color='green', label='Valid region')
    ax.fill_between(r_vals, 0.15, chi_vals, where=(chi_vals > 0.15), 
                    alpha=0.3, color='red', label='Invalid region')
    
    ax.set_xlabel('Radial coordinate r = √(x² + y²)', fontsize=12)
    ax.set_ylabel('χ (causality/stability ratio)', fontsize=12)
    ax.set_title('Radial Profile of χ and X=0.15 Boundary', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlim(0, max_radius)
    ax.set_ylim(0, max(0.5, chi_vals.max()))
    
    plt.tight_layout()
    plt.savefig('radial_profile.png', dpi=300, bbox_inches='tight')
    print("Saved: radial_profile.png")
    print(f"Critical radius: r_c ≈ {r_critical:.4f}")
    plt.close()


def text_based_visualization(validator):
    """
    Generate text-based visualization of the X=0.15 boundary.
    Works without matplotlib.
    
    Args:
        validator: XBoundaryValidator instance
    """
    print("\n" + "=" * 70)
    print("TEXT-BASED VISUALIZATION: X=0.15 BOUNDARY")
    print("=" * 70)
    print()
    
    # Create ASCII art visualization
    resolution = 40
    x_vals = np.linspace(-1.0, 1.0, resolution)
    y_vals = np.linspace(-1.0, 1.0, resolution)
    
    print("Parameter Space Map (χ values):")
    print("Legend: . = χ≤0.10, o = 0.10<χ≤0.15, * = 0.15<χ≤0.20, # = χ>0.20")
    print()
    
    for i, y in enumerate(reversed(y_vals)):
        line = ""
        for x in x_vals:
            chi = validator.calculate_chi(x, y)
            if chi <= 0.10:
                line += "."
            elif chi <= 0.15:
                line += "o"
            elif chi <= 0.20:
                line += "*"
            else:
                line += "#"
        
        if i == 0:
            line += "  y=+1.0"
        elif i == resolution // 2:
            line += "  y=0.0"
        elif i == resolution - 1:
            line += "  y=-1.0"
        
        print(line)
    
    print(" " * (resolution // 2 - 5) + "x=-1.0" + " " * 10 + "x=+1.0")
    print()


def main():
    """Generate all visualizations for the X=0.15 boundary."""
    print("=" * 70)
    print("X=0.15 BOUNDARY VISUALIZATION")
    print("=" * 70)
    print()
    
    validator = XBoundaryValidator()
    
    # Always generate text-based visualization
    text_based_visualization(validator)
    
    # Generate graphical visualizations if matplotlib is available
    if MATPLOTLIB_AVAILABLE:
        print("\nGenerating graphical visualizations...")
        print()
        
        visualize_chi_distribution(validator, resolution=200)
        visualize_2d_to_3d_transformation(validator, num_points=30)
        visualize_radial_profile(validator, max_radius=1.0, num_points=1000)
        
        print()
        print("All visualizations saved successfully!")
        print("Files created:")
        print("  - chi_distribution.png")
        print("  - 2d_to_3d_transformation.png")
        print("  - radial_profile.png")
    else:
        print("\nTo generate graphical visualizations, install matplotlib:")
        print("  pip install matplotlib")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
