import sqeezz
import asyncio
from typing import List, Any, Callable
from config import setup_builders

# ===== SETUP BUILDERS =====
setup_builders()

# ===== BASIC BUILDER CAPABILITIES =====

print("=== 1. Basic Builder with lazy_add_ref ===")


def basic_example() -> None:
    os = sqeezz.using('os')
    sys = sqeezz.using('sys')
    json = sqeezz.using('json')

    print(f"Current directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print(f"JSON dumps: {json.dumps({'test': 'data'})}")


basic_example()

print("\n=== 2. Builder with add_ref (function/class references) ===")


def function_class_example() -> None:
    logger = sqeezz.using('custom_logger')
    Calculator = sqeezz.using('Calculator')
    db_class = sqeezz.using('DatabaseConnection')

    print(logger("Application started"))
    print(f"5 + 3 = {Calculator.add(5, 3)}")
    print(f"4 * 7 = {Calculator.multiply(4, 7)}")

    # Create instance of class
    db = db_class("localhost:5432")
    print(db.connect())


function_class_example()

print("\n=== 3. Builder with add_named_ref (custom names) ===")


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


def environment_info() -> None:
    os = sqeezz.using('os')
    sys = sqeezz.using('sys')
    db_host = sqeezz.using('db_host')
    debug = sqeezz.using('debug')

    print(f"Current dir: {os.getcwd()}")
    print(f"Python version: {getattr(sys, 'version', 'unknown')}")
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
mobile_server_config: Callable[[],
                               None] = sqeezz.group('mobile_app',
                                                    server_config)

web_route_handler: Callable[[str],
                            None] = sqeezz.group('web_app', route_handler)
mobile_route_handler: Callable[[str],
                               None] = sqeezz.group('mobile_app',
                                                    route_handler)

print("Web app configuration:")
web_server_config()
web_route_handler('/api/users')
web_route_handler('/nonexistent')

print("\nMobile app configuration:")
mobile_server_config()
mobile_route_handler('/mobile/auth')

print("\n=== 6. Async Function Support ===")


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
grouped_async_op: Callable[[], Any] = sqeezz.group('async_env',
                                                   async_operation)
grouped_async_processor: Callable[[List[str]],
                                  Any] = sqeezz.group('async_env',
                                                      async_data_processor)


async def run_async_examples() -> None:
    print("Running async operations...")

    result1 = await grouped_async_op()
    result2 = await grouped_async_processor(['hello', 'world', 'async'])

    print(f"Async operation result: {result1}")
    print(f"Processed data: {result2}")


# Run async examples
asyncio.run(run_async_examples())

print("\n=== 7. Complex Dependency Chains ===")


def user_workflow(user_id: int) -> None:
    # Get dependencies
    UserService = sqeezz.using('UserService')
    EmailService = sqeezz.using('EmailService')
    user_db = sqeezz.using('user_db')
    logger = sqeezz.using('app_logger')
    email_config = sqeezz.using('email_config')

    # Create service instances
    user_service = UserService(user_db, logger)
    email_service = EmailService(email_config)

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
    env_name = sqeezz.using(
        'db_host')  # Using db_host as environment identifier

    print(
        f"Operation '{operation_type}' in environment: {env_name}, debug: {config}"
    )


# Use the same function with different groups
prod_operation: Callable[[str], None] = sqeezz.group('production',
                                                     flexible_operation)
dev_operation: Callable[[str], None] = sqeezz.group('development',
                                                    flexible_operation)
test_operation: Callable[[str], None] = sqeezz.group('testing',
                                                     flexible_operation)

print("Same function, different environments:")
prod_operation("user_creation")
dev_operation("user_creation")
test_operation("user_creation")

print("\n=== 9. Class Example with Using initialization ===")


class ServiceManager:
    """Example class that uses Using for dependency access"""
    
    def __init__(self):
        # Initialize Using objects for dependencies we'll need
        self.logger_using = sqeezz.Using('app_logger')
        self.config_using = sqeezz.Using('config')
        self.db_using = sqeezz.Using('db')
        self.user_service_using = sqeezz.Using('UserService')
    
    def get_logger(self):
        """Get logger using Using.get"""
        return self.logger_using.get
    
    def get_config_value(self, key: str):
        """Get configuration value using Using.get"""
        config = self.config_using.get
        return config.get(key)
    
    def log_system_status(self):
        """Log system status using dependencies through Using.get"""
        logger = self.logger_using.get
        config = self.config_using.get
        
        debug_mode = config.get('debug', False)
        port = config.get('port', 'unknown')
        
        return logger(f"System status: debug={debug_mode}, port={port}")
    
    def create_user_service(self):
        """Create user service instance using Using.get"""
        UserService = self.user_service_using.get
        db = self.db_using.get
        logger = self.logger_using.get
        
        return UserService(db, logger)
    
    def perform_user_operation(self, user_id: int):
        """Perform a complete user operation using multiple dependencies"""
        logger = self.logger_using.get
        logger(f"Starting user operation for user {user_id}")
        
        user_service = self.create_user_service()
        user_data = user_service.get_user(user_id)
        
        logger("User operation completed successfully")
        return user_data


# Create grouped version of the service manager
class_service_manager = sqeezz.group('app', ServiceManager)

print("Creating ServiceManager instance:")
service_manager = class_service_manager()

print("\nTesting ServiceManager methods:")
print("1. Log system status:")
print(f"   {service_manager.log_system_status()}")

print("\n2. Get config value:")
print(f"   Debug mode: {service_manager.get_config_value('debug')}")

print("\n3. Perform user operation:")
user_result = service_manager.perform_user_operation(456)
print(f"   User data: {user_result}")

print("\n4. Direct logger access:")
logger = service_manager.get_logger()
print(f"   {logger('Direct logger call from ServiceManager')}")

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
print("✓ Class with Using initialization and Using.get methods")
