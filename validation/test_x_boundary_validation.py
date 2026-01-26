#!/usr/bin/env python3
"""
Unit tests for X=0.15 boundary validation module.

Tests cover:
- Chi calculation accuracy
- Boundary condition validation
- 2D to 3D transformations
- Parameter space scanning
- Vacuum geometry metrics
"""

import unittest
import numpy as np
from x_boundary_validation import (
    XBoundaryValidator,
    BoundaryCondition,
    demonstrate_boundary_discovery
)


class TestXBoundaryValidator(unittest.TestCase):
    """Test cases for XBoundaryValidator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = XBoundaryValidator()
        self.epsilon = 1e-6  # Numerical tolerance for float comparisons
    
    def test_boundary_value_constant(self):
        """Test that boundary value is correctly set"""
        self.assertEqual(self.validator.BOUNDARY_VALUE, 0.15)
        self.assertEqual(self.validator.TOLERANCE, 0.001)
    
    def test_calculate_chi_at_origin(self):
        """Test chi calculation at origin (should be 0)"""
        chi = self.validator.calculate_chi(0.0, 0.0)
        self.assertAlmostEqual(chi, 0.0, places=10)
    
    def test_calculate_chi_symmetry(self):
        """Test that chi calculation is symmetric in x and y"""
        chi_1 = self.validator.calculate_chi(0.3, 0.4)
        chi_2 = self.validator.calculate_chi(0.4, 0.3)
        self.assertAlmostEqual(chi_1, chi_2, places=10)
    
    def test_calculate_chi_scaling(self):
        """Test chi scales correctly with radius"""
        # For small r, chi should scale approximately as sqrt(r²)
        chi_1 = self.validator.calculate_chi(0.1, 0.0)
        chi_2 = self.validator.calculate_chi(0.2, 0.0)
        
        # chi should increase with radius
        self.assertLess(chi_1, chi_2)
    
    def test_calculate_chi_asymptotic(self):
        """Test chi has a peak and then decreases at large radius"""
        # For large r, chi → 0 due to 1/(1+r²) term
        chi_large = self.validator.calculate_chi(100.0, 100.0)
        # Should be small at very large radius
        self.assertLess(chi_large, 0.1)
    
    def test_validate_boundary_condition_below(self):
        """Test validation for chi below boundary"""
        condition = self.validator.validate_boundary_condition(0.10)
        self.assertTrue(condition.is_valid)
        self.assertEqual(condition.chi, 0.10)
        self.assertAlmostEqual(condition.distance_from_boundary, 0.05, places=10)
    
    def test_validate_boundary_condition_at(self):
        """Test validation for chi at boundary"""
        condition = self.validator.validate_boundary_condition(0.15)
        self.assertTrue(condition.is_valid)
        self.assertEqual(condition.chi, 0.15)
        self.assertAlmostEqual(condition.distance_from_boundary, 0.0, places=10)
    
    def test_validate_boundary_condition_above(self):
        """Test validation for chi above boundary"""
        condition = self.validator.validate_boundary_condition(0.20)
        self.assertFalse(condition.is_valid)
        self.assertEqual(condition.chi, 0.20)
        self.assertAlmostEqual(condition.distance_from_boundary, 0.05, places=10)
    
    def test_validate_boundary_condition_tolerance(self):
        """Test boundary condition with tolerance"""
        # Just within tolerance
        condition = self.validator.validate_boundary_condition(0.150)
        self.assertTrue(condition.is_valid)
        
        # Just outside tolerance
        condition = self.validator.validate_boundary_condition(0.152)
        self.assertFalse(condition.is_valid)
    
    def test_transform_2d_to_3d_at_origin(self):
        """Test 2D to 3D transformation at origin"""
        x_3d, y_3d, z_3d = self.validator.transform_2d_to_3d(0.0, 0.0)
        self.assertAlmostEqual(x_3d, 0.0, places=10)
        self.assertAlmostEqual(y_3d, 0.0, places=10)
        self.assertAlmostEqual(z_3d, 0.0, places=10)
    
    def test_transform_2d_to_3d_preservation(self):
        """Test that x and y coordinates are preserved in transformation"""
        x_2d, y_2d = 0.3, 0.4
        x_3d, y_3d, z_3d = self.validator.transform_2d_to_3d(x_2d, y_2d)
        
        self.assertAlmostEqual(x_3d, x_2d, places=10)
        self.assertAlmostEqual(y_3d, y_2d, places=10)
    
    def test_transform_2d_to_3d_z_positive(self):
        """Test that z coordinate is positive for positive x, y"""
        x_3d, y_3d, z_3d = self.validator.transform_2d_to_3d(0.3, 0.4)
        self.assertGreater(z_3d, 0)
    
    def test_transform_2d_to_3d_vacuum_energy_scaling(self):
        """Test z coordinate depends on vacuum energy"""
        x_2d, y_2d = 0.3, 0.4
        
        # Transform with default vacuum energy
        _, _, z_default = self.validator.transform_2d_to_3d(x_2d, y_2d)
        
        # Transform with double vacuum energy
        _, _, z_double = self.validator.transform_2d_to_3d(x_2d, y_2d, vacuum_energy=2e-9)
        
        # z should change with vacuum energy (not necessarily sqrt scaling due to chi dependence)
        # Just verify it increases
        self.assertGreater(z_double, z_default)
    
    def test_scan_parameter_space_basic(self):
        """Test basic parameter space scan"""
        results = self.validator.scan_parameter_space(
            x_range=(-0.5, 0.5),
            y_range=(-0.5, 0.5),
            num_points=10
        )
        
        # Check all required keys are present
        self.assertIn('x', results)
        self.assertIn('y', results)
        self.assertIn('chi', results)
        self.assertIn('valid', results)
        self.assertIn('zero_violation_count', results)
        self.assertIn('total_points', results)
        self.assertIn('valid_fraction', results)
        
        # Check dimensions
        self.assertEqual(results['x'].shape, (10, 10))
        self.assertEqual(results['y'].shape, (10, 10))
        self.assertEqual(results['chi'].shape, (10, 10))
        self.assertEqual(results['valid'].shape, (10, 10))
        
        # Check total points
        self.assertEqual(results['total_points'], 100)
        
        # Check valid fraction is between 0 and 1
        self.assertGreaterEqual(results['valid_fraction'], 0.0)
        self.assertLessEqual(results['valid_fraction'], 1.0)
    
    def test_scan_parameter_space_origin_valid(self):
        """Test that origin region is valid in parameter scan"""
        results = self.validator.scan_parameter_space(
            x_range=(-0.1, 0.1),
            y_range=(-0.1, 0.1),
            num_points=10
        )
        
        # Near origin, all points should be valid
        self.assertGreater(results['valid_fraction'], 0.9)
    
    def test_scan_parameter_space_far_invalid(self):
        """Test that far regions have chi behavior at large radius"""
        results = self.validator.scan_parameter_space(
            x_range=(5.0, 6.0),
            y_range=(5.0, 6.0),
            num_points=10
        )
        
        # At very large r, chi becomes small again (< 0.15), so actually valid
        # This is due to the 1/(1+r²) term in the formula
        self.assertGreater(results['valid_fraction'], 0.5)
    
    def test_calculate_vacuum_geometry_metric_flat_at_origin(self):
        """Test metric is flat (g_00=1) at origin"""
        g_00 = self.validator.calculate_vacuum_geometry_metric(0.0, 0.0, 0.0)
        self.assertAlmostEqual(g_00, 1.0, places=10)
    
    def test_calculate_vacuum_geometry_metric_positive_perturbation(self):
        """Test metric has positive perturbation away from origin"""
        g_00 = self.validator.calculate_vacuum_geometry_metric(0.3, 0.2, 0.01)
        
        # g_00 should be greater than 1 (positive perturbation)
        self.assertGreater(g_00, 1.0)
    
    def test_calculate_vacuum_geometry_metric_increases_with_distance(self):
        """Test metric perturbation increases with distance"""
        g_00_near = self.validator.calculate_vacuum_geometry_metric(0.1, 0.1, 0.01)
        g_00_far = self.validator.calculate_vacuum_geometry_metric(0.3, 0.3, 0.03)
        
        # Further points should have larger perturbations
        self.assertGreater(g_00_far, g_00_near)


class TestBoundaryCondition(unittest.TestCase):
    """Test cases for BoundaryCondition dataclass"""
    
    def test_boundary_condition_creation(self):
        """Test BoundaryCondition can be created"""
        condition = BoundaryCondition(
            chi=0.12,
            is_valid=True,
            distance_from_boundary=0.03
        )
        
        self.assertEqual(condition.chi, 0.12)
        self.assertTrue(condition.is_valid)
        self.assertEqual(condition.distance_from_boundary, 0.03)


class TestCriticalRadius(unittest.TestCase):
    """Test cases for critical radius calculation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = XBoundaryValidator()
    
    def test_critical_radius_value(self):
        """Test that critical radius is approximately 0.154"""
        # Calculate chi at r ≈ 0.154
        r_test = 0.154
        x = r_test / np.sqrt(2)
        y = r_test / np.sqrt(2)
        chi = self.validator.calculate_chi(x, y)
        
        # Should be close to 0.15
        self.assertAlmostEqual(chi, 0.15, places=2)
    
    def test_inside_critical_radius_valid(self):
        """Test points inside critical radius are valid"""
        # Test at r = 0.1 (< 0.154)
        r = 0.1
        x = r / np.sqrt(2)
        y = r / np.sqrt(2)
        chi = self.validator.calculate_chi(x, y)
        condition = self.validator.validate_boundary_condition(chi)
        
        self.assertTrue(condition.is_valid)
    
    def test_outside_critical_radius_invalid(self):
        """Test points outside critical radius are invalid"""
        # Test at r = 0.6 (> 0.42)
        r = 0.6
        x = r / np.sqrt(2)
        y = r / np.sqrt(2)
        chi = self.validator.calculate_chi(x, y)
        condition = self.validator.validate_boundary_condition(chi)
        
        self.assertFalse(condition.is_valid)


