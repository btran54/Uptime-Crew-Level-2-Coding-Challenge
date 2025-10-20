import unittest
import sys
import io
from contextlib import redirect_stdout
from Asgn_2 import ProducerConsumer, verify_containers


class TestProducerConsumer(unittest.TestCase):
    """Test suite for Producer-Consumer implementation"""
    
    def run_producer_consumer(self, source_data):
        """
        Helper method to run producer-consumer and capture output
        Returns: (ProducerConsumer instance, output string)
        """
        output = io.StringIO()
        with redirect_stdout(output):
            pc = ProducerConsumer(source_data)
            pc.run()
            success = pc.verify()
        
        return pc, output.getvalue(), success
    
    def test_01_even_number_of_values(self):
        """Test Case 1: Even number of values"""
        print("\n=== Test 1: Even number of values ===")
        source_data = [1, 2.5, 3, 4.7, 5, 6.3, 7, 8.9, 9, 10.1]  # 10 elements
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 10, "Source should have 10 elements")
        self.assertEqual(len(pc.destination_container), 10, "Destination should have 10 elements")
        self.assertEqual(pc.source_container, pc.destination_container, "Data should match exactly")
        self.assertEqual(pc.shared_queue.maxsize, 5, "Queue size should be 10 // 2 = 5")
        print("✓ Test passed: Even number of values")
    
    def test_02_odd_number_of_values(self):
        """Test Case 2: Odd number of values"""
        print("\n=== Test 2: Odd number of values ===")
        source_data = [1, 2.5, 3, 4.7, 5, 6.3, 7, 8.9, 9]  # 9 elements
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 9, "Source should have 9 elements")
        self.assertEqual(len(pc.destination_container), 9, "Destination should have 9 elements")
        self.assertEqual(pc.source_container, pc.destination_container, "Data should match exactly")
        self.assertEqual(pc.shared_queue.maxsize, 4, "Queue size should be 9 // 2 = 4")
        print("✓ Test passed: Odd number of values")
    
    def test_03_small_list_less_than_queue_size(self):
        """Test Case 3: List smaller than queue capacity"""
        print("\n=== Test 3: Small list (< queue size) ===")
        source_data = [1, 2, 3]  # 3 elements, queue size will be 1
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 3, "Source should have 3 elements")
        self.assertEqual(len(pc.destination_container), 3, "Destination should have 3 elements")
        self.assertEqual(pc.shared_queue.maxsize, 1, "Queue size should be 3 // 2 = 1")
        self.assertEqual(pc.source_container, pc.destination_container, "Data should match exactly")
        print("✓ Test passed: Small list")
    
    def test_04_large_list_much_larger_than_queue(self):
        """Test Case 4: List much larger than queue capacity"""
        print("\n=== Test 4: Large list (>> queue size) ===")
        source_data = list(range(1, 101))  # 100 elements
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 100, "Source should have 100 elements")
        self.assertEqual(len(pc.destination_container), 100, "Destination should have 100 elements")
        self.assertEqual(pc.shared_queue.maxsize, 50, "Queue size should be 100 // 2 = 50")
        self.assertEqual(pc.source_container, pc.destination_container, "Data should match exactly")
        print("✓ Test passed: Large list")
    
    def test_05_empty_list(self):
        """Test Case 5: Empty list"""
        print("\n=== Test 5: Empty list ===")
        source_data = []
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass for empty list")
        self.assertEqual(len(pc.source_container), 0, "Source should be empty")
        self.assertEqual(len(pc.destination_container), 0, "Destination should be empty")
        self.assertEqual(pc.shared_queue.maxsize, 0, "Queue size should be 0 // 2 = 0")
        print("✓ Test passed: Empty list")
    
    def test_06_single_element(self):
        """Test Case 6: Single element"""
        print("\n=== Test 6: Single element ===")
        source_data = [42.5]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 1, "Source should have 1 element")
        self.assertEqual(len(pc.destination_container), 1, "Destination should have 1 element")
        self.assertEqual(pc.shared_queue.maxsize, 0, "Queue size should be 1 // 2 = 0")
        self.assertEqual(pc.source_container[0], 42.5, "Element should be 42.5")
        self.assertEqual(pc.destination_container[0], 42.5, "Element should be transferred")
        print("✓ Test passed: Single element")
    
    def test_07_two_elements(self):
        """Test Case 7: Two elements (edge case for queue size)"""
        print("\n=== Test 7: Two elements ===")
        source_data = [1.5, 2.5]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 2, "Source should have 2 elements")
        self.assertEqual(len(pc.destination_container), 2, "Destination should have 2 elements")
        self.assertEqual(pc.shared_queue.maxsize, 1, "Queue size should be 2 // 2 = 1")
        self.assertEqual(pc.source_container, pc.destination_container, "Data should match exactly")
        print("✓ Test passed: Two elements")
    
    def test_08_all_integers(self):
        """Test Case 8: All integers"""
        print("\n=== Test 8: All integers ===")
        source_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(pc.source_container, pc.destination_container, "All integers should transfer")
        self.assertTrue(all(isinstance(x, int) for x in pc.destination_container), 
                       "All elements should be integers")
        print("✓ Test passed: All integers")
    
    def test_09_all_floats(self):
        """Test Case 9: All floats"""
        print("\n=== Test 9: All floats ===")
        source_data = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(pc.source_container, pc.destination_container, "All floats should transfer")
        self.assertTrue(all(isinstance(x, float) for x in pc.destination_container), 
                       "All elements should be floats")
        print("✓ Test passed: All floats")
    
    def test_10_negative_numbers(self):
        """Test Case 10: Negative numbers"""
        print("\n=== Test 10: Negative numbers ===")
        source_data = [-1, -2.5, -3, -4.7, -5, 0, 5, 4.7, 3, 2.5, 1]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(pc.source_container, pc.destination_container, 
                        "Negative numbers should transfer correctly")
        print("✓ Test passed: Negative numbers")
    
    def test_11_duplicate_values(self):
        """Test Case 11: Duplicate values"""
        print("\n=== Test 11: Duplicate values ===")
        source_data = [5, 5, 5, 3.14, 3.14, 2.71, 2.71, 2.71]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(pc.source_container, pc.destination_container, 
                        "Duplicates should be preserved")
        self.assertEqual(pc.source_container.count(5), pc.destination_container.count(5),
                        "Duplicate count should match")
        print("✓ Test passed: Duplicate values")
    
    def test_12_very_large_dataset(self):
        """Test Case 12: Very large dataset (1000 elements)"""
        print("\n=== Test 12: Very large dataset ===")
        source_data = [i * 0.5 for i in range(1000)]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(len(pc.source_container), 1000, "Source should have 1000 elements")
        self.assertEqual(len(pc.destination_container), 1000, "Destination should have 1000 elements")
        self.assertEqual(pc.shared_queue.maxsize, 500, "Queue size should be 1000 // 2 = 500")
        self.assertEqual(pc.source_container, pc.destination_container, "Large dataset should transfer")
        print("✓ Test passed: Very large dataset")
    
    def test_13_extreme_values(self):
        """Test Case 13: Extreme values (very large and very small)"""
        print("\n=== Test 13: Extreme values ===")
        source_data = [1e10, 1e-10, -1e10, -1e-10, float('inf'), float('-inf'), 0]
        
        pc, output, success = self.run_producer_consumer(source_data)
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(pc.source_container, pc.destination_container, 
                        "Extreme values should transfer correctly")
        print("✓ Test passed: Extreme values")
    
    def test_14_verify_containers_function(self):
        """Test Case 14: Test the verify_containers helper function directly"""
        print("\n=== Test 14: verify_containers function ===")
        
        # Test matching containers
        source = [1, 2, 3, 4, 5]
        destination = [1, 2, 3, 4, 5]
        success, checks, passed, failed = verify_containers(source, destination)
        
        self.assertTrue(success, "Matching containers should pass")
        self.assertEqual(len(passed), 3, "All 3 checks should pass")
        self.assertEqual(len(failed), 0, "No checks should fail")
        
        # Test mismatched order
        source = [1, 2, 3, 4, 5]
        destination = [1, 3, 2, 4, 5]
        success, checks, passed, failed = verify_containers(source, destination)
        
        self.assertFalse(success, "Mismatched order should fail")
        self.assertEqual(len(failed), 1, "Order check should fail")
        
        # Test missing elements
        source = [1, 2, 3, 4, 5]
        destination = [1, 2, 3, 4]
        success, checks, passed, failed = verify_containers(source, destination)
        
        self.assertFalse(success, "Missing elements should fail")
        self.assertGreater(len(failed), 0, "At least one check should fail")
        
        print("✓ Test passed: verify_containers function")
    
    def test_15_queue_capacity_calculation(self):
        """Test Case 15: Queue capacity is exactly half of source"""
        print("\n=== Test 15: Queue capacity calculation ===")
        
        test_cases = [
            (10, 5),   # Even: 10 // 2 = 5
            (11, 5),   # Odd: 11 // 2 = 5
            (100, 50), # Large even
            (99, 49),  # Large odd
            (2, 1),    # Small even
            (3, 1),    # Small odd
            (1, 0),    # Single element
        ]
        
        for source_size, expected_queue_size in test_cases:
            source_data = list(range(source_size))
            pc, _, _ = self.run_producer_consumer(source_data)
            
            self.assertEqual(pc.shared_queue.maxsize, expected_queue_size,
                           f"Queue size should be {expected_queue_size} for source size {source_size}")
        
        print("✓ Test passed: Queue capacity calculation")


