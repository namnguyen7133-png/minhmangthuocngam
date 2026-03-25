import os
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.txt")

def doc_cau_hinh():
    config = {}
    if not os.path.exists(CONFIG_FILE): return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                k, v = line.split(":", 1)
                config[k.strip()] = v.strip()
    return config

def day_hang_phuc_hoi():
    data = doc_cau_hinh()
    if not data: return

    repo_url = data["LINK_GITHUB"]
    token = data["TOKEN_ACCESS"]
    branch = data.get("BRANCH_NAME", "main")
    
    # Ép dùng Token để đăng nhập không cần hiện bảng
    final_url = repo_url.replace("https://", f"https://{token}@")

    try:
        os.chdir(BASE_DIR)
        
        # Cấu hình Git dùng Token để không hỏi mật khẩu
        subprocess.run(["git", "config", "--local", "credential.helper", ""], capture_output=True)
        
        if not os.path.exists(os.path.join(BASE_DIR, ".git")):
            subprocess.run(["git", "init"], capture_output=True)
        
        subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", final_url], check=True)

        print("📦 Đang chọn đúng 2 thư mục dữ liệu...")
        # Lấy đường dẫn từ file config của chú
        p1 = data["PATH_SCRAPER"]
        p2 = data["PATH_SHOPEE"]

        # Chỉ thêm đúng 2 thư mục này
        subprocess.run(f'git add "{p1}"', shell=True)
        subprocess.run(f'git add "{p2}"', shell=True)
        subprocess.run(["git", "add", "bot_shopee.py"], capture_output=True)

        subprocess.run(["git", "branch", "-M", branch], check=True)
        
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"Data Update: {time_now}"], capture_output=True)

        print("🚀 Đang gửi dữ liệu (không cần đăng nhập tay)...")
        # Lệnh quan trọng để ép GitHub nhận Token
        result = subprocess.run(["git", "push", "-f", "origin", branch], capture_output=True, text=True)

        if result.returncode == 0:
            print("\n✅ THÀNH CÔNG RỒI CHÚ NAM! Dữ liệu 32 shop đã lên mạng.")
        else:
            print(f"❌ LỖI: {result.stderr}")

    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")

if __name__ == "__main__":
    day_hang_phuc_hoi()
    input("\nBấm Enter để đóng...")