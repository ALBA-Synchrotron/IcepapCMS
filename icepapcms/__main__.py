import logging
import logging.handlers
import queue
import os
import argparse
from .lib import ConfigManager
from .gui.icepapcms import IcepapApp


def get_parser():
    parser = argparse.ArgumentParser('Icepap Configuration Manager '
                                     'System (CMS)')
    parser.add_argument(
        "-e", "--expert", action="store_true", dest="expert",
        help="Full expert interface. False by default")
    parser.add_argument(
        "-s", "--skip-versioncheck", action="store_true",
        dest="skipversioncheck",
        help="Skip the version mismatch check. False by default")
    parser.add_argument(
        "--all-networks", action="store_true", dest="allnets",
        help="Allow all available icepap systems. False by default")
    # parser.add_argument(
    #     "--ldap", action="store_true", dest="ldap",
    #     help="Force LDAP login to get username. False by default")
    parser.add_argument("--debug-level", dest='debug_level', type=str,
                        help='Logging level used:[DEBUG, INFO, WARNING, '
                             'ERROR, CRITICAL]', default='WARNING')
    parser.add_argument("--debug-module", dest='debug_module', type=str,
                        help='Activate the logging for this module, '
                             'eg: icepapcms.gui.ipapconsole',
                        default='')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Activate the logging only for the icepap '
                             'socket communication.')

    return parser


def configure_logging():
    config_manager = ConfigManager()

    que = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(que)
    log_format = '%(asctime)s - %(message)s'
    log_console = logging.StreamHandler()
    log_console.setFormatter(logging.Formatter(log_format))

    log_filename = os.path.join(config_manager.log_folder, 'log.txt')
    log_file = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=10000000, backupCount=5)
    log_file.setFormatter(logging.Formatter(log_format))

    # Check if debug_raw_cmd is active
    if config_manager._options.debug:
        module_filter = 'icepap.tcp'
        config_manager._options.debug_level = 'debug'
    else:
        module_filter = config_manager._options.debug_module
    if module_filter:
        log_file.addFilter(logging.Filter(module_filter))
        log_console.addFilter(logging.Filter(module_filter))
    listener = logging.handlers.QueueListener(que, log_console, log_file)
    debug_levels = {'debug': logging.DEBUG,
                    'info': logging.INFO,
                    'warning': logging.WARNING,
                    'error': logging.ERROR,
                    'critical': logging.CRITICAL}
    debug_level = debug_levels[config_manager._options.debug_level.lower()]
    logging.basicConfig(level=debug_level, handlers=[queue_handler])
    return listener


def main():
    config_manager = ConfigManager()
    args = get_parser().parse_args()

    config_manager._options = args
    listener = configure_logging()

    listener.start()
    app = IcepapApp()
    app.start()
    listener.stop()


if __name__ == "__main__":
    main()