class TestEdgeCases(unittest.TestCase):
    """Additional edge case tests"""
    
    def test_source_container_immutability(self):
        """Test that source container is not modified during transfer"""
        print("\n=== Edge Case: Source immutability ===")
        original_data = [1, 2.5, 3, 4.7, 5]
        source_data = original_data.copy()
        
        output = io.StringIO()
        with redirect_stdout(output):
            pc = ProducerConsumer(source_data)
            pc.run()
            pc.verify()
        
        # Source should remain unchanged
        self.assertEqual(pc.source_container, original_data, 
                        "Source container should not be modified")
        print("✓ Test passed: Source immutability")
    
    def test_order_preservation(self):
        """Test that order is strictly preserved"""
        print("\n=== Edge Case: Order preservation ===")
        source_data = [10, 5, 8, 3, 9, 1, 7, 2, 6, 4]
        
        output = io.StringIO()
        with redirect_stdout(output):
            pc = ProducerConsumer(source_data)
            pc.run()
            success = pc.verify()
        
        self.assertTrue(success, "Verification should pass")
        self.assertEqual(pc.source_container, pc.destination_container,
                        "Order must be preserved exactly")
        
        # Verify element-by-element
        for i, (src, dst) in enumerate(zip(pc.source_container, pc.destination_container)):
            self.assertEqual(src, dst, f"Element at index {i} should match")
        
        print("✓ Test passed: Order preservation")


def run_tests():
    """Run all tests with detailed output"""
    print("=" * 70)
    print("PRODUCER-CONSUMER UNIT TESTS")
    print("=" * 70)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestProducerConsumer))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ ALL TESTS PASSED!")
    else:
        print("\n✗ SOME TESTS FAILED")
    
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    
    sys.exit(0 if success else 1)