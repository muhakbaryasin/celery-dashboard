import logging

logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s',
      filename='app.log',
      filemode='a')

Logger = logging