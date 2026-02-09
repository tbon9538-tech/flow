import os
import sys
import random
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, timezone
from pathlib import Path
from multiprocessing import Pool, freeze_support

# --- 0. 高端打包路径兼容逻辑 ---
def get_resource_path(relative_path):
    """获取程序运行时资源的绝对路径 (适配 PyInstaller)"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 运行时的临时文件夹路径
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 定义引擎路径 (确保 ffmpeg.exe 和 exiftool.exe 在同一目录)
FFMPEG_EXE = get_resource_path("ffmpeg.exe")
EXIFTOOL_EXE = get_resource_path("exiftool.exe")

# --- 1. 全球热门投放地区指纹库 & 硬件设备池 ---

# [新增] 硬件指纹池：避免单一设备号风控
DEVICE_POOL = [
    ("Apple", "iPhone 14 Pro", "16.1.1"),
    ("Apple", "iPhone 15 Pro", "17.0.2"),
    ("Apple", "iPhone 15 Pro Max", "17.2.1"),
    ("Apple", "iPhone 16 Pro", "18.0"),
    ("Apple", "iPhone 16 Pro Max", "18.1"),
    ("Samsung", "SM-S928B", "Android 14"), # Galaxy S24 Ultra 国际版
    ("Google", "Pixel 8 Pro", "Android 14")
]

def select_timezone_visual():
    """GUI 选择目标市场时区"""
    tz_map = {
        "🇺🇸 美国-洛杉矶 (西海岸 UTC-8)": {"offset": -8, "ext": ".MOV"},
        "🇺🇸 美国-纽约 (东海岸 UTC-5)": {"offset": -5, "ext": ".MOV"},
        "🇯🇵 日本-东京 (JST/UTC+9)": {"offset": 9, "ext": ".MOV"},
        "🇰🇷 韩国-首尔 (KST/UTC+9)": {"offset": 9, "ext": ".MOV"},
        "🇬🇧 英国-伦敦 (GMT/UTC+0)": {"offset": 0, "ext": ".mp4"},
        "🇩🇪 德国-柏林 (CET/UTC+1)": {"offset": 1, "ext": ".mp4"},
        "🇭🇰 中国-香港 (HKT/UTC+8)": {"offset": 8, "ext": ".mp4"},
        "🇻🇳 越南-河内 (ICT/UTC+7)": {"offset": 7, "ext": ".mp4"},
        "🇸🇬 新加坡 (SGT/UTC+8)": {"offset": 8, "ext": ".mp4"}
    }
    selected_data = [None]
    
    def on_confirm():
        choice = combo.get()
        if choice in tz_map:
            selected_data[0] = tz_map[choice]
            root.destroy()
        else:
            messagebox.showwarning("警告", "请先选择目标市场")

    root = tk.Tk()
    root.title("PolaFlow Global Hacker v22.0 - Final")
    root.geometry("450x280")
    
    lbl = tk.Label(root, text="🌍 增长黑客版：选择目标投放地区\n(自动匹配时区、硬件指纹、音频混响)", 
                   pady=20, font=("Arial", 10, "bold"))
    lbl.pack()
    
    combo = ttk.Combobox(root, values=list(tz_map.keys()), width=45, state="readonly")
    combo.set("--- 点击选择市场 ---")
    combo.pack(pady=5)
    
    btn = tk.Button(root, text="🚀 启动全维度重构矩阵", command=on_confirm, 
                    bg="#1a73e8", fg="white", width=25, height=2)
    btn.pack(pady=25)
    
    root.mainloop()
    return selected_data[0]

# --- 2. 滤镜与视觉重构逻辑 (保持财经质感) ---
def get_ultimate_visual_chain():
    # 随机参数生成
    k1 = random.uniform(-0.015, 0.015)       # 极微小镜头畸变
    chroma = random.uniform(0.6, 1.4)        # 色散位移
    freq = random.uniform(2, 4.5)            # 降噪频率
    noise = random.randint(3, 6)             # 底噪强度
    rot = random.uniform(-0.01, 0.01)        # 微旋转
    
    # 财经质感曲线：轻微提升对比度与清晰度
    financial_curves = "curves=all='0/0 0.2/0.15 0.5/0.5 0.8/0.85 1/1'"
    
    # 构建滤镜链
    return [
        f"dctdnoiz=s={freq}:n=2",                              # 频域降噪 (破坏原始噪点指纹)
        "scale=iw:-1:flags=lanczos+accurate_rnd",              # 采样重算
        f"lenscorrection=k1={k1}:k2=0.001",                    # 几何重构
        f"chromaberrap=rh={chroma}:rv={chroma}:gh=0.3:gv=0.3", # 模拟光学瑕疵
        f"vignette='PI/4+{random.uniform(0.05, 0.1)}'",        # 边缘暗角 (改变直方图)
        f"rotate={rot}:fillcolor=black:ow=iw:oh=ih",           # 旋转破坏矩阵对齐
        f"noise=alls={noise}:allf=t+u",                        # 注入新指纹噪点
        financial_curves,                                      # 调色
        "format=yuv420p"                                       # 兼容性输出
    ]

def mutate_video(input_file, output_file, config):
    offset = config['offset']
    
    # --- [升级] 动态音频滤镜 (微混响) ---
    # e_delay 控制在 0.002-0.02s (2ms-20ms)，产生“加厚/金属”音色，不影响语音清晰度
    h_gain = round(random.uniform(3, 8), 2)
    e_delay = round(random.uniform(0.002, 0.02), 4)  
    e_decay = round(random.uniform(0.05, 0.15), 2)
    
    # anequalizer: 提升高频空气感
    # aecho: 极短延迟混响，改变声纹波形
    ap = f"anequalizer=c0 f=20000 w=2000 g={h_gain},aecho=0.8:0.88:{e_delay}:{e_decay}"
    
    # 视觉呼吸与随机裁切
    sj = f"crop=iw-4:ih-4:{random.randint(0,4)}:{random.randint(0,4)},scale=1080:1920"
    lb = f"geq=lum='p(x,y)*(1+0.005*sin(2*PI*0.5*t))'" # 亮度呼吸 (Luma Breath)
    
    vf = ",".join(get_ultimate_visual_chain() + [sj, lb])
    
    # FFmpeg 渲染指令
    cmd = [
        FFMPEG_EXE, '-y', '-hide_banner', '-loglevel', 'error', 
        '-i', str(input_file),
        '-vf', vf, 
        '-af', ap, 
        '-c:v', 'libx264', 
        '-crf', str(random.randint(18, 22)),   # 动态码率
        '-preset', 'fast', 
        '-map_metadata', '-1',                 # 清除原始元数据
        '-c:a', 'aac', '-ar', '44100', '-b:a', '128k', 
        str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        
        # --- [升级] 时序重构与硬件伪装 ---
        
        # 1. 计算当地时间
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        # 随机回拨 2-24 小时作为“拍摄时间”
        cap_dt = target_now - timedelta(minutes=random.randint(120, 1440))
        ts = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{"+" if offset >= 0 else "-"}{abs(offset):02d}:00')
        
        # 2. 从池中随机抽取设备
        make_val, model_val, sw_val = random.choice(DEVICE_POOL)
        
        # 3. ExifTool 深度注入
        exif_cmd = [
            EXIFTOOL_EXE, '-overwrite_original', 
            f"-Make={make_val}", 
            f"-Model={model_val}",
            f"-Software={sw_val}",
            f"-CreateDate={ts}", 
            f"-ModifyDate={ts}", 
            f"-DateTimeOriginal={ts}", 
            f"-InternalSerialNumber=SN{random.getrandbits(32)}", # 随机序列号
            str(output_file)
        ]
        
        subprocess.run(exif_cmd, stdout=subprocess.DEVNULL)
        
        # 4. 修改文件系统时间 (utime)
        os.utime(output_file, (cap_dt.timestamp(), cap_dt.timestamp()))
        
        print(f"[+] 成功: {input_file.name} -> 模拟设备: {model_val}")
        return True
        
    except Exception as e:
        print(f"[!] 处理失败: {input_file.name} | {e}")
        return False

# --- 3. 自动化任务引擎 ---
def main():
    # 必须在多进程任务前调用，防止 EXE 递归崩溃
    freeze_support()
    
    config = select_timezone_visual()
    if config:
        in_p, out_p = Path("./raw"), Path("./output")
        in_p.mkdir(exist_ok=True)
        out_p.mkdir(exist_ok=True)
        
        # 扫描 .mp4 和 .mov
        tasks = [(f, out_p / f"FIN_{random.randint(10000, 99999)}_{f.stem}{config['ext']}", config) 
                 for f in in_p.glob("*.*") if f.suffix.lower() in ('.mp4', '.mov')]
        
        if not tasks:
            print("[!] raw 文件夹无视频。请放入素材。")
            return

        print(f"[*] 引擎启动 | 核心数: {os.cpu_count()} | 任务数: {len(tasks)}")
        print(f"[*] 正在进行: 视觉重构 -> 音频混响(20ms) -> 硬件指纹随机化 -> 时区对齐")
        
        with Pool(os.cpu_count()) as pool:
            pool.starmap(mutate_video, tasks)
            
        print("[+] 所有任务处理完成。请检查 output 文件夹。")

if __name__ == "__main__":
    main()