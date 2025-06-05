import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
IS_TEST = ENVIRONMENT == 'test'

print(f"Environment: {ENVIRONMENT}")
print(f"Is Test: {IS_TEST}")
print(f"All env vars: {dict(os.environ)}") 