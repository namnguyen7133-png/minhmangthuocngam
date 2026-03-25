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
    if not data: 
        print("❌ LỖI: Không tìm thấy file config.txt")
        return

    # Thông tin từ hình ảnh GitHub của chú
    token = data.get("TOKEN_ACCESS")
    branch = data.get("BRANCH_NAME", "main")
    
    # Tạo URL bảo mật dùng Token để không bị hỏi mật khẩu (Lỗi /dev/tty)
    # Cấu trúc: https://<token>@github.com/namnguyen7133-png/minhmangthuocngam.git
    final_url = f"https://{token}@github.com/namnguyen7133-png/minhmangthuocngam.git"

    try:
        os.chdir(BASE_DIR)
        
        # Thiết lập môi trường không tương tác để chặn mọi hộp thoại hỏi mật khẩu
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        
        if not os.path.exists(os.path.join(BASE_DIR, ".git")):
            subprocess.run(["git", "init"], capture_output=True, env=env)
        
        # Làm sạch remote cũ để nạp URL mới có chứa Token
        subprocess.run(["git", "remote", "remove", "origin"], capture_output=True, env=env)
        subprocess.run(["git", "remote", "add", "origin", final_url], check=True, env=env)

        print("📦 Đang chọn đúng 2 thư mục dữ liệu...")
        p1 = data.get("PATH_SCRAPER")
        p2 = data.get("PATH_SHOPEE")

        if p1: subprocess.run(f'git add "{p1}"', shell=True, env=env)
        if p2: subprocess.run(f'git add "{p2}"', shell=True, env=env)
        subprocess.run(["git", "add", "bot_shopee.py"], capture_output=True, env=env)

        subprocess.run(["git", "branch", "-M", branch], check=True, env=env)
        
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"Data Update: {time_now}"], capture_output=True, env=env)

        print("🚀 Đang gửi dữ liệu lên GitHub...")
        # Lệnh ép đẩy dữ liệu (Force Push) kèm theo môi trường đã cấu hình
        result = subprocess.run(["git", "push", "-u", "-f", "origin", branch], capture_output=True, text=True, env=env)

        if result.returncode == 0:
            print(f"\n✅ THÀNH CÔNG RỒI CHÚ NAM!")
            print(f"Dữ liệu đã lên: https://github.com/namnguyen7133-png/minhmangthuocngam")
        else:
            # Nếu lỗi, kiểm tra xem Token có đúng quyền 'workflow' và 'repo' không
            print(f"❌ LỖI: {result.stderr}")

    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")

if __name__ == "__main__":
    day_hang_phuc_hoi()
    input("\nBấm Enter để đóng...")