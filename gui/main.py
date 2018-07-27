
import config as cfg
import gui
import logging
import time


try:
    # config logs
    filename = 'logs/gui_{}.log'.format(int(time.time()))
    logging.basicConfig(filename=filename, level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.captureWarnings(False)
    logging.info('GUI: Generación de Universos de Interventoría')
    # get data from db
    logging.info('Getting data from db')
    data = gui.get_data(cfg)
    # data wrangling
    logging.info('Data wrangling')
    data = gui.data_wrangling(data, cfg)
    # universe generation
    logging.info('Universe generation')
    gui.universe_generation(data, cfg)
    # send-email
    # logging.info('Sending report')
    # gui.send_report(cfg)
    logging.info('Process finished')
except Exception as exc:
    logging.exception(exc)
    # gui.send_error(cfg)
