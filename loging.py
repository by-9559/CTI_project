import logging
import time
import os



def log():
    level = logging.DEBUG
    dir = "log/"
    ls = os.listdir(dir)
    ls.sort()
    [os.remove(dir + i) for i in ls[:-5]]
    log_name = dir +"%s.log"%time.strftime("%Y%m%d%H%M", time.localtime()) 
    logger = logging.getLogger("标签检测")
    logger.setLevel(level)
    # 建立一个filehandler来把日志记录在文件里，级别为debug以上
    fh = logging.FileHandler(log_name,encoding="utf-8")
    fh.setLevel(level)
    # 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # 设置日志格式
    formatter = logging.Formatter("%(lineno)d--行-- %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    #将相应的handler添加在logger对象中
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


