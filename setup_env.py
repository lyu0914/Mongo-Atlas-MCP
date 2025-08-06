"""
环境变量设置脚本

帮助用户创建和配置.env文件
"""

import os
import sys


def create_env_file():
    """
    创建.env文件
    
    提示用户输入MongoDB Atlas连接字符串并创建.env文件
    """
    print("MongoDB Atlas MCP 服务器环境配置")
    print("=" * 50)
    
    # 检查.env文件是否已存在
    if os.path.exists('.env'):
        print("发现已存在的.env文件")
        response = input("是否要覆盖现有文件？(y/N): ").strip().lower()
        if response != 'y':
            print("取消操作")
            return
    
    print("\n请提供您的MongoDB Atlas连接字符串")
    print("连接字符串格式示例:")
    print("mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority")
    print()
    
    # 获取连接字符串
    mongodb_uri = input("请输入MongoDB Atlas连接字符串: ").strip()
    
    if not mongodb_uri:
        print("错误: 连接字符串不能为空")
        return
    
    # 验证连接字符串格式
    if not mongodb_uri.startswith('mongodb://') and not mongodb_uri.startswith('mongodb+srv://'):
        print("警告: 连接字符串格式可能不正确")
        response = input("是否继续？(y/N): ").strip().lower()
        if response != 'y':
            return
    
    # 创建.env文件内容
    env_content = f"""# MongoDB Atlas 连接配置
# 请将以下内容替换为您的实际MongoDB Atlas连接字符串
MONGODB_URI={mongodb_uri}

# 日志级别配置
LOG_LEVEL=INFO
"""
    
    try:
        # 写入.env文件
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✓ .env文件创建成功！")
        print(f"文件位置: {os.path.abspath('.env')}")
        print("\n现在您可以运行测试脚本了:")
        print("python test_mongo_atlas_mcp_safe.py")
        
    except Exception as e:
        print(f"✗ 创建.env文件失败: {str(e)}")


def validate_env_file():
    """
    验证.env文件配置
    
    检查.env文件是否存在并包含必要的配置
    """
    print("验证环境配置")
    print("=" * 30)
    
    if not os.path.exists('.env'):
        print("✗ .env文件不存在")
        print("请运行 setup_env.py 创建配置文件")
        return False
    
    # 读取.env文件
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查MONGODB_URI
        if 'MONGODB_URI=' not in content:
            print("✗ .env文件中缺少MONGODB_URI配置")
            return False
        
        # 提取连接字符串
        lines = content.split('\n')
        mongodb_uri = None
        for line in lines:
            if line.startswith('MONGODB_URI='):
                mongodb_uri = line.split('=', 1)[1].strip()
                break
        
        if not mongodb_uri:
            print("✗ MONGODB_URI值为空")
            return False
        
        print("✓ .env文件存在")
        print(f"✓ MONGODB_URI已配置: {mongodb_uri[:50]}...")
        print("\n配置验证通过！")
        return True
        
    except Exception as e:
        print(f"✗ 读取.env文件失败: {str(e)}")
        return False


def main():
    """
    主函数
    
    提供交互式菜单
    """
    print("MongoDB Atlas MCP 服务器环境配置工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建/更新.env文件")
        print("2. 验证环境配置")
        print("3. 退出")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            validate_env_file()
        elif choice == '3':
            print("退出程序")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main() 