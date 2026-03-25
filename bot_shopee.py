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

    repo_url = data.get("LINK_GITHUB")
    token = data.get("TOKEN_ACCESS")
    branch = data.get("BRANCH_NAME", "main")
    
    # Lấy đường dẫn và dọn dẹp các ký tự thừa
    path_scraper = data.get("PATH_SCRAPER").strip('"')
    path_shopee = data.get("PATH_SHOPEE").strip('"')
    
    # Dùng Token để tự động đăng nhập, không hiện bảng Sign In nữa
    final_url = repo_url.replace("https://", f"https://{token}@")

    try:
        os.chdir(BASE_DIR)
        
        # Khởi tạo lại để sạch sẽ
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", final_url], check=True)

        print("🎯 Đang tìm 2 thư mục dữ liệu...")
        
        # Thêm thư mục cẩn thận hơn
        co_du_lieu = False
        if os.path.exists(path_scraper):
            subprocess.run(["git", "add", "."], cwd=path_scraper) # Thêm file từ thư mục scraper
            co_du_lieu = True
        if os.path.exists(path_shopee):
            subprocess.run(["git", "add", "."], cwd=path_shopee) # Thêm file từ thư mục shopee
            co_du_lieu = True
            
        if not co_du_lieu:
            print("❌ Chú ơi, đường dẫn trong config.txt hình như bị sai, máy không thấy thư mục nào cả!")
            return

        subprocess.run(["git", "add", "bot_shopee.py"], capture_output=True)
        subprocess.run(["git", "branch", "-M", branch], check=True)
        
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"Cap nhat: {time_now}"], capture_output=True)

        print("🚀 Đang tự động đăng nhập và gửi dữ liệu...")
        # Lệnh này sẽ dùng Token để đi thẳng vào GitHub
        result = subprocess.run([
            "git", "push", "-f", "-u", "origin", branch
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("\n✅ THÀNH CÔNG RỒI CHÚ NAM!")
        else:
            print(f"❌ LỖI: {result.stderr}")

    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")

if __name__ == "__main__":
    day_hang_phuc_hoi()
    input("\nBấm Enter để đóng...")