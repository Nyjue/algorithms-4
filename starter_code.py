"""
Sorting Assignment Starter Code
Implement five sorting algorithms and benchmark their performance.
"""
import time
import tracemalloc
import json
import os

# PART 1: SORTING IMPLEMENTATIONS

def bubble_sort(arr):
    """Comparison-based sort with adjacent element swapping"""
    n = len(arr)
    # Make a copy to avoid modifying the original array
    result = arr.copy()
    
    for i in range(n):
        # Flag to optimize - if no swaps, array is sorted
        swapped = False
        for j in range(0, n-i-1):
            if result[j] > result[j+1]:
                result[j], result[j+1] = result[j+1], result[j]
                swapped = True
        if not swapped:
            break
    return result

def selection_sort(arr):
    """Sort that repeatedly finds minimum element"""
    result = arr.copy()
    n = len(result)
    
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result

def insertion_sort(arr):
    """Sort that builds sorted array one element at a time"""
    result = arr.copy()
    
    for i in range(1, len(result)):
        key = result[i]
        j = i-1
        while j >= 0 and result[j] > key:
            result[j+1] = result[j]
            j -= 1
        result[j+1] = key
    return result

def merge_sort(arr):
    """Divide-and-conquer sort with merging"""
    # Base case
    if len(arr) <= 1:
        return arr.copy() if isinstance(arr, list) else arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return merge(left, right)

def merge(left, right):
    """Helper function for merge sort"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# PART 2: STABILITY DEMONSTRATION

def demonstrate_stability():
    """
    Demonstrate stability of sorting algorithms on product data by price.
    Returns a dictionary with algorithm names as keys and boolean stability status.
    """
    # Test data: products with same price but different original order
    products = [
        {"name": "Product A", "price": 100, "id": 1},
        {"name": "Product B", "price": 90, "id": 2},
        {"name": "Product C", "price": 100, "id": 3},
        {"name": "Product D", "price": 80, "id": 4},
        {"name": "Product E", "price": 100, "id": 5}
    ]
    
    algorithms = {
        "Bubble Sort": bubble_sort_products,
        "Selection Sort": selection_sort_products,
        "Insertion Sort": insertion_sort_products,
        "Merge Sort": merge_sort_products
    }
    
    stability_results = {}
    
    print("\n" + "="*60)
    print("STABILITY DEMONSTRATION")
    print("="*60)
    
    for name, algo_func in algorithms.items():
        # Sort by price only
        sorted_products = algo_func(products.copy(), key="price")
        
        # Check stability: for equal prices, original order should be preserved
        stable = check_stability(products, sorted_products)
        stability_results[name] = stable
        
        # Print demonstration
        print(f"\n{name} - Stable: {stable}")
        if not stable:
            print("  Note: Equal price items may have been reordered")
        else:
            print("  ✓ Preserves order of equal-price items")
    
    return stability_results

def check_stability(original, sorted_list):
    """Helper to check if sort was stable"""
    # Group by price
    price_groups = {}
    for i, item in enumerate(original):
        price = item["price"]
        if price not in price_groups:
            price_groups[price] = []
        price_groups[price].append((i, item["id"]))
    
    # Check if relative order preserved within each price group
    for price, items in price_groups.items():
        # Get original order of ids
        orig_ids = [id for _, id in items]
        
        # Get order in sorted list
        sorted_ids = [item["id"] for item in sorted_list if item["price"] == price]
        
        # Check if order preserved
        if orig_ids != sorted_ids:
            return False
    return True

def bubble_sort_products(arr, key="price"):
    """Bubble sort for product dictionaries"""
    result = arr.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n-i-1):
            if result[j][key] > result[j+1][key]:
                result[j], result[j+1] = result[j+1], result[j]
    return result

def selection_sort_products(arr, key="price"):
    """Selection sort for product dictionaries (unstable)"""
    result = arr.copy()
    n = len(result)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if result[j][key] < result[min_idx][key]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result

def insertion_sort_products(arr, key="price"):
    """Insertion sort for product dictionaries"""
    result = arr.copy()
    for i in range(1, len(result)):
        key_item = result[i]
        j = i-1
        while j >= 0 and result[j][key] > key_item[key]:
            result[j+1] = result[j]
            j -= 1
        result[j+1] = key_item
    return result

def merge_sort_products(arr, key="price"):
    """Merge sort for product dictionaries"""
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = merge_sort_products(arr[:mid], key)
    right = merge_sort_products(arr[mid:], key)
    
    return merge_products(left, right, key)

def merge_products(left, right, key):
    """Merge helper for product dictionaries"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# PART 3: PERFORMANCE BENCHMARKING

