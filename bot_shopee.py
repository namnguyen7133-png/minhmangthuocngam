import os
import subprocess
import shutil
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
    path_scraper = data.get("PATH_SCRAPER")
    path_shopee = data.get("PATH_SHOPEE")
    final_url = repo_url.replace("https://", f"https://{token}@")

    try:
        os.chdir(BASE_DIR)
        
        # Thử làm sạch nếu có thể, nếu bị Windows chặn thì bỏ qua để chạy tiếp
        dot_git = os.path.join(BASE_DIR, ".git")
        if os.path.exists(dot_git):
            try:
                shutil.rmtree(dot_git)
                print("🧹 Đã dọn dẹp xong bộ nhớ cũ.")
            except:
                print("⚠️ Đang cập nhật trực tiếp vào bộ nhớ hiện tại...")

        # Khởi tạo lại Git (lệnh này sẽ tự sửa lỗi nếu chưa có .git)
        subprocess.run(["git", "init"], capture_output=True)
        
        # Cập nhật địa chỉ gửi hàng
        subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", final_url], check=True)

        print("🎯 Đang chọn đúng 2 thư mục dữ liệu Shopee...")
        # CHỈ THÊM 2 THƯ MỤC DATA, KHÔNG THÊM CẢ MÁY TÍNH
        if path_scraper and os.path.exists(path_scraper):
            subprocess.run(["git", "add", f'"{path_scraper}"'], shell=True)
        if path_shopee and os.path.exists(path_shopee):
            subprocess.run(["git", "add", f'"{path_shopee}"'], shell=True)
        
        # Thêm file code này
        subprocess.run(["git", "add", "bot_shopee.py"], capture_output=True)

        subprocess.run(["git", "branch", "-M", branch], check=True)
        
        time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"Cap nhat data: {time_now}"], capture_output=True)

        print("🚀 Đang đẩy dữ liệu sạch lên GitHub...")
        result = subprocess.run([
            "git", "push", "-f", "--push-option=allow-unsafe", "-u", "origin", branch
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("\n✅ THÀNH CÔNG! Chỉ có 2 thư mục dữ liệu trên GitHub.")
        else:
            print(f"❌ LỖI: {result.stderr}")

    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")

if __name__ == "__main__":
    day_hang_phuc_hoi()
    input("\nBấm Enter để đóng...")