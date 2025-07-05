
import sqeezz
from unittest.mock import Mock
import asyncio
import datetime
from typing import Dict, List, Any, Callable, Optional

# ===== BASIC BUILDER CAPABILITIES =====

print("=== 1. Basic Builder with lazy_add_ref ===")
# Lazy loading of standard modules
sqeezz.builder()\
    .lazy_add_ref('os')\
    .lazy_add_ref('sys')\
    .lazy_add_ref('json')

def basic_example() -> None:
    os_ref = sqeezz.using('os')
    sys_ref = sqeezz.using('sys')
    json_ref = sqeezz.using('json')
    
    print(f"Current directory: {os_ref.getcwd()}")
    print(f"Python version: {sys_ref.version}")
    print(f"JSON dumps: {json_ref.dumps({'test': 'data'})}")

basic_example()

print("\n=== 2. Builder with add_ref (function/class references) ===")

# Custom functions and classes to add as references
def custom_logger(message: str) -> str:
    return f"[{datetime.datetime.now()}] {message}"

class Calculator:
    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
    
    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b

class DatabaseConnection:
    def __init__(self, host: str) -> None:
        self.host = host
    
    def connect(self) -> str:
        return f"Connected to {self.host}"

# Add function and class references
sqeezz.builder()\
    .add_ref(custom_logger)\
    .add_ref(Calculator)\
    .add_ref(DatabaseConnection)

def function_class_example() -> None:
    logger = sqeezz.using('custom_logger')
    calc = sqeezz.using('Calculator')
    db_class = sqeezz.using('DatabaseConnection')
    
    print(logger("Application started"))
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"4 * 7 = {calc.multiply(4, 7)}")
    
    # Create instance of class
    db = db_class("localhost:5432")
    print(db.connect())

function_class_example()

print("\n=== 3. Builder with add_named_ref (custom names) ===")

# Mock objects for testing
mock_database = Mock()
mock_database.query.return_value = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
mock_database.insert.return_value = {"success": True, "id": 3}

mock_api_client = Mock()
mock_api_client.get.return_value = {"status": "ok", "data": "response"}
mock_api_client.post.return_value = {"status": "created", "id": 123}

# Add with custom names
sqeezz.builder()\
    .add_named_ref('db', mock_database)\
    .add_named_ref('api', mock_api_client)\
    .add_named_ref('config', {'debug': True, 'port': 5000})\
    .add_named_ref('logger_func', custom_logger)

def named_ref_example() -> None:
    db = sqeezz.using('db')
    api = sqeezz.using('api')
    config = sqeezz.using('config')
    logger = sqeezz.using('logger_func')
    
    print(logger("Using named references"))
    print(f"Database query result: {db.query('SELECT * FROM users')}")
    print(f"API response: {api.get('/status')}")
    print(f"Config debug mode: {config['debug']}")

named_ref_example()

print("\n=== 4. Multiple Named Groups ===")

# Production group with real modules
sqeezz.builder('production')\
    .lazy_add_ref('os')\
    .lazy_add_ref('sys')\
    .add_named_ref('db_host', 'prod-db.example.com')\
    .add_named_ref('debug', False)

# Development group with different settings
sqeezz.builder('development')\
    .lazy_add_ref('os')\
    .lazy_add_ref('sys')\
    .add_named_ref('db_host', 'localhost')\
    .add_named_ref('debug', True)

# Testing group with mocks
mock_os = Mock()
mock_os.getcwd.return_value = "/fake/test/directory"
mock_os.listdir.return_value = ["test_file.txt"]

sqeezz.builder('testing')\
    .add_named_ref('os', mock_os)\
    .add_named_ref('sys', Mock(version="3.11.0-test"))\
    .add_named_ref('db_host', 'test-db')\
    .add_named_ref('debug', True)

def environment_info() -> None:
    os_ref = sqeezz.using('os')
    sys_ref = sqeezz.using('sys')
    db_host = sqeezz.using('db_host')
    debug = sqeezz.using('debug')
    
    print(f"Current dir: {os_ref.getcwd()}")
    print(f"Python version: {getattr(sys_ref, 'version', 'unknown')}")
    print(f"Database host: {db_host}")
    print(f"Debug mode: {debug}")

# Create grouped functions
prod_info: Callable[[], None] = sqeezz.group('production', environment_info)
dev_info: Callable[[], None] = sqeezz.group('development', environment_info)
test_info: Callable[[], None] = sqeezz.group('testing', environment_info)

print("Production environment:")
prod_info()

print("\nDevelopment environment:")
dev_info()

print("\nTesting environment:")
test_info()

print("\n=== 5. Advanced Group Usage with Different Functions ===")

# Create a more complex scenario
sqeezz.builder('web_app')\
    .add_named_ref('port', 5000)\
    .add_named_ref('host', '0.0.0.0')\
    .add_named_ref('routes', ['/api/users', '/api/posts', '/health'])

sqeezz.builder('mobile_app')\
    .add_named_ref('port', 3000)\
    .add_named_ref('host', 'localhost')\
    .add_named_ref('routes', ['/mobile/auth', '/mobile/data'])

def server_config() -> None:
    port = sqeezz.using('port')
    host = sqeezz.using('host')
    routes = sqeezz.using('routes')
    
    print(f"Server running on {host}:{port}")
    print(f"Available routes: {', '.join(routes)}")

