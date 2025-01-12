from datetime import datetime
from threading import Thread
import wx
import requests
import utils


def get_order(base_url, username: str, token: str, car_id, plan_id):
    """获取订单"""
    headers = {
        "Host": "fz.evennet.cn",
        "Connection": "keep-alive",
        "Content-Length": "70",
        "Device-Type": "wxapp",
        "xweb_xhr": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI "
                      "MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555",
        "token": token,
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wx78a562cb12b6d9fa/43/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    data = {
        "driverId": username,
        "sendCarId": car_id,
        "appointPlanId": plan_id,
    }

    response = requests.post(f'{base_url}/msyapi/customerTransportInfo/driverAppointment', json=data,
                             headers=headers, stream=True,
                             verify=False)
    if response.status_code != 200:
        utils.logger.error(f'获取订单接口返回错误，状态码：{response.status_code}; 返回信息：{response.json()}')
        raise ValueError('获取订单接口返回错误')
    utils.logger.debug(f'response:{response.text}')
    resp_info = response.json()
    resp_state = resp_info.get('success')
    return resp_state


def thread_get_order(base_url, username: str, token: str, car_id, plan_id, try_count):
    state = False
    try_index = 1
    while not state and try_index <= try_count:
        state = get_order(base_url, username, token, car_id, plan_id)
        utils.logger.debug(f'用户：{username}; 尝试第{try_index}次, 共计尝试：{try_count}, 结果：{state};')
        try_index = try_index + 1


class AutoOrder:
    def __init__(self):
        self.base_url = 'https://fz.evennet.cn'

    def force_get(self, username: str, token: str):
        task_infos = self.get_driver_tasks(username, token)
        if len(task_infos) <= 0:
            wx.MessageBox(f'未获取到工作列表！', '未完成', wx.OK | wx.ICON_INFORMATION)
        utils.logger.debug(f'task_infos:{task_infos}')
        for task_info in task_infos:
            task_id = int(task_info.get('id'))
            colliery_name = task_info.get('colliery_name')
            plan_infos = self.get_appointment_list(username, token, task_id)

            utils.logger.debug(f'获取计划:{plan_infos}')
            if len(plan_infos) <= 0:
                wx.MessageBox(f'未获取到计划列表！', '未完成', wx.OK | wx.ICON_INFORMATION)
            for plan_info in plan_infos:
                plan_id = plan_info.get('plan_id')
                goods_name = plan_info.get('goods_name')
                state = get_order(self.base_url, username, token, task_id, plan_id)
                utils.logger.debug(f'手动抢单，用户：{username}; 煤矿：{colliery_name}; 工作：{goods_name}; 结果：{state};')
                state_msg = '失败'
                if state:
                    state_msg = '成功'
                wx.MessageBox(f'用户：{username}；煤矿：{colliery_name}; 工作：{goods_name}; 抢单：{state_msg}',
                              '完成抢单', wx.OK | wx.ICON_INFORMATION)

    def start_get(self, infos, try_count: int = 3):
        is_finish = False
        if len(infos) > 0:
            info = infos[0]
            username = info[1]
            token = info[2]
            task_infos = self.get_driver_tasks(username, token)
            utils.logger.debug(f'username:{username};task_infos:{task_infos}')
            for task_info in task_infos:
                task_id = int(task_info.get('id'))
                colliery_name = task_info.get('colliery_name')
                plan_infos = self.get_appointment_list(username, token, task_id)
                utils.logger.debug(f'username:{username}; plan_infos:{plan_infos}')
                for plan_info in plan_infos:
                    plan_id = plan_info.get('plan_id')
                    plan_num = plan_info.get('plan_num')
                    appoint_num = plan_info.get('appoint_num')
                    goods_name = plan_info.get('goods_name')
                    if plan_num != appoint_num:
                        for curr_info in infos:
                            curr_username = curr_info[1]
                            curr_token = curr_info[2]
                            utils.logger.debug(
                                f'开始抢单，用户：{curr_username}; 煤矿：{colliery_name}; 工作：{goods_name}')
                            p = Thread(target=thread_get_order,
                                       args=(
                                           self.base_url, curr_username, curr_token, task_id, plan_id, try_count))
                            p.start()
                        is_finish = True
                    else:
                        utils.logger.debug(f'计划已满 煤矿：{colliery_name}; 工作：{goods_name}; 用户：{username};')
        return is_finish

    def get_driver_tasks(self, username: str, token: str):
        """获取工作列表"""

        # 请求头
        headers = {
            'Host': 'fz.evennet.cn',
            'Connection': 'keep-alive',
            'Content-Length': '36',
            'Device-Type': 'wxapp',
            'xweb_xhr': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI '
                          'MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555',
            'token': token,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wx78a562cb12b6d9fa/43/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        # 请求body
        data = {
            "driverId": username,
            "state": 0
        }

        # 发送POST请求
        response = requests.post(f'{self.base_url}/msyapi/customerSendCarDetail/queryDriverTask', json=data,
                                 headers=headers, stream=True,
                                 verify=False)
        if response.status_code != 200:
            utils.logger.error(f'获取工作接口返回错误，状态码：{response.status_code};返回信息：{response.json()}')
            raise ValueError('获取工作接口返回错误')
        ids = []
        resp_info = response.json()

        success = resp_info.get('success', False)
        if not success:
            utils.logger.error(f'获取计划接口返回错误，success：{success};返回信息：{resp_info}')
            raise ValueError('获取计划接口返回错误')

        resp_data = resp_info.get('data', None)
        if resp_data is None:
            utils.logger.error(f'获取任务接口未返回data，info:{resp_info};')
            return ids
        resp_datalist = resp_data.get('datalist', None)
        if resp_datalist is None:
            utils.logger.error(f'获取任务接口未返回 datalist，data:{resp_data};')
            return ids
        for task_info in resp_datalist:
            task_id = task_info.get('detailId')
            colliery_name = task_info.get('collieryName')
            info = {
                'id': int(task_id),
                'colliery_name': colliery_name
            }
            ids.append(info)
        return ids

    def get_appointment_list(self, username: str, token: str, car_id):
        """获取计划ID"""
        headers = {
            "Host": "fz.evennet.cn",
            "Connection": "keep-alive",
            "Content-Length": "47",
            "Device-Type": "wxapp",
            "xweb_xhr": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI "
                          "MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555",
            "token": token,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wx78a562cb12b6d9fa/43/page-frame.html",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

        data = {
            "driverId": username,
            "sendCarId": car_id
        }

        response = requests.post(f'{self.base_url}/msyapi/customerTransportInfo/queryDriverAppointmentList', json=data,
                                 headers=headers, stream=True,
                                 verify=False)
        if response.status_code != 200:
            utils.logger.error(f'获取计划接口返回错误，状态码：{response.status_code};返回信息：{response.text}')
            raise ValueError('获取计划接口返回错误')
        resp_info = response.json()
        success = resp_info.get('success', False)
        if not success:
            utils.logger.error(f'获取计划接口返回错误，success：{success};返回信息：{resp_info}')
            raise ValueError('获取计划接口返回错误')
        resp_data = resp_info.get('data')
        plan_ids = []
        if resp_data is None:
            utils.logger.error(f'获取计划接口未返回 data，info:{resp_info};')
            return plan_ids
        resp_datalist = resp_data.get('datalist', None)
        if resp_datalist is None:
            utils.logger.error(f'获取计划接口未返回 datalist，data:{resp_data};')
            return plan_ids
        for info in resp_datalist:
            plan_id = info.get('appointPlanId')
            plan_num = info.get('planNum')
            appoint_num = info.get('appointNum')
            goods_name = info.get('goodsName')
            appoint_date = info.get('appointDate')
            date_format = "%Y-%m-%d %H:%M:%S%z"
            # 转换字符串为时间格式
            formatted_date = datetime.strptime(appoint_date, date_format)
            curr_date = datetime.now()
            utils.logger.debug(f'计划时间：{appoint_date}； 解析时间:{formatted_date}')
            if curr_date.day + 1 == formatted_date.day:
                plan_ids.append({
                    'plan_id': plan_id,
                    'plan_num': plan_num,
                    'appoint_num': appoint_num,
                    'goods_name': goods_name,
                })
        return plan_ids
