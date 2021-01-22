import sys
import datetime
from application import application


if __name__ == "__main__":
    app = application()
    file_from = 1
    file_to = 252

    if len(sys.argv) > 1:
        year = sys.argv[1]
        if len(year) == 2:
            year = "20" + year
    else:
        now = datetime.datetime.now()
        year = now.year

    print(year)
    app.download(year, file_from, file_to)
