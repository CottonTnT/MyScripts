import os

path = "/etc/resolv.conf"
newline = "nameserver 114.114.114.114"

def appendeDns():
    if os.geteuid() != 0:
        print("需要管理员权限")
        return
    
    try:
        with open(path, 'a+') as file:
            file.seek(0, 0)
            lines = file.readlines()
            if any(newline in line for line in lines):
                print("already in resolv.conf")
            
            file.write(newline + '\n')
            print(f"已成功将 '{newline}' 追加到 {path}")

    except FileNotFoundError:
        print(f"文件 {path} 未找到。")
    except PermissionError:
        print(f"权限错误: 无法访问 {path}。")

if __name__ == '__main__':
    appendeDns()
