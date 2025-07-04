
import sqeezz
from unittest.mock import Mock

# Set up the default group with lazy loading of os
sqeezz.builder()\
.lazy_add_ref('os')

# Create a mock os module for testing
mock_os = Mock()
mock_os.getcwd.return_value = "/fake/current/directory"
mock_os.listdir.return_value = ["file1.txt", "file2.txt", "fake_folder"]
mock_os.path.exists.return_value = True
mock_os.path.join = lambda *args: "/".join(args)

def example(test_str: str):
    print(sqeezz.using('os'), test_str, sep=' |>> ')

def file_operations():
    os_ref = sqeezz.using('os')
    print(f"Current directory: {os_ref.getcwd()}")
    if hasattr(os_ref, 'listdir'):
        print(f"Directory contents: {os_ref.listdir('.')}")

def path_operations():
    os_ref = sqeezz.using('os')
    if hasattr(os_ref, 'path'):
        joined_path = os_ref.path.join("home", "user", "documents")
        print(f"Joined path: {joined_path}")
        print(f"Path exists: {os_ref.path.exists(joined_path)}")

# Example 1: Basic usage with real os module
print("=== Example 1: Real OS Module ===")
example('hello')
file_operations()
path_operations()

# Example 2: Using mocked os module in a test group
print("\n=== Example 2: Mocked OS Module ===")
sqeezz.builder('test os')\
.add_named_ref('os', mock_os)

test_example = sqeezz.group('test os', example)
test_file_ops = sqeezz.group('test os', file_operations)
test_path_ops = sqeezz.group('test os', path_operations)

test_example('testing group')
test_file_ops()
test_path_ops()

# Example 3: Multiple groups with different configurations
print("\n=== Example 3: Multiple Groups ===")
sqeezz.builder('production')\
.lazy_add_ref('os')\
.lazy_add_ref('sys')

sqeezz.builder('testing')\
.add_named_ref('os', mock_os)\
.add_named_ref('sys', Mock(platform="fake-platform", version="3.11.0"))

def system_info():
    os_ref = sqeezz.using('os')
    sys_ref = sqeezz.using('sys')
    print(f"OS module: {type(os_ref).__name__}")
    print(f"System platform: {getattr(sys_ref, 'platform', 'unknown')}")

prod_system_info = sqeezz.group('production', system_info)
test_system_info = sqeezz.group('testing', system_info)

print("Production environment:")
prod_system_info()

print("Testing environment:")
test_system_info()

# Example 4: Back to default group
print("\n=== Example 4: Back to Default ===")
example('goodbye')
file_operations()
