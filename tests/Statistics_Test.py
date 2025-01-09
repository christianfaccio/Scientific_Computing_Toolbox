import unittest
import math
import random
import io
import sys
import time
import os


import numpy as np
import matplotlib.pyplot as plt


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT_DIR, 'lib', 'python'))  

import stats_cpp




class TestStatisticsModule(unittest.TestCase):
    """
    A comprehensive set of tests for the C++-based 'statistics' module,
    checking correctness, comparing with NumPy, and visualizing results
    with matplotlib.
    """

    @classmethod
    def setUpClass(cls):
        """
        Called once before the entire test suite. 
        Here we can seed RNG for reproducibility or create data
        used by multiple tests.
        """
        random.seed(42)
        np.random.seed(42)

    def setUp(self):
        """
        Called before each test. 
        """
        pass

    
    def test_dataset_creation_and_integrity(self):
        """
        Basic test that verifies dataset creation, row addition, 
        column names, and dataset size.
        """
        ds = stats_cpp.Dataset()
        self.assertEqual(ds.size(), 0, "New dataset should be empty.")

        row_1 = {"A": 1.0, "B": 2.0, "C": "foo"}
        ds.addRow(row_1)

        row_2 = {"A": 3.0, "B": 4.0, "C": "bar"}
        ds.addRow(row_2)

        self.assertEqual(ds.size(), 2, "Dataset should have exactly 2 rows.")

        col_names = ds.getColumnNames()
        self.assertEqual(set(col_names), {"A", "B", "C"},
                         "Dataset columns should match the added rows.")

    
    def test_statistical_methods_normal_distribution(self):
        """
        Test mean, variance, std dev, and frequencyCount on a 
        normally-distributed random sample. Compare to theoretical values.
        """
        mu, sigma = 10.0, 3.0
        n_samples = 10_000

        samples = [random.gauss(mu, sigma) for _ in range(n_samples)]

        ds = stats_cpp.Dataset()
        for val in samples:
            ds.addRow({"X": val})

        analyzer = stats_cpp.StatisticalAnalyzer(ds)

       
        calc_mean = analyzer.mean("X")
        self.assertAlmostEqual(calc_mean, mu, delta=0.1,
            msg="Mean of large normal sample should be close to theoretical mean.")

    
        calc_variance = analyzer.variance("X")
        self.assertAlmostEqual(calc_variance, sigma**2, delta=0.5,
            msg="Variance of large normal sample should be close to theoretical variance.")

    
        calc_std = analyzer.standardDeviation("X")
        self.assertAlmostEqual(calc_std, sigma, delta=0.2,
            msg="Std dev of large normal sample should be close to theoretical value.")

      
        freq_map = analyzer.frequencyCount("X")
        total_count = sum(freq_map.values())
        self.assertEqual(total_count, n_samples, 
            "frequencyCount should capture all sample rows.")

    
    def test_median(self):
        """
        Tests the median calculation using a small set of known values.
        """
        ds = stats_cpp.Dataset()

      
        for val in [10.0, 2.0, 5.0, 7.0]:
            ds.addRow({"Val": val})

        analyzer = stats_cpp.StatisticalAnalyzer(ds)
        self.assertEqual(analyzer.median("Val"), 6.0,
                         "Median should be the average of (5.0 and 7.0).")

      
        ds.addRow({"Val": 9.0})
        self.assertEqual(analyzer.median("Val"), 7.0,
                         "Median should be the middle element (2,5,7,9,10 -> 7).")

  
    def test_correlation_matrix_and_strong_correlation(self):
        """
        Test correlationMatrix and reportStrongCorrelations 
        with well-controlled data.
        """
        ds = stats_cpp.Dataset()
        n_samples = 1000

        # X ~ Uniform(0,1)
        # Y = 2*X + 5 => Perfect linear correlation with X
        # Z ~ Uniform(0,1) => Uncorrelated with X/Y
        x_vals = [random.random() for _ in range(n_samples)]
        y_vals = [2.0*x + 5.0 for x in x_vals]
        z_vals = [random.random() for _ in range(n_samples)]

        for x, y, z in zip(x_vals, y_vals, z_vals):
            ds.addRow({"X": x, "Y": y, "Z": z})

        analyzer = stats_cpp.StatisticalAnalyzer(ds)
        col_names = ["X", "Y", "Z"]
        corr_mtx = analyzer.correlationMatrix(col_names)

        # correlationMatrix -> 3x3
        # corr(X,Y) ~ 1, corr(X,Z) ~ 0, corr(Y,Z) ~ 0
        corr_xy = corr_mtx[0, 1]
        corr_xz = corr_mtx[0, 2]
        corr_yz = corr_mtx[1, 2]

        self.assertAlmostEqual(corr_xy, 1.0, delta=0.05,
            msg="X and Y should be strongly correlated (~1.0).")
        self.assertAlmostEqual(corr_xz, 0.0, delta=0.1,
            msg="X and Z should have near-zero correlation.")
        self.assertAlmostEqual(corr_yz, 0.0, delta=0.1,
            msg="Y and Z should have near-zero correlation.")

      
        strong_threshold = 0.8
        output = analyzer.reportStrongCorrelations(col_names, strong_threshold)

        # We expect X-Y to appear as strong correlation.
        self.assertIn("X - Y", output,
            "reportStrongCorrelations should report X-Y as strongly correlated.")
        self.assertNotIn("X - Z", output,
            "X-Z correlation should not be reported.")
        self.assertNotIn("Y - Z", output,
            "Y-Z correlation should not be reported.")


    def test_empty_dataset_errors(self):
        """
        Ensure that calling methods on an empty dataset raises exceptions.
        """
        ds = stats_cpp.Dataset()
        with self.assertRaises(RuntimeError):
            _ = ds.getColumnNames()

        with self.assertRaises(RuntimeError):
            analyzer = stats_cpp.StatisticalAnalyzer(ds)
            _ = analyzer.mean("NonExistent")

    def test_invalid_column_errors(self):
        """
        Ensure that calling methods on non-existent columns raises exceptions.
        """
        ds = stats_cpp.Dataset()
        ds.addRow({"A": 1.0})
        analyzer = stats_cpp.StatisticalAnalyzer(ds)

        with self.assertRaises(Exception):
            _ = analyzer.mean("NonExistent")

        with self.assertRaises(Exception):
            _ = analyzer.correlationMatrix(["NonExistent"])

   
    def test_numpy_comparison_and_plot(self):
        """
        Compare performance & numeric consistency with NumPy,
        then plot results with matplotlib.
        This is more of a demonstration than a typical unit test.
       """
        n_samples = 200_000
        np_data = np.random.normal(loc=5.0, scale=2.0, size=n_samples)

      
        ds = stats_cpp.Dataset()
        for val in np_data:
            ds.addRow({"Rand": float(val)})

        analyzer = stats_cpp.StatisticalAnalyzer(ds)

     
        cxx_mean = analyzer.mean("Rand")
        cxx_var  = analyzer.variance("Rand")
        cxx_std  = analyzer.standardDeviation("Rand")

        np_mean = np.mean(np_data)
        np_var  = np.var(np_data)  # population variance
        np_std  = np.std(np_data)  # population std

        self.assertAlmostEqual(cxx_mean, np_mean, delta=0.01,
            msg="C++ mean should match NumPy mean within tolerance.")
        self.assertAlmostEqual(cxx_var, np_var, delta=0.05,
            msg="C++ variance should match NumPy variance within tolerance.")
        self.assertAlmostEqual(cxx_std, np_std, delta=0.01,
            msg="C++ std dev should match NumPy std dev within tolerance.")

       
        # Time the C++ calls
        t0 = time.time()
        _ = analyzer.mean("Rand")
        _ = analyzer.variance("Rand")
        _ = analyzer.standardDeviation("Rand")
        cxx_time = time.time() - t0

        # Time the NumPy calls
        t1 = time.time()
        _ = np.mean(np_data)
        _ = np.var(np_data)
        _ = np.std(np_data)
        np_time = time.time() - t1

        print("\nPerformance Comparison:")
        print(f"  C++ (bindings) time: {cxx_time:.4f} seconds")
        print(f"  NumPy time:          {np_time:.4f} seconds\n")

       

   
        plt.figure(figsize=(8,6))
        plt.hist(np_data, bins=50, density=True, alpha=0.6, label='Data Histogram')

        # Add small offset to x position of one line to make both visible
        plt.axvline(cxx_mean - 0.02, color='r', linestyle='--', label=f"C++ Mean={cxx_mean:.2f}")
        plt.axvline(np_mean + 0.02, color='g', linestyle='-', label=f"NumPy Mean={np_mean:.2f}")

        plt.title("Distribution of Random Data (normal loc=5.0, scale=2.0)")
        plt.xlabel("Value")
        plt.ylabel("Density")
        plt.legend()
        plt.tight_layout()
        plt.savefig('histogram_comparison.png')
        plt.close()

        # Create a second column correlated with "Rand"
        # e.g., CorrRand = Rand * 2 + some noise
        corr_col = np_data * 2.0 + np.random.normal(0, 1, n_samples)

        # Add to dataset. Because we already added rows, we can't just do it row by row
        # unless we create a brand new dataset. Let's do that for demonstration:
        ds2 = stats_cpp.Dataset()
        for val, val2 in zip(np_data, corr_col):
            ds2.addRow({"Rand": float(val), "CorrRand": float(val2)})

        analyzer2 = stats_cpp.StatisticalAnalyzer(ds2)
        col_names = ["Rand", "CorrRand"]
        corr_matrix = analyzer2.correlationMatrix(col_names)
        
        # Compare with NumPy corrcoef
        np_corr = np.corrcoef(np_data, corr_col)

     
        self.assertAlmostEqual(corr_matrix[0, 1], np_corr[0, 1], delta=0.01,
            msg="C++ correlation should match NumPy correlation within tolerance.")


if __name__ == "__main__":
    unittest.main()
