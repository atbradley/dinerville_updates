import os
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder
import records

load_dotenv()

# Logging setup
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler = logging.handlers.RotatingFileHandler('agent.log', maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("dinerville_tools")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

home = Path.home()
dinerville_db_user = os.getenv('DINERVILLE_DB_USER')
dinerville_db_pass = os.getenv('DINERVILLE_DB_PASS')
ssh_address = os.getenv('SSH_ADDRESS')
ssh_port = int(os.getenv('SSH_PORT', 7822))

def _send_query(qry):
    logger.info(f"Executing DB query: {qry}")
    try:
        server = SSHTunnelForwarder(
            (ssh_address, ssh_port),
            ssh_username='adam',
            ssh_pkey=str(home / '.ssh/id_rsa'),
            remote_bind_address=('127.0.0.1', 3306),
            local_bind_address=('127.0.0.1', 0),      # 0 = pick a free local port
        )

        server.start()

        db = records.Database(
            f'mysql+pymysql://{dinerville_db_user}:{dinerville_db_pass}@127.0.0.1:{server.local_bind_port}/dinerville'
        )

        with db.get_connection() as conn:
            rows = conn.query(qry, fetchall=True)
            outp = rows.as_dict()
        
        logger.info(f"Query successful. Returned {len(outp)} rows.")
        return outp
    except Exception as e:
        logger.error(f"Database/Tunnel error: {e}", exc_info=True)
        return []
    finally:
        if 'db' in locals():
            db.close()
        if 'server' in locals():
            server.stop()

def random_diners(cnt:int=5) -> List[Dict[str, str]]:
    """
    Returns a list of random diners from the Dinerville database. The number of diners returned is specified by the `cnt` parameter.
    """
    logger.info("random_diners called")
    if Path('lastrandom').exists():
        with open('lastrandom') as f:
            last_random = int(f.read().strip())
    else:
        last_random = 0


    qry = f"""
CALL get_diner_data({cnt})
    """

    diners = _send_query(qry)

    if diners:
        last_random += cnt

    with open('lastrandom', 'w') as f:
         f.write(str(last_random))

    return diners
