import logging
import speedtest
import json
import os

LOCAL = os.getenv("LOCALAPPDATA")

file = open(f"{os.getenv("LOCALAPPDATA")}\\settings.json")
settings = json.load(file)

KB = 1024
MB = KB**2
GB = KB**3
TB = KB**4
DS_TARGET_MB = settings["DOWNLOAD_TARGET"]
US_TARGET_MB = settings["UPLOAD_TARGET"]

log_path = os.getenv("LOCALAPPDATA") + "\\"
log_name = settings["LOG_NAME"]+".log"
logging.basicConfig(format='%(levelname)s: %(message)s', filename=log_path+log_name, encoding="utf-8", level=logging.INFO)


def format_measurement(input: float):
    return input/MB


if __name__ == "__main__":
    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()
    results_dict = s.results.dict()
    download = format_measurement(results_dict["download"])
    upload = format_measurement(results_dict["upload"])

    info_str = f"download = {download:.2f} Mbps, upload = {upload:.2f} Mbps, ping = {results_dict["ping"]} ms, timestamp = {results_dict["timestamp"]}"
    if(download < DS_TARGET_MB or upload < US_TARGET_MB):
        logging.warning(info_str)
    else:
        logging.info(info_str)

