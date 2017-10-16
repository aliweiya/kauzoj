sudo apt-get install rabbitmq-server
celery -A tasks worker --loglevel=info
