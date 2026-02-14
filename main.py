import os
import sys
import random
import subprocess
import uuid
import platform
import time
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, timezone
from pathlib import Path
from multiprocessing import Pool, freeze_support

# ==========================================
# 0. 基础环境配置 (v29.0 God Mode)
# ==========================================
def get_resource_path(relative_path):
    """获取资源绝对路径，适配 PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 自动判断系统后缀
EXT = ".exe" if platform.system() == "Windows" else ""
FFMPEG_EXE = get_resource_path(f"ffmpeg{EXT}")
EXIFTOOL_EXE = get_resource_path(f"exiftool{EXT}")

# 兜底检测
if not os.path.exists(FFMPEG_EXE): FFMPEG_EXE = "ffmpeg"
if not os.path.exists(EXIFTOOL_EXE): EXIFTOOL_EXE = "exiftool"

# ==========================================
# 1. 逻辑自洽数据库 (设备 x 格式 x 固件)
# ==========================================
DEVICE_DATABASE = [
    # (厂商, 型号, 固件版本, [支持后缀列表])
    ("Apple", "iPhone 14 Pro", "16.1.1", [".MOV"]),
    ("Apple", "iPhone 15 Pro", "17.0.2", [".MOV"]),
    ("Apple", "iPhone 15 Pro Max", "17.2.1", [".MOV"]),
    ("Apple", "iPhone 16 Pro", "18.0", [".MOV"]),
    ("Apple", "iPhone 16 Pro Max", "18.1", [".MOV"]),
    ("Samsung", "SM-S928B", "Android 14", [".mp4"]), # S24 Ultra
    ("Google", "Pixel 8 Pro", "Android 14", [".mp4"])
]

# ==========================================
# 2. 全球战场选择器
# ==========================================
def select_timezone_visual():
    tz_map = {
        "🇺🇸 美国-洛杉矶 (UTC-8)": (-8, 34.0522, -118.2437),
        "🇺🇸 美国-纽约 (UTC-5)": (-5, 40.7128, -74.0060),
        "🇬🇧 英国-伦敦 (UTC+0)": (0, 51.5074, -0.1278),
        "🇩🇪 德国-柏林 (UTC+1)": (1, 52.5200, 13.4050),
        "🇯🇵 日本-东京 (UTC+9)": (9, 35.6762, 139.6503),
        "🇰🇷 韩国-首尔 (UTC+9)": (9, 37.5665, 126.9780),
        "🇻🇳 越南-河内 (UTC+7)": (7, 21.0285, 105.8542),
        "🇹🇭 泰国-曼谷 (UTC+7)": (7, 13.7563, 100.5018),
        "🇮🇩 印尼-雅加达 (UTC+7)": (7, -6.2088, 106.8456),
        "🇵🇭 菲律宾-马尼拉 (UTC+8)": (8, 14.5995, 120.9842),
        "🇲🇾 马来西亚-吉隆坡 (UTC+8)": (8, 3.1390, 101.6869),
        "🇸🇬 新加坡 (UTC+8)": (8, 1.3521, 103.8198),
        "🇦🇺 澳大利亚-悉尼 (UTC+10)": (10, -33.8688, 151.2093)
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
    root.title("PolaFlow v29.0 God Mode")
    root.geometry("550x350")
    
    lbl = tk.Label(root, text="🌍 PolaFlow v29.0 上帝模式 (God Mode)\n[100%原生伪装 / 零0000时间戳 / Lavc擦除]", 
                   pady=20, font=("Arial", 11, "bold"))
    lbl.pack()
    
    combo = ttk.Combobox(root, values=list(tz_map.keys()), width=55, state="readonly")
    combo.set("--- 点击选择全球投放战场 ---")
    combo.pack(pady=5)
    
    btn = tk.Button(root, text="🚀 启动神级清洗", command=on_confirm, 
                    bg="#8e44ad", fg="white", width=25, height=2)
    btn.pack(pady=25)
    
    root.mainloop()
    return selected_data[0]

# ==========================================
# 3. 视觉重构链 (修复色彩空间)
# ==========================================
def get_ultimate_visual_chain():
    k1 = random.uniform(-0.015, 0.015)
    chroma = random.uniform(0.6, 1.4)
    freq = random.uniform(2, 4.5)
    noise = random.randint(2, 4)
    
    # 财经质感曲线
    financial_curves = "curves=all='0/0 0.2/0.18 0.5/0.5 0.8/0.82 1/1'"
    
    # 安全缩放 (Zoom-in 1% + 随机偏移)，代替旋转，防止黑边
    x_offset = random.randint(0, 8)
    y_offset = random.randint(0, 8)
    
    zoom_crop = (
        f"scale=1090:1938:flags=lanczos," # 先放大约 1%
        f"crop=1080:1920:{x_offset}:{y_offset}" # 再切回 1080p
    )

    # 呼吸滤镜 (eq)
    lb = f"eq=contrast='1+0.005*sin(2*PI*0.5*n/30)':eval=frame"

    return [
        f"dctdnoiz=s={freq}:n=3",
        zoom_crop, 
        f"lenscorrection=k1={k1}:k2=0.001",
        f"chromashift=cbh={chroma}:crh={-chroma}:cbv={chroma}:crv={-chroma}",
        f"vignette='PI/4+{random.uniform(0.02, 0.08)}'",
        f"noise=alls={noise}:allf=t+u",
        financial_curves,
        lb,
        "format=yuv420p",
        # [核心修复] 显式标记色彩空间为 BT.709 (模拟 iPhone SDR)
        "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" 
    ]

# ==========================================
# 4. 核心处理引擎
# ==========================================
def mutate_video(input_file, output_dir, region_data):
    offset, base_lat, base_lon = region_data 
    
    try:
        # A. 抽取设备 & 确定格式 (逻辑自洽)
        make_val, model_val, sw_val, supported_exts = random.choice(DEVICE_DATABASE)
        target_ext = supported_exts[0] # 严格使用设备支持的第一个格式
        
        # B. 生成 100% 原生防撞文件名 (无 UUID 后缀)
        unique_id_internal = str(uuid.uuid4())[:8] # 仅用于 Exif 内部序列号
        
        # 碰撞检测循环：确保 IMG_XXXX.MOV 不重复
        max_retries = 100
        filename = ""
        for _ in range(max_retries):
            if make_val == "Apple":
                # Apple: IMG_XXXX.MOV
                if random.random() < 0.85:
                    filename = f"IMG_{random.randint(1000, 9999)}{target_ext}"
                else:
                    filename = f"Video_{datetime.now().strftime('%Y%m%d')}_{random.randint(10,99)}{target_ext}"
            else:
                # Android: YYYYMMDD_HHMMSS.mp4
                dt_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{dt_str}{target_ext}"
            
            # 检查文件是否存在
            if not (output_dir / filename).exists():
                break
            # 如果存在，休眠 1ms 重试生成
            time.sleep(0.001)

        output_file = output_dir / filename

        # --- C. 音频指纹 (引入非线性变速) ---
        # 1.002 倍速微调，模拟硬件时钟漂移
        speed_jitter = random.uniform(0.998, 1.002) 
        h_gain = round(random.uniform(3, 8), 2)
        e_delay = round(random.uniform(0.025, 0.05), 4) # 25ms - 50ms (真实环境回声)
        
        ap = (
            f"anequalizer=c0 f=18000 w=2000 g={h_gain}," # 超高频底噪
            f"aecho=1.0:0.001:{e_delay}:0.15,"           # 微弱回声
            f"atempo={speed_jitter},"                    # 非线性变速 (关键!)
            f"aresample=44100"                           # 强制统一采样率
        )
        
        # --- D. 视觉滤镜 ---
        target_fps = random.choice(["29.97", "30", "59.94"]) 
        vf = ",".join(get_ultimate_visual_chain())

        # --- E. FFmpeg 编码 (物理切除 Lavf) ---
        cmd = [
            FFMPEG_EXE, '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(input_file),
            '-vf', vf, '-af', ap,
            '-r', target_fps,
            '-c:v', 'libx264',
            '-x264-params', 'no-info=1',             # 阻止 x264 写入信息
            '-bsf:v', 'filter_units=remove_types=6', # 移除 SEI
            '-crf', str(random.randint(19, 23)),
            '-preset', 'fast',
            '-bitexact',                             # 移除 Lavf 版本号
            '-map_metadata', '-1',                   # 清除原始元数据
            '-c:a', 'aac', 
            '-ar', '44100',                          # 严格锁定 44100
            '-b:a', '192k',
            str(output_file)
        ]
        
        subprocess.run(cmd, check=True)

        # -------------------------------------------------
        # F. Exif 深度伪装 (God Mode 核心：修复 0000 和 Lavc)
        # -------------------------------------------------
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        cap_dt = target_now - timedelta(minutes=random.randint(60, 1440))
        # 格式必须严格匹配 ExifTool 要求: YYYY:mm:dd HH:MM:SS
        ts = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{"+" if offset >= 0 else "-"}{abs(offset):02d}:00')

        # GPS 坐标抖动
        final_lat = base_lat + random.uniform(-0.02, 0.02)
        final_lon = base_lon + random.uniform(-0.02, 0.02)
        lat_ref = "N" if final_lat >= 0 else "S"
        lon_ref = "E" if final_lon >= 0 else "W"

        # 品牌原子伪装 (Atomic Level Mimicry)
        atom_tags = []
        if make_val == "Apple":
            # 伪装成 QuickTime 容器
            atom_tags = [
                "-MajorBrand=qt  ",   
                "-MinorVersion=0.0.0",
                "-CompatibleBrands=qt  ",
                "-CompressorName=H.264",      # 覆盖 Lavc libx264
                "-HandlerVendorID=apple",
                "-Make=Apple",
                f"-Model={model_val}",
                f"-Software={sw_val}"
            ]
        else:
            # 伪装成 Android MP4 容器
            atom_tags = [
                "-MajorBrand=mp42",
                "-MinorVersion=0.0.0",
                "-CompatibleBrands=mp42isom",
                "-CompressorName=",           # Android 通常不写这个，强制删除
                "-HandlerVendorID=",          # 删除 Handler Vendor
                f"-Make={make_val}",
                f"-Model={model_val}",
                f"-Software={sw_val}"
            ]

        exif_cmd = [
            EXIFTOOL_EXE, '-overwrite_original', '-api', 'LargeFileSupport=1',
            # 1. 基础原子标签
            *atom_tags,
            
            # 2. 时间戳全覆盖 (修复 0000 问题)
            f"-CreateDate={ts}",
            f"-ModifyDate={ts}",
            f"-TrackCreateDate={ts}",
            f"-TrackModifyDate={ts}",
            f"-MediaCreateDate={ts}",
            f"-MediaModifyDate={ts}",
            f"-DateTimeOriginal={ts}",
            f"-CreationDate={ts}", # Apple 特有
            
            # 3. 硬件信息
            f"-InternalSerialNumber={unique_id_internal}",
            f"-VideoFrameRate={target_fps}",
            f"-GPSLatitude={abs(final_lat)}",
            f"-GPSLatitudeRef={lat_ref}",
            f"-GPSLongitude={abs(final_lon)}",
            f"-GPSLongitudeRef={lon_ref}",
            
            # 4. [关键] 清除工具痕迹
            "-XMPToolkit=",     # 删除 ExifTool 签名
            "-Encoder=",        # 删除编码器标记
            "-Warning=",        # 清除警告信息
            
            str(output_file)
        ]
        
        # 执行 ExifTool
        result = subprocess.run(exif_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # 如果写入失败，抛出异常，不要静默失败
            raise Exception(f"ExifTool Error: {result.stderr}")

        # G. 二进制噪声注入 (Hash 免疫)
        # 在文件尾部追加 16-64 字节的随机数据
        with open(output_file, "ab") as f:
            f.write(os.urandom(random.randint(16, 64)))

        # H. 文件系统时间同步
        os.utime(output_file, (cap_dt.timestamp(), cap_dt.timestamp()))
        print(f"[+] 成功: {filename} | {model_val} | 采样: 44100 | Lavc: 已擦除")
        return True

    except Exception as e:
        print(f"[!] 错误 {input_file}: {e}")
        return False

# ==========================================
# 5. 主程序
# ==========================================
def main():
    freeze_support()
    print("--- PolaFlow v29.0 God Mode (Final) ---")
    
    region_data = select_timezone_visual() 
    
    if region_data is not None:
        in_p, out_p = Path("./raw"), Path("./output")
        in_p.mkdir(exist_ok=True); out_p.mkdir(exist_ok=True)
        
        raw_files = [f for f in in_p.glob("*.*") if f.suffix.lower() in ('.mp4', '.mov', '.m4v', '.webm')]
        if not raw_files:
            print("[!] raw 文件夹无视频。")
            return

        tasks = [(f, out_p, region_data) for f in raw_files]
        cpu_cores = max(1, os.cpu_count() - 1)
        
        print(f"[*] 引擎启动 | 核心: {cpu_cores} | 任务: {len(tasks)}")
        
        with Pool(cpu_cores) as pool:
            pool.starmap(mutate_video, tasks)
            
        print("\n[+] 所有任务处理完成。")
        input("按 Enter 键退出...")

if __name__ == "__main__":
    main()
