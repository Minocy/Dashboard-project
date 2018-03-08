import stock_daily
import stock_minute
import threading
from subprocess import call

def thread_second():
    call(["python", "tweetsFile.py"])

def thread_three():
    call(["python", "stock_update.py"])

processThread = threading.Thread(target=thread_second)  # <- note extra ','
processThread.start()

processThread = threading.Thread(target=thread_three)  # <- note extra ','
processThread.start()