def route_handler(route_name: str) -> None:
    routes = sqeezz.using('routes')
    port = sqeezz.using('port')
    
    if route_name in routes:
        print(f"Handling {route_name} on port {port}")
    else:
        print(f"Route {route_name} not found")

web_server_config: Callable[[], None] = sqeezz.group('web_app', server_config)
mobile_server_config: Callable[[], None] = sqeezz.group('mobile_app', server_config)

web_route_handler: Callable[[str], None] = sqeezz.group('web_app', route_handler)
mobile_route_handler: Callable[[str], None] = sqeezz.group('mobile_app', route_handler)

print("Web app configuration:")
web_server_config()
web_route_handler('/api/users')
web_route_handler('/nonexistent')

print("\nMobile app configuration:")
mobile_server_config()
mobile_route_handler('/mobile/auth')

print("\n=== 6. Async Function Support ===")

# Set up async environment
sqeezz.builder('async_env')\
    .add_named_ref('delay', 0.1)\
    .add_named_ref('message_prefix', '[ASYNC]')

async def async_operation() -> str:
    delay = sqeezz.using('delay')
    prefix = sqeezz.using('message_prefix')
    
    print(f"{prefix} Starting async operation...")
    await asyncio.sleep(delay)
    print(f"{prefix} Async operation completed!")
    return "async_result"

async def async_data_processor(data: List[str]) -> List[str]:
    prefix = sqeezz.using('message_prefix')
    delay = sqeezz.using('delay')
    
    print(f"{prefix} Processing {len(data)} items...")
    await asyncio.sleep(delay)
    processed = [item.upper() for item in data]
    print(f"{prefix} Processing complete!")
    return processed

# Create grouped async functions
grouped_async_op: Callable[[], Any] = sqeezz.group('async_env', async_operation)
grouped_async_processor: Callable[[List[str]], Any] = sqeezz.group('async_env', async_data_processor)

async def run_async_examples() -> None:
    print("Running async operations...")
    
    result1 = await grouped_async_op()
    result2 = await grouped_async_processor(['hello', 'world', 'async'])
    
    print(f"Async operation result: {result1}")
    print(f"Processed data: {result2}")

# Run async examples
asyncio.run(run_async_examples())

print("\n=== 7. Complex Dependency Chains ===")

# Simulate a complex application with multiple dependencies
class UserService:
    def __init__(self, db: Any, logger: Callable[[str], str]) -> None:
        self.db = db
        self.logger = logger
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        self.logger(f"Fetching user {user_id}")
        return self.db.find_user(user_id)

class EmailService:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.smtp_host = config['smtp_host']
        self.port = config['port']
    
    def send_email(self, to: str, subject: str) -> str:
        return f"Email sent to {to} via {self.smtp_host}:{self.port}"

# Mock dependencies
mock_user_db = Mock()
mock_user_db.find_user.return_value = {"id": 1, "name": "Alice", "email": "alice@example.com"}

email_config: Dict[str, Any] = {
    'smtp_host': 'smtp.example.com',
    'port': 587
}

# Set up complex dependency chain
sqeezz.builder('app')\
    .add_named_ref('user_db', mock_user_db)\
    .add_named_ref('app_logger', custom_logger)\
    .add_named_ref('email_config', email_config)\
    .add_ref(UserService)\
    .add_ref(EmailService)

def user_workflow(user_id: int) -> None:
    # Get dependencies
    user_service_class = sqeezz.using('UserService')
    email_service_class = sqeezz.using('EmailService')
    user_db = sqeezz.using('user_db')
    logger = sqeezz.using('app_logger')
    email_config = sqeezz.using('email_config')
    
    # Create service instances
    user_service = user_service_class(user_db, logger)
    email_service = email_service_class(email_config)
    
    # Execute workflow
    user = user_service.get_user(user_id)
    email_result = email_service.send_email(user['email'], "Welcome!")
    
    print(f"User: {user}")
    print(f"Email result: {email_result}")

app_workflow: Callable[[int], None] = sqeezz.group('app', user_workflow)

print("Complex dependency chain example:")
app_workflow(123)

print("\n=== 8. Switching Between Groups Dynamically ===")

# Demonstrate switching contexts
def flexible_operation(operation_type: str) -> None:
    config = sqeezz.using('debug')
    env_name = sqeezz.using('db_host')  # Using db_host as environment identifier
    
    print(f"Operation '{operation_type}' in environment: {env_name}, debug: {config}")

# Use the same function with different groups
prod_operation: Callable[[str], None] = sqeezz.group('production', flexible_operation)
dev_operation: Callable[[str], None] = sqeezz.group('development', flexible_operation)
test_operation: Callable[[str], None] = sqeezz.group('testing', flexible_operation)

print("Same function, different environments:")
prod_operation("user_creation")
dev_operation("user_creation") 
test_operation("user_creation")

print("\n=== Summary ===")
print("Demonstrated sqeezz capabilities:")
print("✓ lazy_add_ref - Load modules dynamically")
print("✓ add_ref - Add functions/classes by name")
print("✓ add_named_ref - Add with custom names")
print("✓ Multiple named groups")
print("✓ Group function wrapping")
print("✓ Async function support")
print("✓ Complex dependency injection")
print("✓ Dynamic group switching")
