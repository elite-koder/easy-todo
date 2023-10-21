from easy_todo.settings import *

PROD = "PROD"
DEV = "DEV"
FABRIC = os.environ["FABRIC"]
if FABRIC == PROD:
    from easy_todo.prod_settings import *
elif FABRIC == DEV:
    pass
else:
    raise ValueError(f"Unknown FABRIC value - {FABRIC}")
