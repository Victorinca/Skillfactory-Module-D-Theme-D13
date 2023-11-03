#from django.test import TestCase
import logging
import unittest

# Create your tests here.
logger = logging.getLogger('news')
logger = logging.getLogger(__name__)

logger.debug('Это отладочное сообщение')
logger.info('Это информационное сообщение')
logger.warning('Это предупреждение')
logger.error('Это сообщение об ошибке')
logger.critical('Это сообщение о критической ошибке')

def some_view(request):
   logger.debug('Это отладочное сообщение')


class SecurityLoggingTestCase(unittest.TestCase):
   def test_security_logging(self):
       logger = logging.getLogger('django.security')
       logger.info('Test security message')

       # Проверьте, что сообщение было записано в файл security.log
       with open(f"{BASE_DIR}/logs/security.log", 'r') as log_file:
           self.assertIn('Test security message', log_file.read())

