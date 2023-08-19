from os import getenv

from dotenv import load_dotenv

load_dotenv(".env")


API_ID = int(getenv("API_ID", "15351180"))
OWNER = int(getenv("OWNER", "902620564"))
API_HASH = getenv("API_HASH", "adaa1fa337b0dc151e106f6090e59627")
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://1:1@cluster0.ns6rjhr.mongodb.net/?retryWrites=true&w=majority")
BOT_TOKEN = getenv("BOT_TOKEN", "6498090143:AAHLOptNjpQDQsdy1kRdGdCTRRKr-zaGa94")
OPENAI_API = getenv("OPENAI_API", "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")
GIT_TOKEN = getenv("GIT_TOKEN", "")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
BRANCH = getenv("BRANCH", "naya")  # don't change
REPO_URL = getenv("REPO_URL", "https://github.com/naya1503/Naya-Pyro")
CMD_HNDLR = getenv("CMD_HNDLR", "n")
SESSION1 = getenv("SESSION1", "BQAhIHQAvyWjMb6R1ps8afvqgzufnssurnRd46Uqr0WmkPGYDxAaQJRq0zRx1kPY5nfwh6IxL3Z6TGIlfbnNPgXHlahqY-z3pMeSQPj23-2OZM92jfK3U7ejt2e0kHuaqF5RtcHCDLhtR_hFWyDksjL3OeW0uYCcSXPNq1mnZ6uNmMGjnbpyw5jJsfrfknCkrBKgjV1x_aJzbgiKF43_cIsRKjo_cDZI46jI3OlusvhFN3AJKk6jCxlOfXYrnXQz4aw6FbBwbYZbKu3YTWeNBXHckR_njnnxSsXTiGz7X7H6UUk5wGMtLPnssN2tzY0W_1ak945e2M8FhMPCyDgAo7H6Wlr-9AAAAAA1zOWUAA")
SESSION2 = getenv("SESSION2", "")
SESSION3 = getenv("SESSION3", "")
SESSION4 = getenv("SESSION4", "")
SESSION5 = getenv("SESSION5", "")

