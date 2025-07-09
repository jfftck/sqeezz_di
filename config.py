
import sqeezz
from unittest.mock import Mock
import datetime

# ===== SQEEZZ BUILDER CONFIGURATIONS =====

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


class UserService:

    def __init__(self, db, logger) -> None:
        self.db = db
        self.logger = logger

    def get_user(self, user_id: int) -> dict:
        self.logger(f"Fetching user {user_id}")
        return self.db.find_user(user_id)


class EmailService:

    def __init__(self, config: dict) -> None:
        self.smtp_host = config['smtp_host']
        self.port = config['port']

    def send_email(self, to: str, subject: str) -> str:
        return f"Email sent to {to} via {self.smtp_host}:{self.port}"


def setup_builders():
    """Set up all sqeezz builder configurations"""
    
    # Basic builder with lazy_add_ref
    sqeezz.builder()\
        .lazy_add_ref('os')\
        .lazy_add_ref('sys')\
        .lazy_add_ref('json')

    # Builder with add_ref (function/class references)
    sqeezz.builder()\
        .add_ref(custom_logger)\
        .add_ref(Calculator)\
        .add_ref(DatabaseConnection)

    # Mock objects for testing
    mock_database = Mock()
    mock_database.query.return_value = [{
        "id": 1,
        "name": "John"
    }, {
        "id": 2,
        "name": "Jane"
    }]
    mock_database.insert.return_value = {"success": True, "id": 3}

    mock_api_client = Mock()
    mock_api_client.get.return_value = {"status": "ok", "data": "response"}
    mock_api_client.post.return_value = {"status": "created", "id": 123}

    # Builder with add_named_ref (custom names)
    sqeezz.builder()\
        .add_named_ref('db', mock_database)\
        .add_named_ref('api', mock_api_client)\
        .add_named_ref('config', {'debug': True, 'port': 5000})\
        .add_named_ref('logger_func', custom_logger)

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

    # Web app configuration
    sqeezz.builder('web_app')\
        .add_named_ref('port', 5000)\
        .add_named_ref('host', '0.0.0.0')\
        .add_named_ref('routes', ['/api/users', '/api/posts', '/health'])

    # Mobile app configuration
    sqeezz.builder('mobile_app')\
        .add_named_ref('port', 3000)\
        .add_named_ref('host', 'localhost')\
        .add_named_ref('routes', ['/mobile/auth', '/mobile/data'])

    # Async environment setup
    sqeezz.builder('async_env')\
        .add_named_ref('delay', 0.1)\
        .add_named_ref('message_prefix', '[ASYNC]')

    # Complex dependency setup
    mock_user_db = Mock()
    mock_user_db.find_user.return_value = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }

    email_config = {'smtp_host': 'smtp.example.com', 'port': 587}

    sqeezz.builder('app')\
        .add_named_ref('user_db', mock_user_db)\
        .add_named_ref('app_logger', custom_logger)\
        .add_named_ref('logger_func', custom_logger)\
        .add_named_ref('email_config', email_config)\
        .add_named_ref('config', {'debug': True, 'port': 5000})\
        .add_named_ref('db', mock_user_db)\
        .add_ref(UserService)\
        .add_ref(EmailService)
