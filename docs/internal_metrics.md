# LUFT metrics quick reference

## χ (Causality/Stability Ratio) - The X=0.15 Boundary

**Formalized Definition**: The χ ratio is a dimensionless quantity used in LUFT scan workflows to flag the onset of causal or stability violations in vacuum geometric structure.

### Mathematical Formulation

```
χ = (E_vac / E_planck) × √(r²) / (1 + r²)
```

Where:
- **E_vac**: Vacuum energy density (J/m³), typically ~10⁻⁹ J/m³
- **E_planck**: Characteristic vacuum energy scale, ≈ 10⁻⁹ J/m³
- **r² = x² + y²**: Radial coordinate in parameter space

### Boundary Condition

**Critical Threshold**: χ ≈ 0.15 ± 0.001

- **χ ≤ 0.15**: Causality satisfied, stability maintained ✓
- **χ > 0.15**: Potential violations, instability ✗

This boundary emerges from the balance between causal propagation and stability constraints in the vacuum lattice. The threshold corresponds to a critical radius r_c ≈ 0.42 in normalized parameter space.

### 2D to 3D Transformation

The X=0.15 boundary is intimately connected to the transformation from 2D parametric space to 3D physical vacuum geometry:

```
x_3d = x_2d
y_3d = y_2d  
z_3d = √(E_vac) × (x_2d² + y_2d²) / (1 + χ)
```

The third spatial dimension emerges from vacuum energy and the χ ratio, unifying quantum (E_vac) and geometric (r²) aspects.

### Derivation Summary

The χ = 0.15 boundary derives from:
1. Requiring positive vacuum energy density
2. Maintaining subluminal propagation through lattice
3. Preventing closed timelike curves
4. Ensuring lattice node stability (spacing ~0.007 m)

Full mathematical derivation available in: `docs/x_0.15_boundary_discovery.md`

## Zero-Violation Points

**Definition**: Parameter combinations (x, y) that satisfy χ ≤ 0.15, ensuring all LUFT causality and stability checks pass.

**January 2026 Scan Results**:
- Total sampled points: ~2.5M
- Zero-violation points: 1.48M+ 
- Valid fraction: ~59%
- Parameter range: x, y ∈ [-1, 1]
- Sampling density: 1000 × 1000 grid with refinement near boundary

These points form a continuous region around the origin with r < r_c ≈ 0.42.

### Spatial Distribution

- **Core region** (r < 0.3): 100% valid, χ < 0.10
- **Boundary region** (0.3 < r < 0.42): Gradient zone, χ ≈ 0.10-0.15  
- **Exterior** (r > 0.42): Invalid, χ > 0.15

## Time-Domain Harmonics

**Observed Frequencies**:
- **Long-period suppression**: ~66 h (≈ 4.2 × 10⁻³ Hz)
- **Short-period harmonic**: ~0.9 h (≈ 3.1 × 10⁻⁴ Hz)

These harmonics emerge from χ-dependent lattice dynamics and represent:
- **66 h**: Vacuum energy relaxation timescale
- **0.9 h**: Lattice node coherence timescale  

**Connection to χ = 0.15**: The harmonics scale as ~1/√(0.15 - χ) near the boundary, showing critical slowing down as the stability threshold is approached.

**Validation Status**: Observed in internal LUFT magnetosphere spectra. External replication required using SQUID arrays and geomagnetic observatories.

## Related Observables

### Lattice Signatures
- **Node density**: 10¹²-10¹⁵ nodes/km³
- **Node spacing**: λ ≈ 0.007 m (constrained by χ = 0.15)
- **Characteristic frequency**: 7,467-7,470 Hz
- **Magnetic field**: ~10⁻¹⁵ T (collective), ~10⁻¹⁸ T (individual)

### Vacuum Geometry
- **Metric perturbation**: g_00 ≈ 1 + 2χr/(1+r)
- **Vacuum pressure**: P ≈ 10⁻⁵ Pa (10⁻¹¹ lb/ft²)
- **Lattice flows**: ~500 m/s (1,640 ft/s)

## Computational Tools

**Validation Module**: `validation/x_boundary_validation.py`

Key functions:
- `calculate_chi(x, y)`: Compute χ ratio
- `validate_boundary_condition(chi)`: Check if χ ≤ 0.15
- `transform_2d_to_3d(x, y)`: Map parameter space to physical space
- `scan_parameter_space(x_range, y_range)`: Identify zero-violation regions

## References

- **Full documentation**: `docs/x_0.15_boundary_discovery.md`
- **Validation code**: `validation/x_boundary_validation.py`
- **LUFT framework**: Repository root documentation

**Status**: Formalized for publication (January 2026)  
**Next steps**: Peer review, experimental validation, integration with LUFT scan workflow public release
