import sys
from datetime import datetime
import classes.globals as g


if __name__ == "__main__":
    if len(sys.argv) > 1:
        d2 = sys.argv[1]

    else:
        d = datetime.now()
        d2 = d.strftime('%Y-%m-%d')

    if len(sys.argv) > 2:
        scope = sys.argv[2]

    else:
        scope = "eu"

    g.app.create_commodity_extract(scope, d2)
