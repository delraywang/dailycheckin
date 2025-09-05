#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import json
import time
from datetime import datetime

# 签到URL
CHECKIN_URL = "https://mxwljsq.top/user/checkin"

# 从环境变量获取Cookie
COOKIE = os.environ.get("MXWLJSQ_COOKIE", "")

def main():
    if not COOKIE:
        print("❌ 错误: 未找到Cookie环境变量(MXWLJSQ_COOKIE)，请检查配置")
        print("请在青龙面板的环境变量中添加MXWLJSQ_COOKIE变量")
        return
    
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
        "Cookie": COOKIE
    }
    
    # 记录开始时间
    start_time = datetime.now()
    print(f"⏰ 开始执行签到任务: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 目标URL: {CHECKIN_URL}")
    print("-" * 50)
    
    try:
        # 发送POST请求进行签到
        response = requests.post(CHECKIN_URL, headers=headers, timeout=30)
        
        # 记录结束时间
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # 输出响应信息
        print(f"⏱️ 请求完成，耗时: {duration:.2f}秒")
        print(f"📊 状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            result = response.json()
            print("📄 响应内容:")
            
            # 根据响应格式处理结果
            if result.get("ret") == 1:
                print("✅ 签到成功!")
                print(f"🎁 {result.get('msg', '您获得了流量奖励')}")
            else:
                print("❌ 签到失败")
                if "msg" in result:
                    print(f"📝 失败原因: {result['msg']}")
                else:
                    print("📝 未知失败原因，请检查响应内容")
                    
            # 打印完整的响应内容（调试用）
            print("\n🔍 完整响应JSON:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        except json.JSONDecodeError:
            print("❌ 响应不是有效的JSON格式")
            print("📄 响应内容 (文本):")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ 网络连接错误，请检查网络设置")
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接或增加超时时间")
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求发生异常: {e}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
