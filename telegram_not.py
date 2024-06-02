import requests


tg_api_token = "5811187463:AAFfhimoib__HFTidYodW0Djr-0_mfunkuc"
tg_chat_id = "6171595419"


def message(text="Run Finished!"):
    requests.post(
        "https://api.telegram.org/" + "bot{}/sendMessage".format(tg_api_token),
        params=dict(chat_id=tg_chat_id, text=text),
    )
