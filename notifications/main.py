import logging
import argparse

import log
from delivery import DeliverySystem, LOSS_CHANCE, READ_CHANCE

NUM_USERS = 1000
NUM_MESSAGES = 10


def main():
    parser = argparse.ArgumentParser(
        prog='Notification Simulator',
        description='Simulator for delivering notifications to users.'
    )

    parser.add_argument('-u', '--numusers', type=int, default=NUM_USERS,
                        help=f'Number of users to register. Defaults to {NUM_USERS}.')
    parser.add_argument('-m', '--nummessages', type=int, default=NUM_MESSAGES,
                        help=f'Number of messages to send. Defaults to {NUM_MESSAGES}.')
    parser.add_argument('-lc', '--losschance', type=float, default=LOSS_CHANCE, metavar='[0-1]',
                        help=f'Message loss chance. Defaults to {LOSS_CHANCE}.')
    parser.add_argument('-rc', '--readchance', type=float, default=READ_CHANCE, metavar='[0-1]',
                        help=f'Message read chance. Defaults to {READ_CHANCE}.')
    parser.add_argument('-o', '--output', choices=('console', 'logfile'), default='console',
                        help='Set program output. Defaults to "console".')
    parser.add_argument('-f', '--logfile', type=str, default=log.LOGFILE,
                        help=f'Path to log file. Defaults to "{log.LOGFILE}".')
    parser.add_argument('-lv', '--loglevel', choices=log.LOG_LEVELS.keys(), default='info',
                        help='Logging level. Defaults to "info".')
    parser.add_argument('-ls', '--logsize', type=int, default=log.MAX_BYTES,
                        help=f'Max log size in bytes before rotation. Defaults to {log.MAX_BYTES}.')
    parser.add_argument('-lb', '--logbackup', type=int, default=log.BACKUP_COUNT,
                        help=f'Max number of backup logs. Defaults to {log.BACKUP_COUNT}.')

    args = parser.parse_args()

    if args.output.lower() == 'console' or not args.logfile:
        logging.basicConfig(
            level=log.LOG_LEVELS[args.loglevel.lower()],
            format=log.LOG_FORMAT,
            datefmt=log.DATETIME_FORMAT
        )
    else:
        log.configure_root_logger(
            filename=args.logfile,
            level=log.LOG_LEVELS[args.loglevel.lower()],
            max_bytes=args.logsize,
            backup_count=args.logbackup
        )

    logging.info('Launching Notification Simulator.')
    ds = DeliverySystem(loss_chance=args.losschance, read_chance=args.readchance)
    logging.info('Registering users...')
    for _ in range(args.numusers):
        ds.register_user()
    logging.info(f'Registered {args.numusers} users.')
    logging.info(f'Creating and sending messages to all registered users....')
    for _ in range(args.nummessages):
        ds.broadcast_message()
    logging.info(f'Created and sent {args.nummessages} messages.')
    logging.info('Displaying system statistics...')
    ds.show_statistics()


if __name__ == '__main__':
    main()