def benchmark_algorithm(algorithm, dataset_path, algorithm_name):
    """
    Load dataset, measure execution time and memory usage.
    Returns dictionary with performance metrics.
    """
    try:
        # Load the dataset
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        
        # Extract the values to sort (assuming dataset is list of numbers or dicts with values)
        if isinstance(data[0], dict):
            # For product/order data, extract appropriate field
            if 'price' in data[0]:
                values = [item['price'] for item in data]
            elif 'value' in data[0]:
                values = [item['value'] for item in data]
            else:
                # Try to find a numeric field
                for key in data[0].keys():
                    if isinstance(data[0][key], (int, float)):
                        values = [item[key] for item in data]
                        break
                else:
                    values = list(range(len(data)))  # Fallback
        else:
            values = data.copy()
        
        # Take a subset for O(n²) algorithms to avoid long wait times
        if algorithm_name in ["Bubble Sort", "Selection Sort", "Insertion Sort"]:
            test_size = min(2000, len(values))  # Use 2000 items for quadratic algorithms
            values = values[:test_size]
        else:
            test_size = min(10000, len(values))  # Use 10000 for merge sort
            values = values[:test_size]
        
        # Measure memory before
        tracemalloc.start()
        
        # Measure time
        start_time = time.perf_counter()
        
        # Run the algorithm
        sorted_values = algorithm(values.copy())
        
        end_time = time.perf_counter()
        
        # Measure memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Verify it's sorted (optional)
        is_sorted = all(sorted_values[i] <= sorted_values[i+1] for i in range(len(sorted_values)-1))
        
        return {
            'algorithm': algorithm_name,
            'time_seconds': end_time - start_time,
            'memory_mb': peak / 10**6,  # Convert to MB
            'dataset_size': len(values),
            'valid': is_sorted
        }
    except Exception as e:
        print(f"Error benchmarking {algorithm_name} on {dataset_path}: {e}")
        return None

def benchmark_all_datasets():
    """Run benchmarks on all datasets"""
    # Check if datasets directory exists
    if not os.path.exists('datasets'):
        print("Error: 'datasets' folder not found. Run data_generator.py first.")
        return []
    
    datasets = {
        'Order Processing': 'datasets/orders.json',
        'Product Catalog': 'datasets/products.json',
        'Inventory': 'datasets/inventory.json',
        'Activity Log': 'datasets/activity_log.json'
    }
    
    # Check if all dataset files exist
    for name, path in datasets.items():
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Run data_generator.py to generate all datasets.")
            return []
    
    algorithms = [
        (bubble_sort, 'Bubble Sort'),
        (selection_sort, 'Selection Sort'),
        (insertion_sort, 'Insertion Sort'),
        (merge_sort, 'Merge Sort')
    ]
    
    results = []
    
    print("\n" + "="*80)
    print("PERFORMANCE BENCHMARKING")
    print("="*80)
    
    for dataset_name, dataset_path in datasets.items():
        print(f"\nBenchmarking on {dataset_name}...")
        print("-" * 40)
        
        for algo_func, algo_name in algorithms:
            print(f"  Running {algo_name}...", end="", flush=True)
            metrics = benchmark_algorithm(algo_func, dataset_path, algo_name)
            if metrics:
                metrics['dataset'] = dataset_name
                results.append(metrics)
                print(f" done! Time: {metrics['time_seconds']:.4f}s, Memory: {metrics['memory_mb']:.2f}MB")
            else:
                print(" failed!")
    
    # Print results table
    print_results_table(results)
    return results

def print_results_table(results):
    """Print formatted results table"""
    if not results:
        print("\nNo results to display.")
        return
    
    print("\n" + "="*100)
    print("BENCHMARK RESULTS SUMMARY")
    print("="*100)
    print(f"{'Algorithm':<20} {'Dataset':<20} {'Time (s)':<15} {'Memory (MB)':<15} {'Size':<10} {'Valid':<8}")
    print("="*100)
    
    for r in results:
        valid_str = "✓" if r.get('valid', False) else "?"
        print(f"{r['algorithm']:<20} {r['dataset']:<20} {r['time_seconds']:<15.4f} {r['memory_mb']:<15.2f} {r['dataset_size']:<10} {valid_str:<8}")

def test_sorting_correctness():
    """Test all sorting algorithms on small test cases"""
    print("\n" + "="*60)
    print("TESTING SORTING CORRECTNESS")
    print("="*60)
    
    # Small test cases
    test_cases = [
        ([], []),
        ([1], [1]),
        ([5, 2, 8, 1, 9], [1, 2, 5, 8, 9]),
        ([3, 3, 3, 3], [3, 3, 3, 3]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    ]
    
    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (selection_sort, "Selection Sort"),
        (insertion_sort, "Insertion Sort"),
        (merge_sort, "Merge Sort")
    ]
    
    all_passed = True
    
    for algo_func, algo_name in algorithms:
        print(f"\nTesting {algo_name}:")
        passed = 0
        total = len(test_cases)
        
        for i, (input_arr, expected) in enumerate(test_cases):
            result = algo_func(input_arr)
            if result == expected:
                passed += 1
                print(f"  ✓ Test {i+1} passed")
            else:
                all_passed = False
                print(f"  ✗ Test {i+1} failed: {input_arr} -> {result}, expected {expected}")
        
        print(f"  {passed}/{total} tests passed")
    
    if all_passed:
        print("\n✅ All sorting algorithms working correctly!")
    else:
        print("\n❌ Some tests failed. Check implementations.")
    
    return all_passed

# MAIN EXECUTION
if __name__ == "__main__":
    print("SORTING ALGORITHM PERFORMANCE OPTIMIZER")
    print("="*60)
    
    # Test sorting correctness
    test_sorting_correctness()
    
    # Demonstrate stability
    demonstrate_stability()
    
    # Run benchmarks
    benchmark_all_datasets()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)