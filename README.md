
# Sqeezz

A lightweight dependency injection and service configuration library for Python that makes it easy to manage dependencies, configure services, and switch between different environments.

## Features

- 🚀 **Simple API** - Easy to use builder pattern for configuring dependencies
- 🔧 **Flexible Configuration** - Support for functions, classes, modules, and custom objects
- 🏷️ **Named Groups** - Organize dependencies into logical groups and switch between them
- ⚡ **Async Support** - Full support for async functions and coroutines
- 🧪 **Testing Friendly** - Perfect for mocking dependencies in tests
- 🌍 **Environment Management** - Easy switching between development, testing, and production configurations

## Installation

```bash
pip install sqeezz
```

## Quick Start

```python
import sqeezz

# Configure dependencies
sqeezz.builder()\
    .add_ref(my_service)\
    .add_named_ref('config', {'debug': True})\
    .lazy_add_ref('os')

# Use dependencies
def my_function():
    service = sqeezz.using('my_service')
    config = sqeezz.using('config')
    os = sqeezz.using('os')
    
    print(f"Debug mode: {config['debug']}")
    print(f"Current directory: {os.getcwd()}")
```

## Core Concepts

### Builder Pattern

Sqeezz uses a fluent builder pattern to configure dependencies:

```python
import sqeezz

# Basic builder
sqeezz.builder()\
    .add_ref(Calculator)\
    .add_named_ref('db_url', 'postgresql://localhost:5432/mydb')\
    .lazy_add_ref('json')
```

### Three Ways to Add Dependencies

#### 1. `add_ref()` - Add by Reference
Adds functions, classes, or objects using their `__name__` attribute:

```python
def logger(message):
    print(f"LOG: {message}")

class UserService:
    def get_user(self, id):
        return {"id": id, "name": "John"}

sqeezz.builder()\
    .add_ref(logger)\
    .add_ref(UserService)

# Usage
log_func = sqeezz.using('logger')
UserService = sqeezz.using('UserService')
user_service = UserService()
```

#### 2. `add_named_ref()` - Add with Custom Name
Adds any object with a custom name:

```python
sqeezz.builder()\
    .add_named_ref('db_config', {'host': 'localhost', 'port': 5432})\
    .add_named_ref('api_key', 'your-secret-key')\
    .add_named_ref('multiplier', lambda x: x * 2)

# Usage
config = sqeezz.using('db_config')
api_key = sqeezz.using('api_key')
multiply = sqeezz.using('multiplier')
```

#### 3. `lazy_add_ref()` - Lazy Module Loading
Loads modules only when needed:

```python
sqeezz.builder()\
    .lazy_add_ref('os')\
    .lazy_add_ref('json')\
    .lazy_add_ref('datetime')

# Usage
os = sqeezz.using('os')
json = sqeezz.using('json')
```

### Named Groups

Organize dependencies into logical groups for different environments:

```python
# Production configuration
sqeezz.builder('production')\
    .add_named_ref('db_host', 'prod-db.example.com')\
    .add_named_ref('debug', False)\
    .add_named_ref('cache_ttl', 3600)

# Development configuration
sqeezz.builder('development')\
    .add_named_ref('db_host', 'localhost')\
    .add_named_ref('debug', True)\
    .add_named_ref('cache_ttl', 60)

# Function that uses configuration
def get_database_info():
    host = sqeezz.using('db_host')
    debug = sqeezz.using('debug')
    return f"Connecting to {host} (debug: {debug})"

# Create environment-specific versions
prod_db_info = sqeezz.group('production', get_database_info)
dev_db_info = sqeezz.group('development', get_database_info)

print(prod_db_info())  # "Connecting to prod-db.example.com (debug: False)"
print(dev_db_info())   # "Connecting to localhost (debug: True)"
```

### Async Support

Sqeezz fully supports async functions:

```python
import asyncio
import sqeezz

# Configure async dependencies
sqeezz.builder('async_env')\
    .add_named_ref('delay', 0.1)\
    .add_named_ref('api_url', 'https://api.example.com')

async def fetch_data():
    delay = sqeezz.using('delay')
    api_url = sqeezz.using('api_url')
    
    print(f"Fetching from {api_url}")
    await asyncio.sleep(delay)
    return {"data": "response"}

# Create grouped async function
async_fetch = sqeezz.group('async_env', fetch_data)

# Usage
result = asyncio.run(async_fetch())
```

## Advanced Examples

### Complex Dependency Chains

```python
import sqeezz
from unittest.mock import Mock

# Setup complex dependencies
mock_database = Mock()
mock_database.find_user.return_value = {
    "id": 1, "name": "Alice", "email": "alice@example.com"
}

def custom_logger(message):
    return f"[{datetime.now()}] {message}"

class UserService:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
    
    def get_user(self, user_id):
        self.logger(f"Fetching user {user_id}")
        return self.db.find_user(user_id)

class EmailService:
    def __init__(self, config):
        self.smtp_host = config['smtp_host']
        self.port = config['port']
    
    def send_email(self, to, subject):
        return f"Email sent to {to} via {self.smtp_host}:{self.port}"

# Configure all dependencies
sqeezz.builder('app')\
    .add_named_ref('user_db', mock_database)\
    .add_named_ref('app_logger', custom_logger)\
    .add_named_ref('email_config', {'smtp_host': 'smtp.example.com', 'port': 587})\
    .add_ref(UserService)\
    .add_ref(EmailService)

# Use in application
def user_workflow(user_id):
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
    
    return {"user": user, "email": email_result}

# Create grouped workflow
app_workflow = sqeezz.group('app', user_workflow)
result = app_workflow(123)
```

### Testing with Mocks

```python
import sqeezz
from unittest.mock import Mock

# Test configuration with mocks
mock_api = Mock()
mock_api.get.return_value = {"status": "ok", "data": "test"}

sqeezz.builder('test')\
    .add_named_ref('api_client', mock_api)\
    .add_named_ref('base_url', 'https://test-api.example.com')\
    .add_named_ref('timeout', 0.001)

def api_service():
    api = sqeezz.using('api_client')
    base_url = sqeezz.using('base_url')
    
    response = api.get(f"{base_url}/users")
    return response

# Test with mocked dependencies
test_service = sqeezz.group('test', api_service)
result = test_service()
assert result["status"] == "ok"
```

## API Reference

### `sqeezz.builder(name: str = 'default') -> Builder`

Creates a new builder for the specified group.

### `Builder.add_ref(ref: Callable | type) -> Builder`

Adds a function or class using its `__name__` attribute as the key.

### `Builder.add_named_ref(name: str, ref: Any) -> Builder`

Adds any object with a custom name.

### `Builder.lazy_add_ref(module_name: str) -> Builder`

Adds a module that will be imported only when first accessed.

### `sqeezz.using(name: str) -> Any`

Retrieves a dependency from the current group.

### `sqeezz.group(group_name: str, func: Callable) -> Callable`

Wraps a function to use dependencies from a specific group.

## Requirements

- Python 3.8+
- No external dependencies

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### 0.1.0
- Initial release
- Basic dependency injection functionality
- Named groups support
- Async function support
- Comprehensive test suite