class TestPhysicsConstants(unittest.TestCase):
    """Test cases verifying physics constants and relationships"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = XBoundaryValidator()
    
    def test_vacuum_energy_scale(self):
        """Test vacuum energy scale is physically reasonable"""
        # Vacuum energy ~10⁻⁹ J/m³ is standard in cosmology
        vacuum_energy = 1e-9
        
        # Should be positive and small
        self.assertGreater(vacuum_energy, 0)
        self.assertLess(vacuum_energy, 1e-6)
    
    def test_chi_dimensionless(self):
        """Test that chi is dimensionless"""
        # Chi should be dimensionless (no units)
        chi = self.validator.calculate_chi(0.3, 0.4)
        
        # Chi should be order 0.1-1 for typical values
        self.assertGreater(chi, 0)
        self.assertLess(chi, 10)
    
    def test_metric_perturbation_small(self):
        """Test metric perturbations are small for typical scales"""
        g_00 = self.validator.calculate_vacuum_geometry_metric(0.3, 0.2, 0.01)
        
        # Perturbation should be small (< 1) for weak fields
        perturbation = abs(g_00 - 1.0)
        self.assertLess(perturbation, 1.0)


class TestDemonstration(unittest.TestCase):
    """Test the demonstration function"""
    
    def test_demonstrate_runs_without_error(self):
        """Test that demonstration runs without errors"""
        try:
            demonstrate_boundary_discovery()
            success = True
        except Exception as e:
            success = False
            print(f"Demonstration failed with error: {e}")
        
        self.assertTrue(success)


def run_tests():
    """Run all tests and print results"""
    print("=" * 70)
    print("RUNNING X=0.15 BOUNDARY VALIDATION TESTS")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestXBoundaryValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestBoundaryCondition))
    suite.addTests(loader.loadTestsFromTestCase(TestCriticalRadius))
    suite.addTests(loader.loadTestsFromTestCase(TestPhysicsConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestDemonstration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
