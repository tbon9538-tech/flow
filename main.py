import os
import sys
import uuid
import random
import subprocess
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ==========================================
# [CONFIGURATION] 核心配置区
# ==========================================

# 请将此处路径替换为你实际的二进制文件路径
FFMPEG_EXE = r"C:\ffmpeg\bin\ffmpeg.exe"  # 或 'ffmpeg' (如果已在 PATH 中)
EXIFTOOL_EXE = r"C:\exiftool\exiftool.exe" # 或 'exiftool'

# 设备指纹库 (模拟真实用户分布)
# 格式: (Make, Model, Software, ScaleFactor)
DEVICE_DATABASE = [
    ("Apple", "iPhone 13 Pro", "15.1.1", 1.0),
    ("Apple", "iPhone 14", "16.0", 1.0),
    ("Apple", "iPhone 12", "14.8", 1.0),
    ("Samsung", "SM-G991B", "Android 12", 1.0), # Galaxy S21
    ("Samsung", "SM-G998B", "Android 13", 1.0), # Galaxy S21 Ultra
    ("Google", "Pixel 6", "Android 12", 1.0),
    ("Xiaomi", "M2102K1G", "Android 11", 1.0),  # Mi 11 Ultra
]

# ==========================================
# [MODULE] 视觉链生成器
# ==========================================
def get_ultimate_visual_chain():
    """
    生成随机视觉噪声与色彩微扰，打破图像哈希 (Image Hash)。
    不再使用简单的叠加，而是模拟 CMOS 传感器的热噪声。
    """
    # 极微小的对比度/亮度波动 (模拟光线变化)
    contrast = round(random.uniform(0.98, 1.02), 3)
    brightness = round(random.uniform(-0.02, 0.02), 3)
    saturation = round(random.uniform(0.95, 1.05), 3)
    
    # 模拟传感器噪点 (极低强度，避免肉眼可见，但在机器视觉层面是不同的)
    noise_filter = f"noise=alls=1:allf=t+u" 
    
    chain = [
        f"eq=contrast={contrast}:brightness={brightness}:saturation={saturation}",
        noise_filter,
        # 强制色彩空间转换，防止 YUV 范围溢出
        "scale=out_color_matrix=bt709:out_range=tv" 
    ]
    return chain

