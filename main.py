import asyncio
import msvcrt
import os
import traceback
import wx
import wxasync
import utils
import views
import sys
from pathlib import Path

LOCK_FILE = Path.home() / ".bambu_printer.lock"

def check_single_instance():
    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_WRONLY)
        try:
            # Unix/Linux
            # fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Windows (uncomment if needed)
            msvcrt.locking(lock_fd, msvcrt.LK_NBLCK, 1)
        except (IOError, BlockingIOError):
            app = wx.App(False)
            wx.MessageBox("已有一个实例在运行，当前实例即将退出。", "警告", wx.OK | wx.ICON_WARNING)
            app.Destroy()
            sys.exit(1)
    except Exception as e:
        utils.logger.error(f"Failed to acquire lock: {str(e)}")
        sys.exit(1)


async def main():
    check_single_instance()
    try:
        app = wxasync.WxAsyncApp(0)
        home_frame = views.HomeFrame(None)
        home_frame.Show()
        await app.MainLoop()
    except Exception as e:
        err_msg = traceback.format_exc()
        utils.logger.error(f'start failed：{str(e)}; err_msg:{err_msg}')


if __name__ == '__main__':
    asyncio.run(main())