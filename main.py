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
# 0. 基础环境配置 (System Boot)
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
if not os.path.exists(FFMPEG_EXE): 
    # 如果找不到内置的，尝试调用系统环境变量中的
    FFMPEG_EXE = "ffmpeg"
if not os.path.exists(EXIFTOOL_EXE): 
    EXIFTOOL_EXE = "exiftool"

# ==========================================
# 1. 设备数据库 (2026 顶奢旗舰版 - High End Only)
# ==========================================
DEVICE_DATABASE = [
    # [Apple] 2026 年度机皇
    ("Apple", "iPhone 17 Pro Max", "26.3", [".MOV"]),
    ("Apple", "iPhone 17 Pro", "26.3", [".MOV"]),
    ("Apple", "iPhone 16 Pro Max", "19.3.1", [".MOV"]),
    # [Samsung] 安卓阵营
    ("Samsung", "SM-S938B", "Android 16", [".mp4"]),  # S25 Ultra
    ("Samsung", "SM-F966B", "Android 16", [".mp4"]),  # Z Fold 7
    # [Google] Pixel
    ("Google", "Pixel 10 Pro XL", "Android 16", [".mp4"]),
]

# ==========================================
# 2. 全球战场选择器 (GUI Module)
# ==========================================
def select_timezone_visual():
    tz_map = {
        "🇺🇸 美国-洛杉矶 (US West)": (-8, 34.0522, -118.2437),
        "🇺🇸 美国-纽约 (US East)": (-5, 40.7128, -74.0060),
        "🇬🇧 英国-伦敦 (UK)": (0, 51.5074, -0.1278),
        "🇩🇪 德国-柏林 (Germany)": (1, 52.5200, 13.4050),
        "🇫🇷 法国-巴黎 (France)": (1, 48.8566, 2.3522),
        "🇯🇵 日本-东京 (Japan)": (9, 35.6762, 139.6503),
        "🇰🇷 韩国-首尔 (Korea)": (9, 37.5665, 126.9780),
        "🇹🇼 中国-台湾 (Taiwan)": (8, 25.0330, 121.5654),
        "🇭🇰 中国-香港 (HongKong)": (8, 22.3193, 114.1694),
        "🇻🇳 越南-河内": (7, 21.0285, 105.8542),
        "🇹🇭 泰国-曼谷": (7, 13.7563, 100.5018),
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
    root.title("PolaFlow v29.0 - Heisenberg Edition")
    root.geometry("550x380")
    
    # 黑色极客风格主题
    root.configure(bg="#1e1e1e")
    
    lbl = tk.Label(root, text="👁️ PolaFlow v29.0 [Zero-Trust Audit]\n[Anti-Fingerprint / Color-Space / Sensor-Noise]",
                   pady=20, font=("Consolas", 11, "bold"), bg="#1e1e1e", fg="#00ff00")
    lbl.pack()

    combo = ttk.Combobox(root, values=list(tz_map.keys()), width=55, state="readonly")
    combo.set("--- Select Target Region ---")
    combo.pack(pady=10)

    btn = tk.Button(root, text="EXECUTE PROTOCOL", command=on_confirm,
                    bg="#c0392b", fg="white", font=("Arial", 10, "bold"), width=30, height=2)
    btn.pack(pady=30)
    
    footer = tk.Label(root, text="Warning: Authorized Personnel Only", bg="#1e1e1e", fg="#7f8c8d")
    footer.pack(side="bottom", pady=10)

    root.mainloop()
    return selected_data[0]

# ==========================================
# 3. 滤镜链 (Visual Entropy)
# ==========================================
def get_ultimate_visual_chain():
    """
    结合了 '无黑边Zoom' 和 '传感器噪点' 的终极视觉链
    """
    # 1. 基础画质微调
    contrast = round(random.uniform(0.98, 1.02), 3)
    saturation = round(random.uniform(0.95, 1.05), 3)
    
    # 2. 模拟 CMOS 传感器热噪 (对抗 AI 查重最有效手段)
    # 强度极低，人眼不可见，但机器 Hash 会完全改变
    noise_filter = f"noise=alls=1:allf=t+u"

    # 3. 几何拓扑重构 (Zoom + Random Crop) - 替代 Rotate，彻底杜绝黑边
    # 逻辑: 放大到 101% (1090x1938)，然后在中心附近随机裁剪回 1080x1920
    x_offset = random.randint(0, 10)
    y_offset = random.randint(0, 18)
    zoom_crop = (
        f"scale=1090:1938:flags=lanczos,"  
        f"crop=1080:1920:{x_offset}:{y_offset}" 
    )

    chain = [
        f"eq=contrast={contrast}:saturation={saturation}",
        noise_filter,
        zoom_crop,
        # 强制色彩空间转换 (防止色域溢出)
        "scale=out_color_matrix=bt709:out_range=tv",
        "format=yuv420p" 
    ]
    return chain

# ==========================================
# 4. 核心处理引擎 (The Heisenberg Core)
# ==========================================
def mutate_video(input_file, output_dir, region_data):
    offset, base_lat, base_lon = region_data

    try:
        # A. 抽取设备
        make_val, model_val, sw_val, _ = random.choice(DEVICE_DATABASE)
        is_apple = (make_val == "Apple")

        # B. 命名拓扑学 (无需 UUID)
        process_type = ""
        unique_serial = str(uuid.uuid4())[:8] # 仅用于内部元数据

        if is_apple:
            # iOS 原生命名
            if random.random() < 0.85:
                target_ext = ".MOV"
                filename = f"IMG_{random.randint(1000, 9999)}{target_ext}"
                process_type = "Native Camera"
            else:
                target_ext = ".mp4"
                filename = f"Video_{datetime.now().strftime('%Y%m%d')}_{random.randint(10, 99)}{target_ext}"
                process_type = "Editor Export"
        else:
            # Android 原生命名
            target_ext = ".mp4"
            date_str = datetime.now().strftime('%Y%m%d')
            time_str = datetime.now().strftime('%H%M%S')
            filename = f"{date_str}_{time_str}{target_ext}"
            process_type = "Native Camera"

        output_file = output_dir / filename

        # ==========================================
        # C. 听觉熵增 (Audio Entropy) - [修复点]
        # ==========================================
        # 严禁使用 aecho！改为麦克风频响模拟。
        
        # 1. 极微量的变速 (Hash Breaking)，人耳听不出
        pitch_factor = random.uniform(0.995, 1.005)
        
        # 2. 模拟不同手机麦克风的 EQ 曲线
        # Apple 麦克风通常高频较好，Samsung 中频较厚
        low_cut = random.randint(60, 100)
        high_cut = random.randint(16000, 19000)
        
        ap = (
            f"highpass=f={low_cut},lowpass=f={high_cut}," # 频响限制
            f"atempo={pitch_factor:.5f}," # 时域漂移
            f"aresample=44100," # 统一采样
            f"dynaudnorm=f=150:g=15:p=0.9:m=10.0" # 模拟 AGC (自动增益)
        )

        # --- 帧率 & 视觉 ---
        target_fps = random.choice(["23.976", "29.97", "30", "59.94", "60"])
        vf_chain = ",".join(get_ultimate_visual_chain())

        # ==========================================
        # D. FFmpeg 编码 (The Matrix Build)
        # ==========================================
        cmd = [
            FFMPEG_EXE, '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(input_file),
            '-vf', vf_chain, 
            '-af', ap,
            '-r', target_fps,
            '-c:v', 'libx264',
            
            # [关键] 模拟硬件编码器特征
            # nal-hrd=cbr 模拟 CBR 模式，no-info 去除 FFmpeg 标识
            '-x264-params', 'no-info=1:nal-hrd=cbr', 
            '-bsf:v', 'filter_units=remove_types=6', # 移除 SEI 用户数据
            
            '-crf', str(random.randint(21, 24)),
            '-preset', 'veryfast', # 手机编码通常很快
            '-tune', 'film',
            
            # [关键] 注入色彩空间 (欺骗 TikTok 认为是原生相机)
            '-color_primaries', '1', '-color_trc', '1', '-colorspace', '1',
            
            '-map_metadata', '-1', # 清除旧元数据
            
            '-c:a', 'aac',
            '-ar', '44100',
            '-b:a', '128k',
            str(output_file)
        ]

        subprocess.run(cmd, check=True)

        # -------------------------------------------------
        # E. Exif & GPS 注入 (深度品牌伪装)
        # -------------------------------------------------
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        cap_dt = target_now - timedelta(minutes=random.randint(60, 1440))
        
        # Exif 格式时间
        tz_sign = "+" if offset >= 0 else "-"
        ts_exif = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{tz_sign}{abs(offset):02d}:00')
        ts_qt = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S')

        # GPS 坐标
        final_lat = base_lat + random.uniform(-0.01, 0.01)
        final_lon = base_lon + random.uniform(-0.01, 0.01)
        lat_ref = "N" if final_lat >= 0 else "S"
        lon_ref = "E" if final_lon >= 0 else "W"

        # [关键] 品牌伪装标签分流
        brand_tags = []
        if is_apple:
            brand_tags = [
                f"-Make=Apple", f"-Model={model_val}", f"-Software={sw_val}",
                f"-CreationDate={ts_exif}", # iOS 特有
                "-MajorBrand=qt  ", "-MinorVersion=0.0.0", "-CompatibleBrands=qt  ", # QuickTime 容器
                "-HandlerDescription=Core Media Video",
                "-CompressorName=", "-Encoder="
            ]
        else:
            brand_tags = [
                f"-Make={make_val}", f"-Model={model_val}", f"-Software={sw_val}",
                "-MajorBrand=mp42", "-MinorVersion=0.0.0", "-CompatibleBrands=mp42isom", # MP4 v2 容器
                "-HandlerDescription=VideoHandle",
                "-CompressorName=", "-Encoder="
            ]

        exif_base_cmd = [
            EXIFTOOL_EXE, '-overwrite_original', '-api', 'LargeFileSupport=1',
            f"-CreateDate={ts_exif}",
            f"-ModifyDate={ts_exif}",
            f"-DateTimeOriginal={ts_exif}",
            f"-MediaCreateDate={ts_qt}",
            f"-MediaModifyDate={ts_qt}",
            f"-InternalSerialNumber={unique_serial}",
            f"-GPSLatitude={abs(final_lat)}", f"-GPSLatitudeRef={lat_ref}",
            f"-GPSLongitude={abs(final_lon)}", f"-GPSLongitudeRef={lon_ref}",
            f"-GPSAltitude={random.randint(10, 100)}", f"-GPSAltitudeRef=0"
        ]

        # 执行 Exif 写入
        full_exif_cmd = exif_base_cmd + brand_tags + [str(output_file)]
        result = subprocess.run(full_exif_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # 降级重试 (只写基础 Exif)
            print(f"[!] Warning: Advanced metadata failed, applying basic tags. Error: {result.stderr}")
            subprocess.run(exif_base_cmd + [str(output_file)])

        # F. 文件时间同步
        os.utime(output_file, (cap_dt.timestamp(), cap_dt.timestamp()))
        print(f"[+] 幽灵化完成: {filename} | {model_val} | 去黑边: ✅ | 原生色彩: ✅")
        return True

    except Exception as e:
        print(f"[!] 错误 {input_file}: {e}")
        return False

# ==========================================
# 5. 主程序入口
# ==========================================
def main():
    freeze_support()
    
    # 隐藏控制台 (如果是打包后的 exe)
    # if sys.platform == 'win32':
        # ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    print("--- PolaFlow Anti-Forensic Engine v29.0 (Heisenberg Edition) ---")

    region_data = select_timezone_visual()

    if region_data is not None:
        in_p, out_p = Path("./raw"), Path("./output")
        in_p.mkdir(exist_ok=True)
        out_p.mkdir(exist_ok=True)

        raw_files = [f for f in in_p.glob("*.*") if f.suffix.lower() in ('.mp4', '.mov', '.m4v', '.webm')]
        if not raw_files:
            messagebox.showinfo("提示", "raw 文件夹为空！请放入视频素材。")
            return

        tasks = [(f, out_p, region_data) for f in raw_files]
        
        # 智能并发控制：保留一半核心给系统，防止卡死
        cpu_cores = max(1, int(os.cpu_count() / 2))
        
        print(f"[*] 引擎启动 | 核心: {cpu_cores} | 任务: {len(tasks)}")
        print("[*] 正在执行全维度指纹清洗...")

        with Pool(cpu_cores) as pool:
            pool.starmap(mutate_video, tasks)

        messagebox.showinfo("完成", f"所有任务处理完成！\n共处理: {len(tasks)} 个文件\n输出路径: {out_p.absolute()}")

if __name__ == "__main__":
    main()
