import os

import dotenv

dotenv.load_dotenv()


SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL")
