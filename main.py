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
# 0. 基础环境配置
# ==========================================
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

EXT = ".exe" if platform.system() == "Windows" else ""
FFMPEG_EXE = get_resource_path(f"ffmpeg{EXT}")
EXIFTOOL_EXE = get_resource_path(f"exiftool{EXT}")

# 兜底检测
if not os.path.exists(FFMPEG_EXE): FFMPEG_EXE = "ffmpeg"
if not os.path.exists(EXIFTOOL_EXE): EXIFTOOL_EXE = "exiftool"

# ==========================================
# 1. 设备数据库 (逻辑自洽)
# ==========================================
DEVICE_DATABASE = [
    ("Apple", "iPhone 14 Pro", "16.1.1", [".MOV"]),
    ("Apple", "iPhone 15 Pro", "17.0.2", [".MOV"]),
    ("Apple", "iPhone 16 Pro", "18.0", [".MOV"]),
    ("Samsung", "SM-S928B", "Android 14", [".mp4"]),
    ("Google", "Pixel 8 Pro", "Android 14", [".mp4"])
]

# ==========================================
# 2. 全球战场选择器
# ==========================================
def select_timezone_visual():
    tz_map = {
        "🇺🇸 美国-洛杉矶 (US West)": (-8, 34.0522, -118.2437),
        "🇺🇸 美国-纽约 (US East)": (-5, 40.7128, -74.0060),
        "🇺🇸 美国-芝加哥 (US Central)": (-6, 41.8781, -87.6298),
        "🇨🇦 加拿大-多伦多": (-5, 43.6532, -79.3832),
        "🇬🇧 英国-伦敦 (UK)": (0, 51.5074, -0.1278),
        "🇩🇪 德国-柏林 (Germany)": (1, 52.5200, 13.4050),
        "🇫🇷 法国-巴黎 (France)": (1, 48.8566, 2.3522),
        "🇪🇸 西班牙-马德里": (1, 40.4168, -3.7038),
        "🇮🇹 意大利-罗马": (1, 41.9028, 12.4964),
        "🇯🇵 日本-东京 (Japan)": (9, 35.6762, 139.6503),
        "🇰🇷 韩国-首尔 (Korea)": (9, 37.5665, 126.9780),
        "🇹🇼 中国-台湾 (Taiwan)": (8, 25.0330, 121.5654),
        "🇭🇰 中国-香港 (HongKong)": (8, 22.3193, 114.1694),
        "🇻🇳 越南-河内": (7, 21.0285, 105.8542),
        "🇹🇭 泰国-曼谷": (7, 13.7563, 100.5018),
        "🇮🇩 印尼-雅加达": (7, -6.2088, 106.8456),
        "🇵🇭 菲律宾-马尼拉": (8, 14.5995, 120.9842),
        "🇲🇾 马来西亚-吉隆坡": (8, 3.1390, 101.6869),
        "🇸🇬 新加坡": (8, 1.3521, 103.8198),
        "🇦🇺 澳大利亚-悉尼": (10, -33.8688, 151.2093)
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
    root.title("PolaFlow v30.0 - Native Fix")
    root.geometry("500x300")
    
    lbl = tk.Label(root, text="🌍 PolaFlow v30.0 终极原生版\n[修复报错 / 原生听感 / BT.709色彩]", 
                   pady=20, font=("Arial", 10, "bold"))
    lbl.pack()
    
    combo = ttk.Combobox(root, values=list(tz_map.keys()), width=55, state="readonly")
    combo.set("--- 点击选择全球投放战场 ---")
    combo.pack(pady=5)
    
    btn = tk.Button(root, text="🚀 启动", command=on_confirm, 
                    bg="#27ae60", fg="white", width=25, height=2)
    btn.pack(pady=25)
    
    root.mainloop()
    return selected_data[0]

# ==========================================
# 3. 视觉滤镜链 (修复报错的关键)
# ==========================================
def get_ultimate_visual_chain():
    k1 = random.uniform(-0.01, 0.01)
    chroma = random.uniform(0.6, 1.2)
    freq = random.uniform(2, 4)
    noise = random.randint(2, 3) # 降低噪点以更像原片
    
    # 1. 缩放+裁剪 (代替旋转，杜绝黑边)
    x_off = random.randint(0, 4)
    y_off = random.randint(0, 4)
    zoom_crop = f"scale=1084:1924:flags=lanczos,crop=1080:1920:{x_off}:{y_off}"
    
    # 2. [关键修复] 使用 eq 代替 geq
    # 这是一个极其安全的呼吸滤镜，让对比度随时间微弱波动
    # 彻底解决了 "Unknown function" 报错
    breathing = "eq=contrast='1+0.003*sin(n/24)'"

    return [
        f"dctdnoiz=s={freq}:n=3",
        zoom_crop,
        f"lenscorrection=k1={k1}:k2=0.001",
        f"chromashift=cbh={chroma}:crh={-chroma}:cbv={chroma}:crv={-chroma}",
        f"vignette='PI/4+{random.uniform(0.02, 0.05)}'", # 减弱暗角
        f"noise=alls={noise}:allf=t+u",
        breathing, # 替换了原来的 geq
        "format=yuv420p",
        # [新增] 强制写入原生色彩标记
        "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709"
    ]

# ==========================================
# 4. 核心处理引擎
# ==========================================
def mutate_video(input_file, output_dir, region_data):
    offset, base_lat, base_lon = region_data
    
    try:
        # A. 抽取设备
        make_val, model_val, sw_val, supported_exts = random.choice(DEVICE_DATABASE)
        target_ext = supported_exts[0]
        
        # B. 原生文件名生成 (防撞)
        unique_id = str(uuid.uuid4())[:8] # 仅内部使用
        max_retries = 50
        filename = ""
        
        for _ in range(max_retries):
            if make_val == "Apple":
                if random.random() < 0.9: # 提高原生比例
                    filename = f"IMG_{random.randint(1000, 9999)}{target_ext}"
                else:
                    filename = f"Video_{datetime.now().strftime('%Y%m%d')}_{random.randint(10,99)}{target_ext}"
            else:
                dt_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{dt_str}{target_ext}"
            
            if not (output_dir / filename).exists():
                break
            time.sleep(0.001)

        output_file = output_dir / filename

        # --- C. 音频指纹 (修复听感) ---
        # 移除了大延迟的 aecho，改用微秒级处理 + 动态变速
        pitch = random.uniform(0.99, 1.01)
        h_gain = round(random.uniform(3, 6), 2)
        
        ap = (
            f"anequalizer=c0 f=18000 w=2000 g={h_gain}," # 超高频特征
            f"asetrate=44100*{pitch},"                   # 变调
            f"atempo={1/pitch},"                         # 变速回原长
            f"aresample=44100"                           # 锁定采样率
        )

        # --- D. FFmpeg 编码 ---
        target_fps = random.choice(["29.97", "30", "59.94"])
        vf = ",".join(get_ultimate_visual_chain())

        cmd = [
            FFMPEG_EXE, '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(input_file),
            '-vf', vf, '-af', ap,
            '-r', target_fps,
            '-c:v', 'libx264',
            '-x264-params', 'no-info=1',
            '-bsf:v', 'filter_units=remove_types=6',
            '-crf', str(random.randint(19, 22)),
            '-preset', 'fast',
            '-bitexact', # 擦除 Lavf
            '-map_metadata', '-1',
            '-c:a', 'aac', '-ar', '44100', '-b:a', '192k',
            str(output_file)
        ]

        subprocess.run(cmd, check=True)

        # --- E. Exif 深度伪装 ---
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        cap_dt = target_now - timedelta(minutes=random.randint(60, 1440))
        ts = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{"+" if offset >= 0 else "-"}{abs(offset):02d}:00')

        # GPS 计算
        final_lat = base_lat + random.uniform(-0.01, 0.01)
        final_lon = base_lon + random.uniform(-0.01, 0.01)
        lat_ref = "N" if final_lat >= 0 else "S"
        lon_ref = "E" if final_lon >= 0 else "W"

        # 品牌特征伪装
        atom_tags = []
        if make_val == "Apple":
            atom_tags = [
                "-MajorBrand=qt  ", "-MinorVersion=0.0.0", "-CompatibleBrands=qt  ",
                "-CompressorName=H.264", # 覆盖 Lavc
                "-HandlerVendorID=apple", "-Make=Apple", f"-Model={model_val}", f"-Software={sw_val}"
            ]
        else:
            atom_tags = [
                "-MajorBrand=mp42", "-MinorVersion=0.0.0", "-CompatibleBrands=mp42isom",
                "-CompressorName=", "-HandlerVendorID=", # 安卓清空
                f"-Make={make_val}", f"-Model={model_val}", f"-Software={sw_val}"
            ]

        exif_cmd = [
            EXIFTOOL_EXE, '-overwrite_original', '-api', 'LargeFileSupport=1',
            *atom_tags,
            f"-CreateDate={ts}", f"-ModifyDate={ts}", f"-DateTimeOriginal={ts}",
            f"-TrackCreateDate={ts}", f"-MediaCreateDate={ts}", # 填满所有时间戳
            f"-InternalSerialNumber={unique_id}",
            f"-VideoFrameRate={target_fps}",
            f"-GPSLatitude={abs(final_lat)}", f"-GPSLatitudeRef={lat_ref}",
            f"-GPSLongitude={abs(final_lon)}", f"-GPSLongitudeRef={lon_ref}",
            "-XMPToolkit=", "-Encoder=", "-Warning=", # 清除痕迹
            str(output_file)
        ]

        result = subprocess.run(exif_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[!] Exif 写入警告: {result.stderr}")

        # F. 二进制噪声注入 (Hash 免疫)
        with open(output_file, "ab") as f:
            f.write(os.urandom(random.randint(16, 64)))

        # G. 时间同步
        os.utime(output_file, (cap_dt.timestamp(), cap_dt.timestamp()))
        print(f"[+] 成功: {filename} | {model_val} | 原生伪装: 100%")
        return True

    except Exception as e:
        print(f"[!] 错误 {input_file}: {e}")
        return False

# ==========================================
# 5. 主程序
# ==========================================
def main():
    freeze_support()
    print("--- PolaFlow v30.0 Native Fix ---")
    
    region_data = select_timezone_visual()
    if region_data:
        in_p, out_p = Path("./raw"), Path("./output")
        in_p.mkdir(exist_ok=True); out_p.mkdir(exist_ok=True)
        
        raw_files = [f for f in in_p.glob("*.*") if f.suffix.lower() in ('.mp4', '.mov')]
        if not raw_files:
            print("[!] raw 文件夹无视频。")
            return

        tasks = [(f, out_p, region_data) for f in raw_files]
        cpu_cores = max(1, os.cpu_count() - 1)
        
        with Pool(cpu_cores) as pool:
            pool.starmap(mutate_video, tasks)
            
        print("\n[+] 所有任务处理完成。")
        input("按 Enter 键退出...")

if __name__ == "__main__":
    main()

