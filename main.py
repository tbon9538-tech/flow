import os
import sys
import random
import subprocess
import uuid
import platform
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

# 自动判断系统后缀
EXT = ".exe" if platform.system() == "Windows" else ""
FFMPEG_EXE = get_resource_path(f"ffmpeg{EXT}")
EXIFTOOL_EXE = get_resource_path(f"exiftool{EXT}")

# 兜底检测
if not os.path.exists(FFMPEG_EXE): FFMPEG_EXE = "ffmpeg"
if not os.path.exists(EXIFTOOL_EXE): EXIFTOOL_EXE = "exiftool"

# ==========================================
# 1. 设备数据库
# ==========================================
DEVICE_DATABASE = [
    ("Apple", "iPhone 14 Pro", "16.1.1", [".MOV", ".mp4"]),
    ("Apple", "iPhone 15 Pro", "17.0.2", [".MOV", ".mp4"]),
    ("Apple", "iPhone 15 Pro Max", "17.2.1", [".MOV", ".mp4"]),
    ("Apple", "iPhone 16 Pro", "18.0", [".MOV", ".mp4"]),
    ("Apple", "iPhone 16 Pro Max", "18.1", [".MOV", ".mp4"]),
    ("Samsung", "SM-S928B", "Android 14", [".mp4"]), # S24 Ultra
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
    root.title("PolaFlow v28.0 - Final Optimized")
    root.geometry("500x350")
    
    lbl = tk.Label(root, text="🌍 全球矩阵重构系统 v28.0 (Final)\n[特性: 完美色彩 / 原生命名 / 无黑边去重]", 
                   pady=20, font=("Arial", 10, "bold"))
    lbl.pack()
    
    combo = ttk.Combobox(root, values=list(tz_map.keys()), width=55, state="readonly")
    combo.set("--- 点击选择全球投放战场 ---")
    combo.pack(pady=5)
    
    btn = tk.Button(root, text="🚀 启动完美生成", command=on_confirm, 
                    bg="#2ecc71", fg="white", width=25, height=2)
    btn.pack(pady=25)
    
    root.mainloop()
    return selected_data[0]

# ==========================================
# 3. 滤镜链 (Fix 3: 使用安全的缩放裁剪替代旋转)
# ==========================================
def get_ultimate_visual_chain():
    k1 = random.uniform(-0.015, 0.015)
    chroma = random.uniform(0.6, 1.4)
    freq = random.uniform(2, 4.5)
    noise = random.randint(2, 4)
    
    # 调色曲线
    financial_curves = "curves=all='0/0 0.2/0.18 0.5/0.5 0.8/0.82 1/1'"
    
    # 核心修改：使用 Zoom-in (1.01x) 然后随机 Crop，代替 Rotate
    # 这能保证画面哈希改变，但绝对不会出现黑边
    
    # 随机偏移量 (在 10px 范围内浮动)
    x_offset = random.randint(0, 8)
    y_offset = random.randint(0, 8)
    
    zoom_crop = (
        f"scale=1090:1938:flags=lanczos," # 先放大约 1%
        f"crop=1080:1920:{x_offset}:{y_offset}" # 再切回 1080p
    )

    return [
        f"dctdnoiz=s={freq}:n=3",
        zoom_crop, # 替代了 rotate
        f"lenscorrection=k1={k1}:k2=0.001",
        f"chromashift=cbh={chroma}:crh={-chroma}:cbv={chroma}:crv={-chroma}",
        f"vignette='PI/4+{random.uniform(0.02, 0.08)}'",
        f"noise=alls={noise}:allf=t+u",
        financial_curves,
        "format=yuv420p" # 确保颜色空间正确
    ]

# ==========================================
# 4. 核心处理引擎
# ==========================================
def mutate_video(input_file, output_dir, region_data):
    offset, base_lat, base_lon = region_data 
    
    try:
        # A. 抽取设备
        make_val, model_val, sw_val, _ = random.choice(DEVICE_DATABASE)
        
        # B. 场景决策 (Fix 2: 修正文件名逻辑，去除 UUID)
        # unique_id 仅用于 Exif 的内部序列号，不用于文件名
        unique_id = str(uuid.uuid4())[:8] 
        process_type = ""
        
        if make_val == "Apple":
            # Apple 命名规范: IMG_XXXX.MOV
            if random.random() < 0.8:
                target_ext = ".MOV"
                # 原生文件名不带 UUID
                filename = f"IMG_{random.randint(1000, 9999)}{target_ext}"
                process_type = "Native Camera"
            else:
                target_ext = ".mp4"
                # 导出视频通常是 "Video.mp4" 或日期
                filename = f"Video_{datetime.now().strftime('%Y%m%d')}_{random.randint(10,99)}{target_ext}"
                process_type = "Editor Export"
        else:
            # Android 命名规范: 20260213_160000.mp4
            target_ext = ".mp4" 
            date_str = datetime.now().strftime('%Y%m%d')
            time_str = datetime.now().strftime('%H%M%S')
            
            if random.random() < 0.8:
                filename = f"{date_str}_{time_str}{target_ext}"
                process_type = "Native Camera"
            else:
                filename = f"Edit_{date_str}{target_ext}"
                process_type = "Editor Export"

        output_file = output_dir / filename

        # V3 终极音频链 (请确保这段代码在 try 缩进内)
        # ==========================================
        pitch_factor = random.uniform(0.98, 1.02)
        h_gain = round(random.uniform(3, 5), 2)
        e_delay = round(random.uniform(25, 45), 4)
        e_decay = round(random.uniform(0.1, 0.15), 2)

        ap = (
            f"anequalizer=c0 f=18000 w=2000 g={h_gain},"
            f"aecho=1.0:0.3:{e_delay}:{e_decay},"
            f"asetrate=44100*{pitch_factor:.5f},"
            f"atempo={1/pitch_factor:.5f},"
            f"aresample=44100,"
            f"dynaudnorm=f=150:g=15:p=0.9:m=10.0"
        )
        
        # --- 帧率 ---
        target_fps = random.choice(["23.976", "29.97", "59.94"]) 
        
        # --- 视觉滤镜 ---
        vf = ",".join(get_ultimate_visual_chain())

        # D. FFmpeg 编码 (Fix 1: 移除 Color Flags，保持默认 SDR)
        cmd = [
            FFMPEG_EXE, '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(input_file),
            '-vf', vf, '-af', ap,
            '-r', target_fps,
            '-c:v', 'libx264',
            '-x264-params', 'no-info=1',
            '-bsf:v', 'filter_units=remove_types=6', # 核心: 移除 SEI
            '-crf', str(random.randint(19, 23)),
            '-preset', 'fast',
            '-bitexact',
            '-map_metadata', '-1',
            '-c:a', 'aac', 
            '-ar', random.choice(['44100', '48000']),
            '-b:a', f'{random.randint(128, 192)}k',
            str(output_file)
        ]
        
        subprocess.run(cmd, check=True)

        # -------------------------------------------------
        # E. Exif & GPS 注入 (深度品牌伪装)
        # -------------------------------------------------
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        cap_dt = target_now - timedelta(minutes=random.randint(60, 1440))
        ts = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{"+" if offset >= 0 else "-"}{abs(offset):02d}:00')

        # GPS 坐标
        lat_jitter = random.uniform(-0.02, 0.02)
        lon_jitter = random.uniform(-0.02, 0.02)
        final_lat = base_lat + lat_jitter
        final_lon = base_lon + lon_jitter
        lat_ref = "N" if final_lat >= 0 else "S"
        lon_ref = "E" if final_lon >= 0 else "W"

        # 品牌伪装标签
        anti_forensics_tags = []
        if make_val == "Apple":
            anti_forensics_tags = [
                "-MajorBrand=qt  ",   
                "-MinorVersion=0.0.0",
                "-CompatibleBrands=qt  ",
                "-CompressorName=H.264", 
                "-VendorID=apple",       
                "-Encoder=",             
                "-HandlerVendorID=apple",
                "-HandlerDescription=Core Media Video"
            ]
        else:
            anti_forensics_tags = [
                "-MajorBrand=mp42",
                "-MinorVersion=0.0.0",
                "-CompatibleBrands=mp42isom",
                "-CompressorName=",      
                "-VendorID=",            
                "-Encoder=",
                "-HandlerVendorID=",
                "-HandlerDescription=VideoHandle"
            ]

        exif_base_cmd = [
            EXIFTOOL_EXE, '-overwrite_original', '-api', 'LargeFileSupport=1',
            f"-Make={make_val}",
            f"-Model={model_val}",
            f"-Software={sw_val}",
            f"-CreateDate={ts}",
            f"-ModifyDate={ts}",
            f"-DateTimeOriginal={ts}",
            f"-InternalSerialNumber={unique_id}", # 序列号藏在内部
            f"-VideoFrameRate={target_fps}",
            f"-GPSLatitude={abs(final_lat)}",
            f"-GPSLatitudeRef={lat_ref}",
            f"-GPSLongitude={abs(final_lon)}",
            f"-GPSLongitudeRef={lon_ref}",
        ]
        
        # 执行写入
        full_exif_cmd = exif_base_cmd + anti_forensics_tags + [str(output_file)]
        
        result = subprocess.run(full_exif_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[!] Warning: Exif write simplified due to error: {result.stderr}")
            subprocess.run(exif_base_cmd + [str(output_file)])

        # F. 文件时间同步
        os.utime(output_file, (cap_dt.timestamp(), cap_dt.timestamp()))
        print(f"[+] 成功: {filename} [{process_type}] | {model_val} | 去黑边: ✅")
        return True

    except Exception as e:
        print(f"[!] 错误 {input_file}: {e}")
        return False

# ==========================================
# 5. 主程序
# ==========================================
def main():
    freeze_support()
    print("--- PolaFlow Anti-Forensic Engine v28.0 (Final) ---")
    
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


