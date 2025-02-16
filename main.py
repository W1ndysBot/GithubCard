# script/GithubCard/main.py

import logging
import os
import sys
import re

# 添加项目根目录到sys.path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.config import *
from app.api import *
from app.switch import load_switch, save_switch


# 数据存储路径，实际开发时，请将GithubCard替换为具体的数据存放路径
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "GithubCard",
)


# 查看功能开关状态
def load_function_status(group_id):
    return load_switch(group_id, "GithubCard")


# 保存功能开关状态
def save_function_status(group_id, status):
    save_switch(group_id, "GithubCard", status)


# 处理元事件，用于启动时确保数据目录存在
async def handle_GithubCard_meta_event(websocket, msg):
    os.makedirs(DATA_DIR, exist_ok=True)


# 处理开关状态
async def toggle_function_status(websocket, group_id, message_id, authorized):
    if not authorized:
        await send_group_msg(
            websocket,
            group_id,
            f"[CQ:reply,id={message_id}]❌❌❌你没有权限对GithubCard功能进行操作,请联系管理员。",
        )
        return

    if load_function_status(group_id):
        save_function_status(group_id, False)
        await send_group_msg(
            websocket,
            group_id,
            f"[CQ:reply,id={message_id}]🚫🚫🚫GithubCard功能已关闭",
        )
    else:
        save_function_status(group_id, True)
        await send_group_msg(
            websocket, group_id, f"[CQ:reply,id={message_id}]✅✅✅GithubCard功能已开启"
        )


# 获取github卡片
async def get_github_card(websocket, group_id, message_id, raw_message):
    try:
        match = re.match(r"https://github.com/(.*)/(.*)", raw_message)
        if match:
            logging.info(f"匹配到github卡片: {match.group(1)}/{match.group(2)}")
            github_owner = match.group(1)
            github_repo = match.group(2).replace("#", "").replace("/", "")

            # opengraph
            opengraph_img_url = (
                f"https://opengraph.githubassets.com/1/{github_owner}/{github_repo}"
            )

            # 发送图片
            await send_group_msg(
                websocket,
                group_id,
                f"[CQ:reply,id={message_id}][CQ:image,file={opengraph_img_url}]",
            )

    except Exception as e:
        logging.error(f"获取github卡片失败: {e}")
        await send_group_msg(
            websocket, group_id, "获取github卡片失败，错误信息：" + str(e)
        )


# 群消息处理函数
async def handle_GithubCard_group_message(websocket, msg):
    # 确保数据目录存在
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        user_id = str(msg.get("user_id"))
        group_id = str(msg.get("group_id"))
        raw_message = str(msg.get("raw_message"))
        role = str(msg.get("sender", {}).get("role"))
        message_id = str(msg.get("message_id"))
        authorized = user_id in owner_id

        # 开关
        if raw_message == "gc":
            await toggle_function_status(websocket, group_id, message_id, authorized)
            return

        # 检查是否开启
        if load_function_status(group_id):
            # 获取github卡片
            await get_github_card(websocket, group_id, message_id, raw_message)

    except Exception as e:
        logging.error(f"处理GithubCard群消息失败: {e}")
        await send_group_msg(
            websocket,
            group_id,
            "处理GithubCard群消息失败，错误信息：" + str(e),
        )
        return


# 统一事件处理入口
async def handle_events(websocket, msg):
    """统一事件处理入口"""
    post_type = msg.get("post_type", "response")  # 添加默认值
    try:
        # 处理回调事件
        if msg.get("status") == "ok":
            return

        post_type = msg.get("post_type")

        # 处理元事件
        if post_type == "meta_event":
            return

        # 处理消息事件
        elif post_type == "message":
            message_type = msg.get("message_type")
            if message_type == "group":
                await handle_GithubCard_group_message(websocket, msg)
            elif message_type == "private":
                return

        # 处理通知事件
        elif post_type == "notice":
            if msg.get("notice_type") == "group":
                return

    except Exception as e:
        error_type = {
            "message": "消息",
            "notice": "通知",
            "request": "请求",
            "meta_event": "元事件",
        }.get(post_type, "未知")

        logging.error(f"处理GithubCard{error_type}事件失败: {e}")

        # 发送错误提示
        if post_type == "message":
            message_type = msg.get("message_type")
            if message_type == "group":
                await send_group_msg(
                    websocket,
                    msg.get("group_id"),
                    f"处理GithubCard{error_type}事件失败，错误信息：{str(e)}",
                )
            elif message_type == "private":
                await send_private_msg(
                    websocket,
                    msg.get("user_id"),
                    f"处理GithubCard{error_type}事件失败，错误信息：{str(e)}",
                )
