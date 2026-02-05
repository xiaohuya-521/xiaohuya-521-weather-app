''''
天气查询工具 v1.0 - 命令行版本
作者：xiaohuya-521
GitHub: https://github.com/xiaohuya-521/xiaohuya-521-weather-app
"""

import requests
import json

def get_weather(city):
    """
    获取指定城市的天气信息
    
    参数:
        city (str): 城市名称，如"北京"、"上海"
    
    返回:
        dict: 包含天气信息的字典，或包含错误信息的字典
    """
    try:
        # 使用免费的天气API
        url = f"http://wthrcdn.etouch.cn/weather_mini?city={city}"
        
        # 发送网络请求，设置5秒超时
        response = requests.get(url, timeout=5)
        
        # 检查请求是否成功
        if response.status_code == 200:
            data = response.json()  # 解析JSON数据
            
            if data["status"] == 1000:  # API返回成功
                weather_data = data["data"]
                
                # 整理需要的信息
                return {
                    "city": weather_data["city"],           # 城市名称
                    "temperature": weather_data["wendu"],   # 温度
                    "advice": weather_data["ganmao"],       # 生活建议
                    "forecast": weather_data["forecast"][0] # 今日天气预报
                }
            else:
                return {"error": "城市不存在或查询失败"}
        else:
            return {"error": f"网络请求失败，状态码: {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"error": "请求超时，请检查网络连接"}
    except requests.exceptions.ConnectionError:
        return {"error": "网络连接失败"}
    except Exception as e:
        return {"error": f"程序异常: {str(e)}"}

def display_weather(result):
    """
    漂亮地显示天气信息
    
    参数:
        result (dict): get_weather函数返回的结果
    """
    if "error" in result:
        print(f"❌ 查询失败: {result['error']}")
        return False
    
    # 使用表情符号让显示更友好
    print("\n" + "=" * 40)
    print(f"📍 {result['city']} 天气信息")
    print("=" * 40)
    print(f"🌡️  当前温度: {result['temperature']}℃")
    print(f"☁️  今日天气: {result['forecast']['type']}")
    print(f"🌬️  风向风力: {result['forecast']['fengxiang']} {result['forecast']['fengli']}")
    print(f"📅 日期: {result['forecast']['date']}")
    print(f"💡 生活建议: {result['advice']}")
    print("=" * 40)
    
    return True

def main():
    """
    主函数，程序入口
    """
    print("=" * 50)
    print("🌤️  天气查询工具 v1.0")
    print("=" * 50)
    print("功能: 查询全国城市实时天气")
    print("提示: 输入城市名称查询，输入'q'退出程序")
    print("=" * 50)
    
    query_count = 0  # 查询次数统计
    
    while True:
        try:
            # 获取用户输入
            city = input("\n🏙️  请输入城市名称 (输入 q 退出): ").strip()
            
            # 检查是否退出
            if city.lower() == 'q':
                print(f"\n感谢使用！本次共查询 {query_count} 次。")
                break
            
            # 检查输入是否为空
            if not city:
                print("⚠️  请输入有效的城市名称")
                continue
            
            # 查询天气
            print(f"🔍 正在查询 {city} 的天气...")
            result = get_weather(city)
            
            # 显示结果
            if display_weather(result):
                query_count += 1
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被中断，感谢使用！")
            break
        except Exception as e:
            print(f"❌ 程序出错: {e}")

def run_example():
    """
    运行示例查询，用于测试
    """
    print("\n运行示例查询...")
    
    test_cities = ["北京", "上海", "广州", "深圳"]
    
    for city in test_cities:
        print(f"\n查询 {city}:")
        result = get_weather(city)
        display_weather(result)

if __name__ == "__main__":
    # 可以选择直接运行主程序，或运行示例
    main()
    # 或者运行示例: run_example()
