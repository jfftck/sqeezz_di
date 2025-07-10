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
        self.logger_using = sqeezz.Using('logger_func')
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


# Create ServiceManager instance
service_manager = ServiceManager()

# Create grouped versions of the methods
app_log_system_status = sqeezz.group('app', service_manager.log_system_status)
app_get_config_value = sqeezz.group('app', service_manager.get_config_value)
app_perform_user_operation = sqeezz.group('app', service_manager.perform_user_operation)
app_get_logger = sqeezz.group('app', service_manager.get_logger)

print("Testing ServiceManager methods with app group:")
print("1. Log system status:")
print(f"   {app_log_system_status()}")

print("\n2. Get config value:")
print(f"   Debug mode: {app_get_config_value('debug')}")

print("\n3. Perform user operation:")
user_result = app_perform_user_operation(456)
print(f"   User data: {user_result}")

print("\n4. Direct logger access:")
logger = app_get_logger()
print(f"   {logger('Direct logger call from ServiceManager')}")

print("\n=== 10. ServiceManager with Different Groups ===")

# Create enterprise versions of the methods
enterprise_log_system_status = sqeezz.group('enterprise', service_manager.log_system_status)
enterprise_get_config_value = sqeezz.group('enterprise', service_manager.get_config_value)
enterprise_perform_user_operation = sqeezz.group('enterprise', service_manager.perform_user_operation)

print("Testing ServiceManager methods with enterprise group:")
print("1. Log system status:")
print(f"   {enterprise_log_system_status()}")

print("\n2. Get config values:")
print(f"   Debug mode: {enterprise_get_config_value('debug')}")
print(f"   Port: {enterprise_get_config_value('port')}")
print(f"   Max connections: {enterprise_get_config_value('max_connections')}")

print("\n3. Perform user operation:")
enterprise_user_result = enterprise_perform_user_operation(789)
print(f"   Enterprise user data: {enterprise_user_result}")

print("\n4. Compare configurations:")
print("App group config:")
print(f"   Port: {app_get_config_value('port')}")
print(f"   Debug: {app_get_config_value('debug')}")

print("Enterprise group config:")
print(f"   Port: {enterprise_get_config_value('port')}")
print(f"   Debug: {enterprise_get_config_value('debug')}")
print(f"   Max connections: {enterprise_get_config_value('max_connections')}")

print("\n=== 11. Group Switcher Decorator - Function Example ===")

@sqeezz.group_switcher
def api_handler(endpoint: str) -> dict:
    """Function that handles API requests with different configurations"""
    api_version = sqeezz.using('api_version')
    rate_limit = sqeezz.using('rate_limit')
    timeout = sqeezz.using('timeout')
    
    return {
        'endpoint': endpoint,
        'version': api_version,
        'rate_limit': rate_limit,
        'timeout': timeout,
        'response': f"Handled {endpoint} with {api_version} (limit: {rate_limit}, timeout: {timeout}s)"
    }

# Use the switcher with different groups
print("API Handler with different configurations:")
print("V1 API:", api_handler['api_v1']('/users'))
print("V2 API:", api_handler['api_v2']('/users'))
print("Beta API:", api_handler['api_beta']('/users'))

# Another function example with database configurations
@sqeezz.group_switcher
def database_connector(table_name: str) -> dict:
    """Function that connects to different database types"""
    db_type = sqeezz.using('db_type')
    connection_pool = sqeezz.using('connection_pool')
    query_timeout = sqeezz.using('query_timeout')
    host = sqeezz.using('host')
    
    return {
        'table': table_name,
        'database': db_type,
        'pool_size': connection_pool,
        'timeout': query_timeout,
        'host': host,
        'connection_string': f"Connected to {db_type} at {host} (pool: {connection_pool}, timeout: {query_timeout}s)"
    }

print("\nDatabase Connector with different configurations:")
print("MySQL:", database_connector['mysql_db']('users'))
print("PostgreSQL:", database_connector['postgres_db']('users'))
print("SQLite:", database_connector['sqlite_db']('users'))

print("\n=== 12. Group Switcher Decorator - Class Method Example ===")

class DatabaseManager:
    """Class that manages database operations with different configurations"""
    
    def __init__(self):
        self.connection_count = 0
    
    @sqeezz.group_switcher
    def execute_query(self, query: str) -> dict:
        """Execute a query with different database configurations"""
        db_type = sqeezz.using('db_type')
        connection_pool = sqeezz.using('connection_pool')
        query_timeout = sqeezz.using('query_timeout')
        host = sqeezz.using('host')
        
        self.connection_count += 1
        
        return {
            'query': query,
            'database_type': db_type,
            'executed_on': host,
            'pool_size': connection_pool,
            'timeout': query_timeout,
            'connection_id': self.connection_count,
            'result': f"Query '{query}' executed on {db_type} at {host}"
        }
    
    @sqeezz.group_switcher
    def get_connection_info(self) -> dict:
        """Get connection information for different database types"""
        db_type = sqeezz.using('db_type')
        connection_pool = sqeezz.using('connection_pool')
        query_timeout = sqeezz.using('query_timeout')
        host = sqeezz.using('host')
        
        return {
            'database_type': db_type,
            'host': host,
            'max_connections': connection_pool,
            'query_timeout': query_timeout,
            'total_connections_made': self.connection_count,
            'status': f"{db_type} database at {host} is ready"
        }

# Create an instance of DatabaseManager
db_manager = DatabaseManager()

print("DatabaseManager with different database configurations:")
print("\n1. Execute queries with different databases:")
mysql_result = db_manager.execute_query['mysql_db']('SELECT * FROM users')
print(f"MySQL result: {mysql_result['result']}")

postgres_result = db_manager.execute_query['postgres_db']('SELECT * FROM orders')
print(f"PostgreSQL result: {postgres_result['result']}")

sqlite_result = db_manager.execute_query['sqlite_db']('SELECT * FROM products')
print(f"SQLite result: {sqlite_result['result']}")

print("\n2. Get connection info for different databases:")
mysql_info = db_manager.get_connection_info['mysql_db']()
print(f"MySQL info: {mysql_info['status']}")

postgres_info = db_manager.get_connection_info['postgres_db']()
print(f"PostgreSQL info: {postgres_info['status']}")

sqlite_info = db_manager.get_connection_info['sqlite_db']()
print(f"SQLite info: {sqlite_info['status']}")

print("\n3. Detailed configuration comparison:")
print("MySQL config:", {
    'type': mysql_info['database_type'],
    'host': mysql_info['host'],
    'pool': mysql_info['max_connections'],
    'timeout': mysql_info['query_timeout']
})

print("PostgreSQL config:", {
    'type': postgres_info['database_type'],
    'host': postgres_info['host'],
    'pool': postgres_info['max_connections'],
    'timeout': postgres_info['query_timeout']
})

print("SQLite config:", {
    'type': sqlite_info['database_type'],
    'host': sqlite_info['host'],
    'pool': sqlite_info['max_connections'],
    'timeout': sqlite_info['query_timeout']
})</old_str>

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
print("✓ Classes working with multiple groups and different configurations")