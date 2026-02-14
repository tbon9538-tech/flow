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
# 0. 基础环境配置 (The Origin Boot)
# ==========================================
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

EXT = ".exe" if platform.system() == "Windows" else ""
FFMPEG_EXE = get_resource_path(f"ffmpeg{EXT}")
EXIFTOOL_EXE = get_resource_path(f"exiftool{EXT}")

if not os.path.exists(FFMPEG_EXE): FFMPEG_EXE = "ffmpeg"
if not os.path.exists(EXIFTOOL_EXE): EXIFTOOL_EXE = "exiftool"

# ==========================================
# 1. 设备数据库 (iOS 26.3 Origin-Ready)
# ==========================================
DEVICE_DATABASE = [
    # ----------------------------------------
    # [Apple] 2026 年度机皇 (最新 iOS 26.3)
    # ----------------------------------------
    # 特性: 2026年2月11日刚发布的最新系统，权重极高
    ("Apple", "iPhone 17 Pro Max", "26.3", [".MOV", ".mp4"]),
    ("Apple", "iPhone 17 Pro", "26.3", [".MOV", ".mp4"]),
    ("Apple", "iPhone 17 Pro Max", "19.3.1", [".MOV", ".mp4"]),
    ("Apple", "iPhone 17 Pro", "19.3", [".MOV", ".mp4"]),

    # ----------------------------------------
    # [Apple] 次旗舰主力 (存量高端用户)
    # ----------------------------------------
    # iPhone 16 Pro 系列 (依然是主力，用户基数大且优质)
    ("Apple", "iPhone 16 Pro Max", "26.2.1", [".MOV", ".mp4"]),
    ("Apple", "iPhone 16 Pro", "26.1", [".MOV", ".mp4"]),
    # iPhone 15 Pro Max (经典的钉子户旗舰，系统升级到最新)
    ("Apple", "iPhone 15 Pro Max", "26.0", [".MOV", ".mp4"]),
    ("Apple", "iPhone 16 Pro Max", "19.2.1", [".MOV", ".mp4"]),
    ("Apple", "iPhone 16 Pro", "19.0", [".MOV", ".mp4"]),  # 很多人停留在初始大版本
    # iPhone 15 Pro Max (钉子户)
    ("Apple", "iPhone 15 Pro Max", "18.5", [".MOV", ".mp4"]),

    # ----------------------------------------
    # [Samsung] 安卓阵营天花板 (Android 16)
    # ----------------------------------------
    # S25 Ultra (2025/2026 跨年机皇)
    ("Samsung", "SM-S938B", "Android 16", [".mp4"]),  # Galaxy S25 Ultra
    # Z Fold 7 (2026 最新折叠屏，极客/富人标签)
    ("Samsung", "SM-F966B", "Android 16", [".mp4"]),  # Galaxy Z Fold 7
    # S24 Ultra (老款机皇，保留少量用于混淆)
    ("Samsung", "SM-S928B", "Android 16", [".mp4"]),  # Galaxy S24 Ultra

    # ----------------------------------------
    # [Google] 影像旗舰 (Pixel 10 系列)
    # ----------------------------------------
    # 专攻画质权重的账号
    ("Google", "Pixel 10 Pro XL", "Android 16", [".mp4"]),  # 谷歌最新超大杯
    ("Google", "Pixel 10 Pro", "Android 16", [".mp4"]),
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
            messagebox.showwarning("Warning", "Please select region")
    root = tk.Tk()
    root.title("PolaFlow v43.0 - The Origin")
    root.geometry("550x380")
    root.configure(bg="#000000")
    lbl = tk.Label(root, text="👁️ PolaFlow v43.0 [The Origin]\n[Moov-at-End / ISO-8601-TZ / Zero Anomaly]",
                   pady=20, font=("Consolas", 11, "bold"), bg="#000000", fg="#00ff00")
    lbl.pack()
    combo = ttk.Combobox(root, values=list(tz_map.keys()), width=55, state="readonly")
    combo.set("--- SELECT TARGET REGION ---")
    combo.pack(pady=10)
    btn = tk.Button(root, text="INITIALIZE ORIGIN SEQUENCE", command=on_confirm,
                    bg="#c0392b", fg="white", font=("Arial", 10, "bold"), width=30, height=2)
    btn.pack(pady=30)
    root.mainloop()
    return selected_data[0]

# ==========================================
# 3. 滤镜链 (V43 极致光电模拟)
# ==========================================
def get_ultimate_visual_chain():
    # 模拟传感器微弱的量子效率波动
    contrast = round(random.uniform(0.9998, 1.0002), 5) 
    saturation = round(random.uniform(0.9995, 1.0005), 5)
    noise_filter = "noise=c0s=3:c1s=1:allf=t" 
    x_offset = random.randint(0, 4); y_offset = random.randint(0, 4)
    # 模拟透镜呼吸效应
    zoom_crop = f"scale=1082:1924:flags=lanczos,crop=1080:1920:{x_offset}:{y_offset}" 
    return [f"eq=contrast={contrast}:saturation={saturation}", noise_filter, zoom_crop, "scale=out_color_matrix=bt709:out_range=tv", "format=yuv420p"]

# ==========================================
# 4. 核心引擎 (Origin Core)
# ==========================================
def mutate_video(input_file, output_dir, region_data):
    offset, base_lat, base_lon = region_data
    try:
        make_val, model_val, sw_val, _ = random.choice(DEVICE_DATABASE)
        is_apple = (make_val == "Apple")
        filename = f"IMG_{random.randint(1000, 9999)}.MOV" if is_apple else f"VID_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_file = output_dir / filename
        
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        cap_dt = target_now - timedelta(minutes=random.randint(10, 5200))
        
        # [V43] 核心对齐：带时区的 ISO 8601 创建时间 (iOS 26.3 规范)
        tz_sign = "+" if offset >= 0 else "-"
        creation_time_iso = cap_dt.strftime(f'%Y-%m-%dT%H:%M:%S{tz_sign}{abs(offset):02d}00')
        creation_time_ffmpeg = cap_dt.strftime('%Y-%m-%dT%H:%M:%S.000000Z')

        tmcd_start = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}:00"
        speed_jitter = random.uniform(0.9998, 1.0002) 
        ap = f"asetrate=48000*{speed_jitter:.5f},aresample=48000,lowpass=f=19000,volume={random.uniform(0.99, 1.01):.2f}"

        target_fps_str = random.choice(["29.97", "30", "60"])
        vf_chain = ",".join(get_ultimate_visual_chain())
        audio_bitrate = f'{random.randint(160, 192)}k' if is_apple else f'{random.randint(128, 160)}k'
        
        # 硬件级对齐参数
        x264_params = (
            "no-info=1:fullrange=off:rc-lookahead=2:mbtree=0:aq-mode=1:"
            "trellis=0:ref=1:chroma-qp-offset=0:vbv-maxrate=30000:vbv-bufsize=60000:"
            "partitions=all:me=dia:subme=1"
        )

        cmd = [
            FFMPEG_EXE, '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(input_file),
            '-vf', vf_chain, '-af', ap,
            '-r', target_fps_str,
            '-bf', '0', '-g', str(int(float(target_fps_str))),
            '-ac', '2', '-c:v', 'libx264',
            '-profile:v', 'high', '-level', '4.2',
            '-x264-params', x264_params,
            '-crf', str(random.randint(22, 25)), '-preset', 'ultrafast',
            '-pix_fmt', 'yuv420p', '-color_primaries', '1', '-color_trc', '1', '-colorspace', '1', '-color_range', 'tv',
            
            # [V43] 关键：移除 faststart，确保 moov 原子在文件尾部
            '-timecode', tmcd_start, 
            '-metadata', f'creation_time={creation_time_ffmpeg}',
            '-metadata:g', f'com.apple.quicktime.make={make_val}',
            '-metadata:g', f'com.apple.quicktime.model={model_val}',
            '-metadata:g', f'com.apple.quicktime.software=iOS {sw_val}',
            '-metadata:g', f'com.apple.quicktime.creationdate={creation_time_iso}', # 注入带时区的 Apple 专属命名空间
            '-metadata:s:v:0', f'handler_name=Core Media Video',
            '-metadata:s:a:0', f'handler_name=Core Media Audio',
            
            '-avoid_negative_ts', 'make_zero', '-write_id3v2', '0',
            '-movflags', '+use_metadata_tags+write_colr', # 已移除 faststart
            '-map_metadata', '-1', '-f', 'mov' if is_apple else 'mp4',
            '-brand', 'qt  ' if is_apple else 'mp42',
            '-c:a', 'aac', '-profile:a', 'aac_low', '-aac_tns', '1', '-ar', '48000', '-b:a', audio_bitrate, '-aac_coder', 'twoloop',
            str(output_file)
        ]

        subprocess.run(cmd, check=True)

        # Exif 终极物理对齐
        ts_exif = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{tz_sign}{abs(offset):02d}:00')
        exif_cmd = [
            EXIFTOOL_EXE, '-overwrite_original', '-api', 'LargeFileSupport=1',
            f"-Make={make_val}", f"-Model={model_val}", f"-Software=iOS {sw_val}",
            f"-CreateDate={ts_exif}", f"-ModifyDate={ts_exif}", f"-DateTimeOriginal={ts_exif}",
            f"-GPSLatitude={abs(base_lat + random.uniform(-0.0002, 0.0002))}", f"-GPSLatitudeRef={'N' if base_lat >= 0 else 'S'}",
            f"-GPSLongitude={abs(base_lon + random.uniform(-0.0002, 0.0002))}", f"-GPSLongitudeRef={'E' if base_lon >= 0 else 'W'}",
            str(output_file)
        ]
        subprocess.run(exif_cmd, capture_output=True)
        os.utime(output_file, (cap_dt.timestamp(), cap_dt.timestamp())) 
        print(f"[+] 零点起源达成: {filename} | Moov-at-End: ✅ | iOS-TZ: ✅")
        return True
    except Exception as e:
        print(f"[!] Protocol Failure: {e}"); return False

def main():
    freeze_support()
    print("--- PolaFlow v43.0 [The Origin] ---")
    region = select_timezone_visual()
    if region:
        in_p, out_p = Path("./raw"), Path("./output")
        in_p.mkdir(exist_ok=True); out_p.mkdir(exist_ok=True)
        tasks = [(f, out_p, region) for f in in_p.glob("*.*") if f.suffix.lower() in ('.mp4', '.mov')]
        with Pool(max(1, int(os.cpu_count() / 2))) as pool:
            pool.starmap(mutate_video, tasks)
        messagebox.showinfo("COMPLETE", "Global Origin Protocol Executed Successfully.")

if __name__ == "__main__":
    main()
