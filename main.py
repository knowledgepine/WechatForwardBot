# -*- coding: utf-8 -*-
import itchat, time, re
from itchat.content import *
from utilities import *
from sys import argv, exit
from GlobalTextHook import GlobalTextHook
from GaTextHook import GaTextHook
from PaiDuiHook import PaiDuiHook
from HistoryRecorder import HistoryRecorder
from GroupTagCloud import GroupTagCloud
from GroupMessageForwarder import GroupMessageForwarder
from ProcessInterface import ProcessInterface
from ActivityInfo import ActivityInfo
from DoutuProcessor import DoutuProcessor
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Some global switches for debugging use only
isDebug = not True

# Component initialization
itchat.auto_login(True)
plugins = [
    GlobalTextHook({ '^/help$': """鸭哥调戏指南：
/activity: 查看本群活动和话唠排名
/tagcloud: 查看本群所有发言标签云
/mytag: 查看自己的消息标签云
/doutu: 启动斗图模式，机器人会对每一个非商城表情斗图。持续5分钟。"""}),
    GaTextHook(),
    PaiDuiHook(),
    HistoryRecorder(),
    GroupTagCloud('/Users/junsong/personal/fonts/wqy-microhei/wqy-microhei.ttc'),
    ActivityInfo('/Users/junsong/personal/fonts/wqy-microhei/wqy-microhei.ttc'),
    GroupMessageForwarder([ 'TestWoodBot', 'TestWoodBot2' ], [ 'TestWoodBot', 'TestWoodBot2' ]),
    DoutuProcessor('./DoutuFeatures.txt')  # Uncomment to enable Dou Tu
]
for plugin in plugins:
    if not isinstance(plugin, ProcessInterface):
        logging.error('One of the plugins are not a subclass of ProcessInterface.')
        exit(-1)

# Core message loops
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def picture_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg, PICTURE)
        except Exception as e:
            logging.error(e) # so that one plug's failure won't prevent others from being executed 

@itchat.msg_register([SHARING], isGroupChat=True)
def sharing_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg, SHARING)
        except Exception as e:
            logging.error(e) # so that one plug's failure won't prevent others from being executed 

@itchat.msg_register([TEXT], isGroupChat=True)
def text_reply(msg):
    if isDebug:
        logging.info(msg)
    for plugin in plugins:
        try:
            plugin.process(msg, TEXT)
        except Exception as e:
            logging.error(e) # so that one plug's failure won't prevent others from being executed 

if __name__ == '__main__':
    itchat.run()
