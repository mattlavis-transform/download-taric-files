from application import application


if __name__ == "__main__":
    app = application()
    file_from = 2
    file_to = 199
    year = "20"
    app.download(year, file_from, file_to)
