import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys

class GameMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=50)

        # Tạo tiêu đề cho menu chính
        self.title = tk.Label(self.frame, text="Man In Red", font=("Hitmarker", 40))
        self.title.pack(pady=10)

        # Tạo chỗ nhập tên người chơi
        self.name_label = tk.Label(self.frame, text="Nhập tên của bạn:", font=("Helvetica", 16))
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Helvetica", 16))
        self.name_entry.pack(pady=10)

        # Tạo nút bắt đầu
        self.start_button = tk.Button(self.frame, text="Bắt đầu", command=self.batdau, font=("Helvetica", 14))
        self.start_button.pack(pady=10)

        # Tạo nút xem hướng dẫn
        self.instructions_button = tk.Button(self.frame, text="Hướng dẫn", command=self.huongdan, font=("Helvetica", 14))
        self.instructions_button.pack(pady=10)

        # Tạo nút xem bảng xếp hạng
        self.leaderboard_button = tk.Button(self.frame, text="Bảng xếp hạng", command=self.bangxephang, font=("Helvetica", 14))
        self.leaderboard_button.pack(pady=10)

    def batdau(self):
        # Lấy tên từ ô nhập
        player_name = self.name_entry.get().strip()
        if not player_name:
            messagebox.showerror("Lỗi", "Bạn phải nhập tên trước khi bắt đầu!")
            return

        # Ghi tên vào file bangxephang.txt
        with open("bangxephang.txt", "a", encoding="utf-8") as file:
            file.write(f"Player: {player_name}, Time: ")

        self.root.destroy()  # Đóng cửa sổ menu chính
        os.system(f"{sys.executable} game.py")  # Chạy file game.py

    def huongdan(self):
        instructions = (
            "Hướng dẫn tân thủ:\n\n"
            "** Tiêu diệt hết địch để qua màn **\n\n"
            "1. Di chuyển bằng các phím mũi tên.\n\n"
            "2. Nhảy bằng phím Space.\n\n"
            "3. Dash bằng phím k, khi dash qua kẻ địch có thẻ tiêu diệt chúng.\n\n"
            "4. Tránh các chướng ngại vật và kẻ thù.\n\n"
            "5. Khi phá đảo có thể dùng các nút 1,2,3,4,5 để chọn màn muốn chơi lại."
        )
        messagebox.showinfo("Hướng dẫn", instructions)

    def bangxephang(self):
        # Đọc nội dung file bangxephang.txt
        with open("bangxephang.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Phân tích và sắp xếp dữ liệu
        leaderboard = []
        for line in lines:
            parts = line.strip().split(", ")
            if len(parts) == 2:
                player = parts[0].split(": ")[1]  # Lấy tên người chơi
                time = float(parts[1].split(": ")[1][:-1])  # Lấy thời gian (loại bỏ 's')

                # Chuyển đổi thời gian từ giây sang phút:giây (kiểu 'phút' giây.s)
                minutes = int(time // 60)  # Tính số phút
                seconds = time % 60  # Tính số giây còn lại
                formatted_time = f"{minutes} phút {seconds:.1f}s"  # Định dạng thời gian chỉ phút và giây
                leaderboard.append((player, formatted_time))

        # Sắp xếp theo thời gian (thứ tự tăng dần)
        leaderboard.sort(key=lambda x: x[1])

        # Tạo cửa sổ mới để hiển thị bảng xếp hạng
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Bảng xếp hạng")

        # Tạo Treeview (bảng kiểu Excel)
        tree = ttk.Treeview(leaderboard_window, columns=("Rank", "Player", "Time"), show="headings", height=10)
        
        # Định dạng tiêu đề cột
        tree.heading("Rank", text="Hạng")
        tree.heading("Player", text="Tên Người Chơi")
        tree.heading("Time", text="Thời gian")

        # Định dạng cột
        tree.column("Rank", width=50, anchor="center")
        tree.column("Player", width=200, anchor="center")
        tree.column("Time", width=150, anchor="center")

        # Thêm dữ liệu vào bảng
        for rank, (player, formatted_time) in enumerate(leaderboard, start=1):
            tree.insert("", "end", values=(rank, player, formatted_time))

        tree.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = GameMenu(root)
    root.mainloop()
