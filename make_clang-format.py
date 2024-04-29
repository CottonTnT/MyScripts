import os
import argparse

parser = argparse.ArgumentParser(
    description='''
        prog [-f] dst_path
        prog [-f] dst_path src_path
                '''
)

parser.add_argument("--force", "-f", 
                    action="store_const", 
                    const=True, 
                    dest="is_forced")

parser.add_argument("dst_path", 
                    type=str, 
                    help="dst_path of target")

parser.add_argument("src_path", 
                    nargs="?",
                    default="~/.clang-format", 
                    type=str,
                    help="src_path of .clang-format")

args = parser.parse_args()

is_forced = args.is_forced
dst_path = os.path.join(os.path.expanduser(args.dst_path), ".clang-format")
src_path = os.path.expanduser(args.src_path)

if not os.path.exists(src_path):
    print(f"The source {src_path} file does not exist.")
    exit()

if os.path.exists(dst_path): 
    if not is_forced:
        print(f"the .clang-format is already here {dst_path},please user -f to overwrite it")
        exit()
    else:
        os.remove(dst_path)
os.symlink(src_path, dst_path)













