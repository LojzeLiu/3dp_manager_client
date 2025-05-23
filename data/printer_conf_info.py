import sqlite3

import models
import utils


class PrinterConfInfo(object):
    def __init__(self, db_name=f"{utils.env_set.base_dir}/bambu.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_table()

    def setup_table(self):
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS conf_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    hostname TEXT,
                    access_code TEXT,
                    serial_number TEXT
                )
            ''')
        self.conn.commit()

    def add_conf_info(self, conf_info):
        self.cursor.execute('''
                INSERT INTO conf_info (name, hostname, access_code, serial_number)
                VALUES (?, ?, ?, ?)
            ''', (conf_info.name, conf_info.hostname, conf_info.access_code, conf_info.serial_number))
        self.conn.commit()

    def get_all_conf_info(self):
        self.cursor.execute('SELECT * FROM conf_info')
        rows = self.cursor.fetchall()
        return [models.BambuConfInfo(name=row[1], hostname=row[2], access_code=row[3], serial_number=row[4]) for row in
                rows]

    def get_all_conf_id(self, name: str, hostname: str, access_code: str):
        self.cursor.execute(
            'SELECT * FROM conf_info WHERE name = ? AND hostname=? AND access_code=?',
            (name, hostname, access_code))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            return rows[0][0]
        return -1

    def update_conf_info(self, conf_id, conf_info: models.BambuConfInfo):
        self.cursor.execute('''
                UPDATE conf_info
                SET name = ?, hostname = ?, access_code = ?, serial_number = ?
                WHERE id = ?
            ''', (conf_info.name, conf_info.hostname, conf_info.access_code, conf_info.serial_number, conf_id))
        self.conn.commit()

    def delete_conf_info(self, id):
        self.cursor.execute('DELETE FROM conf_info WHERE id = ?', (id,))
        self.conn.commit()

    def add_config_info(self, name: str, hostname: str, access_code: str, serial_number: str):
        """
        向 conf_info 表中添加新的打印机配置信息

        参数:
            name (str): 打印机名称
            hostname (str): 打印机主机名/IP地址
            access_code (str): 访问代码/密码
        """
        self.cursor.execute('''
            INSERT INTO conf_info (name, hostname, access_code, serial_number)
            VALUES (?, ?, ?, ?)
        ''', (name, hostname, access_code, serial_number))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
