import asyncio
import traceback

import wxasync

import data
import services
import utils
import views


async def main():
    app = wxasync.WxAsyncApp()

    try:
        home_frame = views.HomeFrame(None)
        home_frame.Show()
        services.PrinterService.start_session()
        await app.MainLoop()
    except Exception as e:
        err_msg = traceback.format_exc()
        utils.logger.error(f'程序启动失败：{str(e)}; err_msg:{err_msg}')


if __name__ == '__main__':
    asyncio.run(main())
