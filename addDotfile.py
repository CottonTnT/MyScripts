import os
import sys
import shutil
import argparse

def createSymlink(source, destination):

    """创建软链接。"""
    try:
        os.symlink(source, destination)
        print(f"创建软链接：{destination} -> {source}")
    except OSError as e:
        print(f"创建软链接失败：{e}")
        sys.exit(1)

def moveFileAndCreateSymlink(file_path, target_dir):
    """移动文件并创建软链接。"""

    # 规范化路径，处理相对路径和绝对路径
    file_path = os.path.abspath(file_path)
    target_dir = os.path.abspath(target_dir)

    # 检查文件和目录是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在")
        sys.exit(1)

    if not os.path.isdir(target_dir):
        print(f"错误：目标目录 {target_dir} 不是一个目录")
        sys.exit(1)

    filename = os.path.basename(file_path)
    destination_path = os.path.join(target_dir, filename)

    # 检查目标位置是否已存在同名文件
    if os.path.exists(destination_path):
        print(f"错误：目标位置 {destination_path} 已存在同名文件")
        sys.exit(1)

    try:
        shutil.move(file_path, destination_path)
        print(f"移动文件：{file_path} -> {destination_path}")
    except OSError as e:
        print(f"移动文件失败：{e}")
        sys.exit(1)

    createSymlink(destination_path, file_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="move the file(abs or relate) to the dir ~/dotfiles")
    parser.add_argument("file_path", help="the path of file, absolute path or relative path")
    parser.add_argument("target_dir", nargs="?", default=os.path.expanduser("~/dotfiles"),
                        help="目标目录路径（相对或绝对，默认为 ~/dotfiles）。")

    args = parser.parse_args()

    # 检查默认目录是否存在，不存在则创建
    default_dotfiles_dir = os.path.expanduser("~/dotfiles")

    if args.target_dir == default_dotfiles_dir and not os.path.exists(default_dotfiles_dir):
        try:
            os.makedirs(default_dotfiles_dir)
            print(f"创建默认目录：{default_dotfiles_dir}")
        except OSError as e:
            print(f"创建默认目录失败：{e}")
            sys.exit(1)

    moveFileAndCreateSymlink(args.file_path, args.target_dir)