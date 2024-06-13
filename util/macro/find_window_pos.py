import win32gui

def search_clinet_position(title_name):
    hwnd = win32gui.FindWindow(None, title_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        x1 = rect[0]
        y1 = rect[1]
        x2 = rect[2]
        y2 = rect[3]
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    else:
        return False


if __name__=="__main__":
    position = search_clinet_position("GersangStation")
    print(position)