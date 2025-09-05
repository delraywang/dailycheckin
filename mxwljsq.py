#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cron "0 9 * * *" script-path=xxx.py,tag=匹配cron用
new Env('猫熊网络加速器')
"""

import requests
import os
import json
import time
import random
from datetime import datetime, timedelta

# ---------------- 统一通知模块加载 ----------------
hadsend = False
send = None
try:
    from notify import send
    hadsend = True
    print("✅ 已加载notify.py通知模块")
except ImportError:
    print("⚠️  未加载通知模块，跳过通知功能")

# 随机延迟配置
max_random_delay = int(os.getenv("MAX_RANDOM_DELAY", "3600"))
random_signin = os.getenv("RANDOM_SIGNIN", "true").lower() == "true"

def format_time_remaining(seconds):
    """格式化时间显示"""
    if seconds <= 0:
        return "立即执行"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}小时{minutes}分{secs}秒"
    elif minutes > 0:
        return f"{minutes}分{secs}秒"
    else:
        return f"{secs}秒"

def wait_with_countdown(delay_seconds, task_name):
    """带倒计时的随机延迟等待"""
    if delay_seconds <= 0:
        return
        
    print(f"{task_name} 需要等待 {format_time_remaining(delay_seconds)}")
    
    remaining = delay_seconds
    while remaining > 0:
        if remaining <= 10 or remaining % 10 == 0:
            print(f"{task_name} 倒计时: {format_time_remaining(remaining)}")
        
        sleep_time = 1 if remaining <= 10 else min(10, remaining)
        time.sleep(sleep_time)
        remaining -= sleep_time

def send_notification(title, content):
    """统一通知函数"""
    if hadsend:
        try:
            send(title, content)
            print(f"✅ 通知发送完成: {title}")
        except Exception as e:
            print(f"❌ 通知发送失败: {e}")
    else:
        print(f"📢 {title}")
        print(f"📄 {content}")

# 签到URL
CHECKIN_URL = "https://mxwljsq.top/user/checkin"

def mxwljsq_signin(cookie, index=1):
    """执行猫熊网络加速器签到"""
    print(f"🎯 账号{index}: 开始签到")
    
    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://mxwljsq.top",
        "Referer": "https://mxwljsq.top/user",
        "Connection": "keep-alive",
        "Cookie": cookie
    }
    
    try:
        # 发送POST请求进行签到
        response = requests.post(CHECKIN_URL, headers=headers, timeout=30)
        
        # 尝试解析JSON响应
        try:
            result = response.json()
            
            # 根据响应格式处理结果
            if result.get("ret") == 1:
                msg = result.get('msg', '您获得了流量奖励')
                print(f"✅ 账号{index}: 签到成功 - {msg}")
                return f"签到成功: {msg}", True
            else:
                error_msg = result.get('msg', '未知错误')
                print(f"❌ 账号{index}: 签到失败 - {error_msg}")
                return f"签到失败: {error_msg}", False
                
        except json.JSONDecodeError:
            print(f"❌ 账号{index}: 响应不是有效的JSON格式")
            return "签到失败: 响应不是有效的JSON格式", False
            
    except requests.exceptions.ConnectionError:
        error_msg = "网络连接错误，请检查网络设置"
        print(f"❌ 账号{index}: {error_msg}")
        return f"签到失败: {error_msg}", False
    except requests.exceptions.Timeout:
        error_msg = "请求超时，请检查网络连接或增加超时时间"
        print(f"❌ 账号{index}: {error_msg}")
        return f"签到失败: {error_msg}", False
    except requests.exceptions.RequestException as e:
        error_msg = f"请求发生异常: {e}"
        print(f"❌ 账号{index}: {error_msg}")
        return f"签到失败: {error_msg}", False
    except Exception as e:
        error_msg = f"发生未知错误: {e}"
        print(f"❌ 账号{index}: {error_msg}")
        return f"签到失败: {error_msg}", False

def main():
    """主程序入口"""
    print(f"==== 猫熊网络加速器签到开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====")
    
    # 随机延迟
    if random_signin:
        delay_seconds = random.randint(0, max_random_delay)
        if delay_seconds > 0:
            signin_time = datetime.now() + timedelta(seconds=delay_seconds)
            print(f"🎲 随机模式: 延迟 {format_time_remaining(delay_seconds)} 后开始")
            print(f"⏰ 预计开始时间: {signin_time.strftime('%H:%M:%S')}")
            wait_with_countdown(delay_seconds, "猫熊网络加速器签到")
    
    # 获取环境变量
    cookies_str = os.getenv("MXWLJSQ_COOKIE", "")
    
    if not cookies_str:
        error_msg = "❌ 未找到MXWLJSQ_COOKIE环境变量，请配置Cookie信息"
        print(error_msg)
        send_notification("猫熊网络加速器签到失败", error_msg)
        return

    # 解析多账号
    cookies = [cookie.strip() for cookie in cookies_str.split('&') if cookie.strip()]
    print(f"📝 共发现 {len(cookies)} 个账号")
    
    success_accounts = 0
    all_results = []
    
    for i, cookie in enumerate(cookies):
        try:
            # 账号间随机等待
            if i > 0:
                delay = random.uniform(5, 15)
                print(f"💤 随机等待 {delay:.1f} 秒后处理下一个账号...")
                time.sleep(delay)
            
            # 执行签到
            result_msg, is_success = mxwljsq_signin(cookie, i + 1)
            all_results.append(f"账号{i+1}: {result_msg}")
            
            if is_success:
                success_accounts += 1
            
            # 发送单个账号通知
            title = f"猫熊网络加速器账号{i+1}签到{'成功' if is_success else '失败'}"
            send_notification(title, result_msg)
            
        except Exception as e:
            error_msg = f"❌ 账号{i+1}: 处理异常 - {str(e)}"
            print(error_msg)
            all_results.append(f"账号{i+1}: {error_msg}")
            send_notification(f"猫熊网络加速器账号{i+1}签到失败", error_msg)
    
    # 发送汇总通知
    if len(cookies) > 1:
        summary_msg = f"""🐼 猫熊网络加速器签到汇总

📊 总计处理: {len(cookies)}个账号
✅ 成功账号: {success_accounts}个
❌ 失败账号: {len(cookies) - success_accounts}个
📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

详细结果:
{chr(10).join([f'  • {result}' for result in all_results])}"""
        send_notification('猫熊网络加速器签到汇总', summary_msg)
        print(f"\n📊 === 汇总统计 ===")
        print(summary_msg)
    
    print(f"\n==== 猫熊网络加速器签到完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ====")

if __name__ == "__main__":
    main()
