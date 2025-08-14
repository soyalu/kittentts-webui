#!/usr/bin/env python3
"""
KittenTTS 日志查看工具
用于查看和管理应用日志文件
"""

import os
import sys
import argparse
from datetime import datetime
import glob

def list_log_files():
    """列出所有日志文件"""
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        print("❌ logs目录不存在")
        return
    
    log_files = glob.glob(os.path.join(logs_dir, '*.log*'))
    if not log_files:
        print("📁 logs目录中没有日志文件")
        return
    
    print("📁 可用的日志文件:")
    for log_file in sorted(log_files):
        size = os.path.getsize(log_file)
        mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
        print(f"  📄 {log_file}")
        print(f"     大小: {size:,} bytes")
        print(f"     修改时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

def view_log(log_file, lines=50, follow=False):
    """查看日志文件内容"""
    if not os.path.exists(log_file):
        print(f"❌ 日志文件不存在: {log_file}")
        return
    
    print(f"📖 查看日志文件: {log_file}")
    print(f"📊 文件大小: {os.path.getsize(log_file):,} bytes")
    print("=" * 80)
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            if follow:
                # 实时跟踪日志
                print("🔄 实时跟踪日志 (按 Ctrl+C 停止)...")
                f.seek(0, 2)  # 移动到文件末尾
                while True:
                    line = f.readline()
                    if line:
                        print(line.rstrip())
                    else:
                        import time
                        time.sleep(0.1)
            else:
                # 显示最后N行
                all_lines = f.readlines()
                if lines > 0:
                    display_lines = all_lines[-lines:]
                else:
                    display_lines = all_lines
                
                for line in display_lines:
                    print(line.rstrip())
                    
    except KeyboardInterrupt:
        if follow:
            print("\n⏹️  停止跟踪日志")
    except Exception as e:
        print(f"❌ 读取日志文件时出错: {e}")

def clear_logs():
    """清理日志文件"""
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        print("❌ logs目录不存在")
        return
    
    log_files = glob.glob(os.path.join(logs_dir, '*.log*'))
    if not log_files:
        print("📁 没有日志文件需要清理")
        return
    
    print(f"🗑️  将清理 {len(log_files)} 个日志文件:")
    for log_file in log_files:
        print(f"  📄 {log_file}")
    
    confirm = input("\n❓ 确认删除这些日志文件吗? (y/N): ")
    if confirm.lower() == 'y':
        deleted_count = 0
        for log_file in log_files:
            try:
                os.remove(log_file)
                print(f"✅ 已删除: {log_file}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ 删除失败 {log_file}: {e}")
        
        print(f"\n🎉 清理完成! 共删除 {deleted_count} 个文件")
    else:
        print("❌ 取消清理操作")

def main():
    parser = argparse.ArgumentParser(description='KittenTTS 日志查看工具')
    parser.add_argument('action', choices=['list', 'view', 'clear'], 
                       help='操作类型: list(列出), view(查看), clear(清理)')
    parser.add_argument('--file', '-f', help='要查看的日志文件路径')
    parser.add_argument('--lines', '-n', type=int, default=50, 
                       help='显示的行数 (默认: 50, 0表示全部)')
    parser.add_argument('--follow', '-F', action='store_true', 
                       help='实时跟踪日志文件')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        list_log_files()
    elif args.action == 'view':
        if not args.file:
            print("❌ 请指定要查看的日志文件 (使用 --file 参数)")
            print("💡 使用 'python view_logs.py list' 查看可用文件")
            return
        view_log(args.file, args.lines, args.follow)
    elif args.action == 'clear':
        clear_logs()

if __name__ == '__main__':
    main()
