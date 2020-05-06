import logging
import logging.handlers
import queue
import os
import argparse
from .lib_icepapcms import ConfigManager
from .ui_icepapcms.icepapcms import IcepapApp


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
    parser.add_argument(
        "--ldap", action="store_true", dest="ldap",
        help="Force LDAP login to get username. False by default")
    parser.add_argument("--debug-level", dest='debug_level', type=str,
                        help='Logging level used:[DEBUG, INFO, WARNING, '
                             'ERROR, CRITICAL]', default='WARNING')
    parser.add_argument("--debug-module", dest='debug_module', type=str,
                        help='Activate the logging for this module, '
                             'eg: icepapCMS.ui_icepapcms.ipapconsole',
                        default='')

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

    filter = config_manager._options.debug_module
    if filter:
        log_file.addFilter(logging.Filter(filter))
        log_console.addFilter(logging.Filter(filter))
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

    # Read configuration from environment
    ldap = os.environ.get('ICEPAP_LDAP', '')
    allnets = os.environ.get('ICEPAP_ALL_NETWORKS', '')
    if ldap.lower() in ['yes', 'true']:
        args.ldap = True
    if allnets.lower() in ['yes', 'true']:
        args.allnets = True

    config_manager._options = args
    listener = configure_logging()

    listener.start()
    app = IcepapApp()
    app.start()
    listener.stop()


if __name__ == "__main__":
    main()

