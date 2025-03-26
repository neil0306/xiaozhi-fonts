import os
import sys
import argparse
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description='Font converter utility')
    parser.add_argument('type', choices=['lvgl', 'dump'], help='Output type: lvgl or dump')
    parser.add_argument('--font-size', type=int, default=14, help='Font size (default: 14)')
    parser.add_argument('--bpp', type=int, default=4, help='Bits per pixel (default: 4)')
    parser.add_argument('--language', choices=['zh_cn', 'zh_tc'], default='zh_cn', help='Language (default: zh_cn): zh_cn/zh_tc')
    return parser.parse_args()

def load_symbols():
    symbols = ["•", "·", "÷", "×", "©", "¥", "®"]
    for line in open("GB2312.TXT"):
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        unicode = int(parts[1], 16)
        symbols.append(chr(unicode))
    return symbols

def load_symbols_zh_tc():
    symbols = ["•", "·", "÷", "×", "©", "¥", "®"]
    for line in open("BIG5.TXT"):
        if line.startswith("#") or line.strip() == "":
            continue
        parts = line.split()
        unicode = int(parts[1], 16)
        symbols.append(chr(unicode))
    return symbols

def main():
    args = parse_arguments()
    
    flags = "--force-fast-kern-format --no-compress --no-prefilter"
    
    if args.language == "zh_cn":
        font = "AlibabaPuHuiTi-3-55-Regular.ttf"
        symbols = load_symbols()
        output = f"src/font_puhui_{args.font_size}_{args.bpp}.c"
    elif args.language == "zh_tc":
        font = "NotoSansTC-Regular.ttf"
        symbols = load_symbols_zh_tc()
        output = f"src/font_noto_{args.font_size}_{args.bpp}_{args.language}.c"
    
    if args.type == "lvgl":
        symbols_str = "".join(symbols)
    else:  # dump
        output = f"./dump"
        symbols_str = "欢迎使用小智聊天机器人，这是一个纯手工打造的人工智能硬件产品。"
        cmd = f"lv_font_conv {flags} --font {font} --format dump --bpp {args.bpp} -o {output} --size {args.font_size} -r 0x20-0x7F --symbols {symbols_str}"

    print("Total symbols:", len(symbols_str))
    print("Generating", output)

    ret = subprocess.call(["lv_font_conv", "--force-fast-kern-format", "--no-compress", "--no-prefilter", 
                    "--font", font, 
                    "--format", "lvgl",
                    "--lv-include", "lvgl.h",
                    "--bpp", str(args.bpp),
                    "-o", output,
                    "--size", str(args.font_size),
                    "-r", "0x20-0x7F",
                    "--symbols", symbols_str])
    if ret != 0:
        print(f"命令执行失败，返回码：{ret}")
    else:
        print("命令执行成功")

if __name__ == "__main__":
    main()

