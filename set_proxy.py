

import os
import argparse
import re

def is_ip_port(address:str) -> bool:
    pattern = r"^(\d{1,3}\.){3}\d{1,3}:\d{1,5}$"

    return bool(re.match(pattern, address))


parser = argparse.ArgumentParser(
        description= '''
            prog [-f] <http_proxy> <https_proxy> <all_proxy> 
                    '''
    )


parser.add_argument("-f", 
                    help="change the proxy forced,even when there were proxy",
                    action="store_true",
                    dest="forced", 
                    )

parser.add_argument("http_proxy", 
                    type=str, 
                    help="http_proxy->ip:port",
                    )

parser.add_argument("https_proxy", 
                    type=str, 
                    help="https_proxy->ip:port",
                    )

parser.add_argument("all_proxy", 
                    type=str, 
                    help="all_proxy->ip:port",
                    )

# 解析参数值
args = parser.parse_args()

# 读取参数值
forced = args.forced

http_proxy = args.http_proxy;
if not is_ip_port(http_proxy):
    print(f"{http_proxy} is not a address")
    exit()
http_proxy = "export http_proxy=\"http://" + http_proxy + '\"\n'

https_proxy = args.https_proxy
if not is_ip_port(https_proxy):
    print(f"{https_proxy} is not a address")
    exit()
https_proxy = "export https_proxy=\"http://" +  https_proxy + '\"\n'

all_proxy = args.all_proxy

if not is_ip_port(all_proxy):
    print(f"{all_proxy} is not a address")
    exit()

all_proxy = "export all_proxy=\"socks5://"  + all_proxy + '\n'

zshrc_path = os.path.expanduser("~/testrc")

if not os.path.exists(zshrc_path):
    print(f"the {zshrc_path} does not exist")

print(forced)

print(http_proxy)
print(https_proxy)
print(all_proxy)

try:
    lines = list()
    with open(zshrc_path, 'a+') as f:
        f.seek(0, 0)
        found = list([False, False, False])
        lines = f.readlines()
        for idx, line in  enumerate(lines):
            if line.startswith("export http_proxy"):
                found[0] = True
                if forced:
                    lines[idx] = http_proxy 
                else:
                    print("already set http_proxy")
                    exit()
            if line.startswith("export https_proxy") and forced:
                found[1] = True
                if forced:
                    lines[idx] = https_proxy 
                else:
                    print("already set https_proxy")
                    exit()
            if line.startswith("export all_proxy") and forced:
                found[2] = True
                if forced:
                    lines[idx] = all_proxy 
                else:
                    print("already set all_proxy")
                    exit()
        if not found[0]:
            lines.append(http_proxy)
        if not found[1]:
            lines.append(https_proxy)
        if not found[2]:
            lines.append(all_proxy)

    # for line in lines:
    #     print(line)
    with open(zshrc_path, 'w') as f:
        f.writelines(lines)

except FileNotFoundError:
    print(f"文件 {path} 未找到。")
except PermissionError:
    print(f"权限错误: 无法访问 {path}。")

print("set successfully to .zshrc")