# X=0.15 Boundary Validation Module

This module provides computational tools for validating the **X=0.15 boundary** in the Lattice-Unified Field Theory (LUFT) framework.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run validation demonstration
python x_boundary_validation.py
```

## Overview

The X=0.15 boundary represents the critical threshold in the causality/stability ratio (χ) where:
- Causality conditions remain satisfied
- Stability constraints are maintained  
- Vacuum geometric structure is coherent

## Module Contents

### `x_boundary_validation.py`

Main validation module containing:

- **`XBoundaryValidator`**: Core validation class
  - `calculate_chi(x, y)`: Calculate χ ratio for a point
  - `validate_boundary_condition(chi)`: Check if χ ≤ 0.15
  - `transform_2d_to_3d(x, y)`: Transform 2D parameters to 3D space
  - `scan_parameter_space(x_range, y_range)`: Scan for zero-violation points
  - `calculate_vacuum_geometry_metric(x, y, z)`: Compute metric tensor

- **`BoundaryCondition`**: Data class for validation results

- **`demonstrate_boundary_discovery()`**: Demonstration function

## Usage Examples

### Example 1: Validate a Single Point

```python
from validation.x_boundary_validation import XBoundaryValidator

validator = XBoundaryValidator()

# Calculate chi
chi = validator.calculate_chi(x=0.3, y=0.2)
print(f"χ = {chi:.4f}")

# Validate boundary condition
condition = validator.validate_boundary_condition(chi)
print(f"Valid: {condition.is_valid}")
print(f"Distance from boundary: {condition.distance_from_boundary:.4f}")
```

### Example 2: 2D to 3D Transformation

```python
# Transform 2D parametric coordinates to 3D physical space
x_3d, y_3d, z_3d = validator.transform_2d_to_3d(x_2d=0.3, y_2d=0.2)
print(f"2D (0.3, 0.2) → 3D ({x_3d:.4f}, {y_3d:.4f}, {z_3d:.4e})")
```

### Example 3: Parameter Space Scan

```python
# Scan parameter space for zero-violation points
results = validator.scan_parameter_space(
    x_range=(-1.0, 1.0),
    y_range=(-1.0, 1.0),
    num_points=1000  # 1000x1000 grid
)

print(f"Total points: {results['total_points']:,}")
print(f"Valid points (χ ≤ 0.15): {results['zero_violation_count']:,}")
print(f"Valid fraction: {results['valid_fraction']:.2%}")
```

### Example 4: Vacuum Geometry

```python
# Calculate vacuum geometry metric
g_00 = validator.calculate_vacuum_geometry_metric(x=0.3, y=0.2, z=0.02)
print(f"Metric component g_00 = {g_00:.6f}")
print(f"Deviation from flat space: {abs(g_00 - 1.0):.2e}")
```

## Mathematical Background

### The χ Ratio

```
χ = (E_vac / E_planck) × √(r²) / (1 + r²)
```

Where:
- E_vac ≈ 10⁻⁹ J/m³ (vacuum energy density)
- E_planck ≈ 10⁻⁹ J/m³ (characteristic scale)
- r² = x² + y²

### Boundary Condition

```
χ ≤ 0.15 + ε
```

Where ε = 0.001 (tolerance)

### 2D to 3D Transformation

```
x_3d = x_2d
y_3d = y_2d
z_3d = √(E_vac) × (x_2d² + y_2d²) / (1 + χ)
```

## Expected Output

Running the demonstration script produces:

```
======================================================================
X=0.15 BOUNDARY VALIDATION - LUFT Grand Unification Discovery
======================================================================

Example 1: Single Point Validation
----------------------------------------------------------------------
χ = 0.100: VALID ✓ (distance from boundary: 0.050)
χ = 0.150: VALID ✓ (distance from boundary: 0.000)
χ = 0.200: INVALID ✗ (distance from boundary: 0.050)
χ = 0.250: INVALID ✗ (distance from boundary: 0.100)

Example 2: 2D to 3D Transformation
----------------------------------------------------------------------
2D (0.10, 0.10) → 3D (0.1000, 0.1000, 5.5544e-07) | χ=0.1386
2D (0.30, 0.20) → 3D (0.3000, 0.2000, 3.1165e-06) | χ=0.3191
2D (0.50, 0.50) → 3D (0.5000, 0.5000, 1.0746e-05) | χ=0.4714

Example 3: Parameter Space Scan
----------------------------------------------------------------------
Total points scanned: 10,000
Zero-violation points (χ ≤ 0.15): 188
Valid fraction: 1.88%
Boundary value: χ = 0.15

Example 4: Vacuum Geometry Metric
----------------------------------------------------------------------
3D (0.10, 0.10, 0.01) → g_00=1.034432 (deviation: 3.44e-02)
3D (0.30, 0.20, 0.02) → g_00=1.169305 (deviation: 1.69e-01)
3D (0.50, 0.50, 0.05) → g_00=1.391095 (deviation: 3.91e-01)

======================================================================
Validation Complete - X=0.15 boundary confirmed for LUFT framework
======================================================================
```

## Documentation

For complete mathematical derivation and physical interpretation, see:
- `docs/x_0.15_boundary_discovery.md` - Full documentation
- `docs/internal_metrics.md` - Technical metrics reference

## Integration with LUFT

This module is part of the LUFT (Lattice-Unified Field Theory) framework:
- Provides standard validation for causality/stability
- Enables 2D to 3D transformations in vacuum geometry
- Identifies zero-violation regions in parameter space
- Supports Grand Unification Discovery research

## License

Part of THE-IMPERIAL-CHALLENGE repository.  
© 2026 Unified Physics Research
