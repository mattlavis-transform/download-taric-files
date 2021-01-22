import sys
import datetime
import classes.globals as g


if __name__ == "__main__":
    file_from = 1
    file_to = 17 # 252

    if len(sys.argv) > 1:
        year = sys.argv[1]
        if len(year) == 2:
            year = "20" + year
    else:
        now = datetime.datetime.now()
        year = now.year

    g.app.download(year, file_from, file_to)
