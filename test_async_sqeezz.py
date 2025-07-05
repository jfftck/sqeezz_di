
import unittest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sqeezz


class TestAsyncSqueezz(unittest.TestCase):
    
    def setUp(self):
        """Reset sqeezz state before each test"""
        sqeezz._refs.clear()
        sqeezz._group_name = 'default'
    
    def test_async_operation_with_mocked_dependencies(self):
        """Test basic async operation with mocked delay and message prefix"""
        # Setup mocked dependencies
        mock_delay = 0.001  # Very short delay for testing
        mock_prefix = '[TEST_ASYNC]'
        
        sqeezz.builder('test_async')\
            .add_named_ref('delay', mock_delay)\
            .add_named_ref('message_prefix', mock_prefix)
        
        async def test_async_operation():
            delay = sqeezz.using('delay')
            prefix = sqeezz.using('message_prefix')
            
            await asyncio.sleep(delay)
            return f"{prefix} Operation completed"
        
        grouped_async_op = sqeezz.group('test_async', test_async_operation)
        
        # Run the test
        async def run_test():
            result = await grouped_async_op()
            self.assertEqual(result, '[TEST_ASYNC] Operation completed')
        
        asyncio.run(run_test())
    
    def test_async_data_processor_with_mocked_dependencies(self):
        """Test async data processor with mocked dependencies"""
        # Setup mocked dependencies
        mock_delay = 0.001
        mock_prefix = '[PROCESSOR]'
        mock_transform = lambda x: x.upper() + '_PROCESSED'
        
        sqeezz.builder('processor_env')\
            .add_named_ref('delay', mock_delay)\
            .add_named_ref('message_prefix', mock_prefix)\
            .add_named_ref('transform_func', mock_transform)
        
        async def async_data_processor(data):
            delay = sqeezz.using('delay')
            prefix = sqeezz.using('message_prefix')
            transform = sqeezz.using('transform_func')
            
            await asyncio.sleep(delay)
            processed = [transform(item) for item in data]
            return processed
        
        grouped_processor = sqeezz.group('processor_env', async_data_processor)
        
        # Run the test
        async def run_test():
            input_data = ['hello', 'world']
            result = await grouped_processor(input_data)
            expected = ['HELLO_PROCESSED', 'WORLD_PROCESSED']
            self.assertEqual(result, expected)
        
        asyncio.run(run_test())
    
    def test_async_database_operations_with_mocks(self):
        """Test async database operations with comprehensive mocks"""
        # Setup mocked database and logger
        mock_db = AsyncMock()
        mock_db.find_user.return_value = {
            'id': 123, 
            'name': 'Test User', 
            'email': 'test@example.com'
        }
        mock_db.update_user.return_value = {'success': True, 'updated_at': '2024-01-01'}
        
        mock_logger = Mock()
        mock_logger.log = Mock(return_value="Logged successfully")
        
        sqeezz.builder('db_test')\
            .add_named_ref('database', mock_db)\
            .add_named_ref('logger', mock_logger)\
            .add_named_ref('timeout', 0.001)
        
        async def async_user_service(user_id, update_data=None):
            db = sqeezz.using('database')
            logger = sqeezz.using('logger')
            timeout = sqeezz.using('timeout')
            
            await asyncio.sleep(timeout)
            
            user = await db.find_user(user_id)
            logger.log(f"Found user: {user['name']}")
            
            if update_data:
                update_result = await db.update_user(user_id, update_data)
                return {'user': user, 'update': update_result}
            
            return {'user': user}
        
        grouped_service = sqeezz.group('db_test', async_user_service)
        
        # Test without update
        async def test_find_only():
            result = await grouped_service(123)
            self.assertEqual(result['user']['name'], 'Test User')
            mock_db.find_user.assert_called_with(123)
            mock_logger.log.assert_called_with("Found user: Test User")
        
        # Test with update
        async def test_find_and_update():
            update_data = {'name': 'Updated User'}
            result = await grouped_service(123, update_data)
            self.assertEqual(result['user']['name'], 'Test User')
            self.assertTrue(result['update']['success'])
            mock_db.update_user.assert_called_with(123, update_data)
        
        asyncio.run(test_find_only())
        asyncio.run(test_find_and_update())
    
    def test_async_api_client_with_mocked_responses(self):
        """Test async API client with mocked HTTP responses"""
        # Setup mocked API client
        mock_api = AsyncMock()
        mock_api.get.return_value = {'status': 200, 'data': {'message': 'success'}}
        mock_api.post.return_value = {'status': 201, 'id': 456}
        
        mock_config = {
            'base_url': 'https://test-api.example.com',
            'timeout': 0.001,
            'retry_count': 3
        }
        
        sqeezz.builder('api_test')\
            .add_named_ref('api_client', mock_api)\
            .add_named_ref('config', mock_config)
        
        async def async_api_service(endpoint, method='GET', data=None):
            api = sqeezz.using('api_client')
            config = sqeezz.using('config')
            
            await asyncio.sleep(config['timeout'])
            
            if method == 'GET':
                response = await api.get(f"{config['base_url']}/{endpoint}")
            elif method == 'POST':
                response = await api.post(f"{config['base_url']}/{endpoint}", data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response
        
        grouped_api = sqeezz.group('api_test', async_api_service)
        
        # Test GET request
        async def test_get_request():
            result = await grouped_api('users/123')
            self.assertEqual(result['status'], 200)
            self.assertEqual(result['data']['message'], 'success')
            mock_api.get.assert_called_with('https://test-api.example.com/users/123')
        
        # Test POST request
        async def test_post_request():
            post_data = {'name': 'New User'}
            result = await grouped_api('users', 'POST', post_data)
            self.assertEqual(result['status'], 201)
            self.assertEqual(result['id'], 456)
            mock_api.post.assert_called_with('https://test-api.example.com/users', post_data)
        
        asyncio.run(test_get_request())
        asyncio.run(test_post_request())
    
    def test_multiple_async_groups_with_different_configs(self):
        """Test multiple async groups with different configurations"""
        # Setup production environment
        prod_config = {
            'database_url': 'prod://db.example.com',
            'cache_ttl': 3600,
            'retry_attempts': 5
        }
        
        # Setup development environment
        dev_config = {
            'database_url': 'dev://localhost:5432',
            'cache_ttl': 60,
            'retry_attempts': 2
        }
        
        sqeezz.builder('production')\
            .add_named_ref('config', prod_config)\
            .add_named_ref('delay', 0.001)
        
        sqeezz.builder('development')\
            .add_named_ref('config', dev_config)\
            .add_named_ref('delay', 0.001)
        
        async def async_environment_service():
            config = sqeezz.using('config')
            delay = sqeezz.using('delay')
            
            await asyncio.sleep(delay)
            
            return {
                'database_url': config['database_url'],
                'cache_ttl': config['cache_ttl'],
                'retry_attempts': config['retry_attempts']
            }
        
        prod_service = sqeezz.group('production', async_environment_service)
        dev_service = sqeezz.group('development', async_environment_service)
        
        async def test_both_environments():
            prod_result = await prod_service()
            dev_result = await dev_service()
            
            # Verify production config
            self.assertEqual(prod_result['database_url'], 'prod://db.example.com')
            self.assertEqual(prod_result['cache_ttl'], 3600)
            self.assertEqual(prod_result['retry_attempts'], 5)
            
            # Verify development config
            self.assertEqual(dev_result['database_url'], 'dev://localhost:5432')
            self.assertEqual(dev_result['cache_ttl'], 60)
            self.assertEqual(dev_result['retry_attempts'], 2)
        
        asyncio.run(test_both_environments())
    
    def test_async_error_handling_with_mocks(self):
        """Test async error handling with mocked failures"""
        # Setup mocked service that can fail
        mock_service = AsyncMock()
        mock_service.risky_operation.side_effect = Exception("Simulated failure")
        
        mock_fallback = AsyncMock()
        mock_fallback.safe_operation.return_value = "Fallback result"
        
        sqeezz.builder('error_test')\
            .add_named_ref('risky_service', mock_service)\
            .add_named_ref('fallback_service', mock_fallback)\
            .add_named_ref('max_retries', 2)
        
        async def async_resilient_operation():
            risky = sqeezz.using('risky_service')
            fallback = sqeezz.using('fallback_service')
            max_retries = sqeezz.using('max_retries')
            
            for attempt in range(max_retries):
                try:
                    result = await risky.risky_operation()
                    return result
                except Exception:
                    if attempt == max_retries - 1:
                        # Last attempt failed, use fallback
                        return await fallback.safe_operation()
                    continue
        
        grouped_operation = sqeezz.group('error_test', async_resilient_operation)
        
        async def test_error_handling():
            result = await grouped_operation()
            self.assertEqual(result, "Fallback result")
            
            # Verify risky operation was called the expected number of times
            self.assertEqual(mock_service.risky_operation.call_count, 2)
            
            # Verify fallback was called once
            mock_fallback.safe_operation.assert_called_once()
        
        asyncio.run(test_error_handling())
    
    def test_async_group_context_switching(self):
        """Test that async groups properly switch context"""
        # Setup different groups with different values
        sqeezz.builder('group_a')\
            .add_named_ref('value', 'A')\
            .add_named_ref('multiplier', 2)
        
        sqeezz.builder('group_b')\
            .add_named_ref('value', 'B')\
            .add_named_ref('multiplier', 3)
        
        async def async_value_processor():
            value = sqeezz.using('value')
            multiplier = sqeezz.using('multiplier')
            
            await asyncio.sleep(0.001)
            
            return f"{value}" * multiplier
        
        processor_a = sqeezz.group('group_a', async_value_processor)
        processor_b = sqeezz.group('group_b', async_value_processor)
        
        async def test_context_switching():
            # Run both processors concurrently
            result_a, result_b = await asyncio.gather(
                processor_a(),
                processor_b()
            )
            
            self.assertEqual(result_a, 'AA')  # 'A' * 2
            self.assertEqual(result_b, 'BBB')  # 'B' * 3
        
        asyncio.run(test_context_switching())


if __name__ == '__main__':
    unittest.main()
