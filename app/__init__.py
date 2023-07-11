import logging

from app.core.config import settings

FORMAT = '%(levelname)s %(asctime)s %(module)s %(lineno)d' \
         ' %(message)s %(filename)s %(name)s'

# 'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s %(pathname)s %(name)s'

logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler(
    filename=settings.log_file_path.joinpath('demo-fastapi.log'), encoding='utf-8')
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.info("日志配置成功")

if __name__ == '__main__':
    print(settings.log_file_path.joinpath('outer.log'))