# ==========================================
# [CORE] 主逻辑函数
# ==========================================
def mutate_video(input_file, output_dir, region_data):
    """
    执行全维度视频重构与指纹清洗
    """
    offset, base_lat, base_lon = region_data
    input_path = Path(input_file)
    output_path_obj = Path(output_dir)
    
    # 确保输出目录存在
    output_path_obj.mkdir(parents=True, exist_ok=True)

    try:
        # -------------------------------------------------
        # A. 硬件指纹仿真 (Device Emulation)
        # -------------------------------------------------
        make_val, model_val, sw_val, _ = random.choice(DEVICE_DATABASE)
        is_apple = (make_val == "Apple")
        
        unique_id = str(uuid.uuid4())[:8]
        process_type = ""
        filename = ""

        # -------------------------------------------------
        # B. 命名拓扑学 (Naming Topology)
        # -------------------------------------------------
        if is_apple:
            # iOS 逻辑
            if random.random() < 0.85:
                # 原生相机: IMG_XXXX.MOV
                filename = f"IMG_{random.randint(1000, 9999)}.MOV"
                process_type = "Native Camera (iOS)"
            else:
                # 剪辑导出: YYYY-MM-DD 格式
                date_str = datetime.now().strftime('%Y-%m-%d')
                filename = f"Video {date_str} at {random.randint(10, 23)}.{random.randint(10, 59)}.{random.randint(10, 59)}.mp4"
                process_type = "Editor Export (iOS)"
        else:
            # Android 逻辑
            date_str = datetime.now().strftime('%Y%m%d')
            time_str = datetime.now().strftime('%H%M%S')
            
            if random.random() < 0.8:
                # Samsung/Pixel: YYYYMMDD_HHMMSS.mp4
                filename = f"{date_str}_{time_str}.mp4"
                process_type = "Native Camera (Android)"
            else:
                # WhatsApp/Editor
                filename = f"VID-{date_str}-WA{random.randint(1000,9999)}.mp4"
                process_type = "Social Export (Android)"

        output_file = output_path_obj / filename

        # -------------------------------------------------
        # C. 听觉熵增 (Audio Entropy) - V3 Pro
        # -------------------------------------------------
        # 移除人工混响，模拟麦克风频响曲线 + 极微小时钟漂移
        
        # 随机化音高/速度 (Hash Breaking) - 极微量，人耳不可察觉
        pitch_factor = random.uniform(0.992, 1.008) 
        
        # 模拟麦克风 EQ (不同手机麦克风对高低频的收音不同)
        low_cut = random.randint(50, 120)
        high_cut = random.randint(15000, 19000)
        mic_eq = f"highpass=f={low_cut},lowpass=f={high_cut}"
        
        # 动态归一化，模拟手机麦克风的自动增益控制 (AGC)
        dyn_norm = "dynaudnorm=f=150:g=15:p=0.9:m=10.0"

        ap_chain = (
            f"{mic_eq},"
            f"atempo={pitch_factor:.5f}," 
            f"aresample=44100," 
            f"volume={random.uniform(0.95, 1.05):.2f},"
            f"{dyn_norm}"
        )

        # -------------------------------------------------
        # D. FFmpeg 编码 (The Matrix Build)
        # -------------------------------------------------
        target_fps = random.choice(["23.976", "29.97", "30", "59.94", "60"])
        
        # 获取视觉滤镜链
        vf_filters = get_ultimate_visual_chain()
        # 关键：强制 pixel format 为 yuv420p (移动端标准)，防止变为 yuv444p
        vf_chain = ",".join(vf_filters + ["format=yuv420p"])

        cmd = [
            str(FFMPEG_EXE), '-y', '-hide_banner', '-loglevel', 'error',
            '-i', str(input_path),
            '-vf', vf_chain, 
            '-af', ap_chain,
            '-r', target_fps,
            
            # 视频编码参数
            '-c:v', 'libx264',
            # 模拟硬件编码器的 CBR 行为，去除 FFmpeg 标识
            '-x264-params', 'no-info=1:nal-hrd=cbr', 
            '-bsf:v', 'filter_units=remove_types=6', # 移除 SEI 用户数据
            '-crf', str(random.randint(21, 25)),     # 移动端常用压缩率
            '-maxrate', '12M',                       # 限制最大码率，符合手机性能
            '-bufsize', '24M',
            '-preset', 'veryfast',                   # 手机录制通常是快速预设
            '-tune', 'film',
            
            # [关键] 注入 BT.709 色彩标签 - 欺骗检测算法这是原生相机拍摄
            '-color_primaries', '1', 
            '-color_trc', '1', 
            '-colorspace', '1',
            
            # Web 优化
            '-movflags', '+faststart', 
            
            # 音频编码参数
            '-c:a', 'aac',
            '-ar', '44100',
            '-b:a', '128k', 
            str(output_file)
        ]

        # 执行转码
        subprocess.run(cmd, check=True)

        # -------------------------------------------------
        # E. 元数据深度注入 (Metadata Injection)
        # -------------------------------------------------
        target_now = datetime.now(timezone.utc) + timedelta(hours=offset)
        # 拍摄时间通常早于上传 (30分钟到2天)
        cap_dt = target_now - timedelta(minutes=random.randint(30, 2800))
        
        # ExifTool 格式化
        tz_sign = "+" if offset >= 0 else "-"
        tz_str = f"{tz_sign}{abs(offset):02d}:00"
        
        # Exif 标准时间串
        ts_exif = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S{tz_str}')
        # QuickTime 标准时间串 (通常不带时区，或UTC)
        ts_qt = cap_dt.strftime(f'%Y:%m:%d %H:%M:%S')

        # GPS 坐标模糊化 (Jitter)
        lat_jitter = random.uniform(-0.005, 0.005) 
        lon_jitter = random.uniform(-0.005, 0.005)
        final_lat = base_lat + lat_jitter
        final_lon = base_lon + lon_jitter
        
        # GPS 引用方向
        lat_ref = "N" if final_lat >= 0 else "S"
        lon_ref = "E" if final_lon >= 0 else "W"
        
        # 海拔模拟 (增加真实度)
        altitude = random.randint(5, 300)

        # 构建 ExifTool 命令
        exif_cmd = [
            str(EXIFTOOL_EXE), 
            '-overwrite_original', 
            '-api', 'LargeFileSupport=1',
            
            # 通用时间戳
            f"-CreateDate={ts_exif}",
            f"-ModifyDate={ts_exif}",
            f"-DateTimeOriginal={ts_exif}",
            f"-MediaCreateDate={ts_qt}", 
            f"-MediaModifyDate={ts_qt}",
            f"-TrackCreateDate={ts_qt}",
            f"-TrackModifyDate={ts_qt}",
            
            # GPS 数据
            f"-GPSLatitude={abs(final_lat)}",
            f"-GPSLatitudeRef={lat_ref}",
            f"-GPSLongitude={abs(final_lon)}",
            f"-GPSLongitudeRef={lon_ref}",
            f"-GPSAltitude={altitude}",
            f"-GPSAltitudeRef=0"
        ]

        # 品牌特征分支
        if is_apple:
            # Apple 特征: QuickTime (qt) 容器结构
            brand_tags = [
                f"-Make=Apple",
                f"-Model={model_val}",
                f"-Software={sw_val}",
                f"-CreationDate={ts_exif}", # iOS 特有标签
                "-MajorBrand=qt  ",         # 注意空格
                "-MinorVersion=0.0.0",
                "-CompatibleBrands=qt  ",
                "-HandlerDescription=Core Media Video",
                # 清除编码痕迹
                "-CompressorName=", 
                "-Encoder=" 
            ]
        else:
            # Android 特征: MP4 v2 (mp42) 容器结构
            brand_tags = [
                f"-Make={make_val}",
                f"-Model={model_val}",
                f"-Software={sw_val}",
                "-MajorBrand=mp42",
                "-MinorVersion=0.0.0",
                "-CompatibleBrands=mp42isom",
                "-HandlerDescription=VideoHandle",
                "-CompressorName=",
                "-Encoder="
            ]

        # 合并命令并执行
        full_exif_cmd = exif_cmd + brand_tags + [str(output_file)]
        
        # 抑制输出，只捕获错误
        res = subprocess.run(full_exif_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[!] Exif Warning: {res.stderr}")

        # -------------------------------------------------
        # F. 文件系统时间层同步 (FS Timestamp)
        # -------------------------------------------------
        # 修改文件的 access 和 modify time 以匹配 Exif
        os.utime(str(output_file), (cap_dt.timestamp(), cap_dt.timestamp()))
        
        print(f"[+] 幽灵化成功: {filename} | {model_val} | 伪装: {'Apple' if is_apple else 'Android'}")
        return True

    except Exception as e:
        print(f"[!] 严重错误 {input_file}: {e}")
        # 销毁失败的样本，防止脏数据上传
        if 'output_file' in locals() and output_file.exists():
             try:
                 os.remove(output_file)
             except:
                 pass
        return False

# ==========================================
# [TEST] 本地测试入口
# ==========================================
if __name__ == "__main__":
    # 模拟测试
    dummy_input = "test_source.mp4"
    dummy_output = "output_render"
    # 东京区域 (UTC+9, Lat, Lon)
    dummy_region = (9, 35.6895, 139.6917) 
    
    if not os.path.exists(dummy_input):
        print(f"[*] 请放置一个名为 {dummy_input} 的文件进行测试。")
    else:
        print("[*] 启动红队混淆引擎...")
        mutate_video(dummy_input, dummy_output, dummy_region)
