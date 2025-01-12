from utils import logger


class PrinterTranslater(object):
    def __init__(self):
        self._trans_map = {
            'AMS1 Slot3 filament has run out. Please insert a new filament.': 'AMS1 3号耗材耗尽，请添加新的耗材。'
        }

    def translate(self, text):
        if text not in self._trans_map:
            logger.error(f'未翻译内容， text：{text}')
        return self._trans_map.get(text, text)


printerTranslater = PrinterTranslater()
