import asyncio
import traceback
import wxasync
import utils
import views


async def main():
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
