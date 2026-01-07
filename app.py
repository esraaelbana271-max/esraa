import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime


# 🎨 Theme Colors (غيرهم من هنا بسهولة)
BG = "#121212"
CARD = "#1e1e1e"
BTN_GREEN = "#009688"
BTN_BLUE = "#2962FF"
BTN_ORANGE = "#FF9800"
TEXT = "#ffffff"
GOLD = "#D4AF37"
ACCENT = "#4FC3F7"
LOG_TEXT = "#00FF7F"


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("منظم الملفات الذكي")
        self.root.geometry("800x600")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # تصنيفات الملفات
        self.EXTENSIONS = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
            "Videos": [".mp4", ".mkv", ".mov", ".avi"],
            "Audio": [".mp3", ".wav", ".aac"],
            "Archives": [".zip", ".rar", ".7z", ".tar"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"],
        }

        self.selected_categories = {}
        self.selected_path = None

        self.create_widgets()

    # ---------------- UI ----------------
    def create_widgets(self):
        # العنوان
        tk.Label(
            self.root,
            text="برنامج تنظيم الملفات",
            font=("Arial", 22, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(pady=15)

        # أيقونات التصنيف
        self.create_category_icons()

        # سجل العمليات
        self.log_area = scrolledtext.ScrolledText(
            self.root,
            width=85,
            height=14,
            font=("Consolas", 10),
            bg=CARD,
            fg=LOG_TEXT,
            insertbackground=TEXT,
        )
        self.log_area.pack(padx=15, pady=10)
        self.log("جاهز للاستخدام...")

        # الشريط السفلي
        self.create_bottom_bar()

    def create_category_icons(self):
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(pady=10)

        categories = [
            "Images", "Documents", "Videos",
            "Audio", "Archives", "Code"
        ]

        row = 0
        col = 0

        for category in categories:
            var = tk.BooleanVar()
            self.selected_categories[category] = var

            btn = tk.Checkbutton(
                frame,
                text=category,
                variable=var,
                indicatoron=False,
                width=18,
                height=4,
                font=("Arial", 11, "bold"),
                bg=CARD,
                fg=GOLD,
                selectcolor=ACCENT,
                relief="raised",
                bd=2,
            )

            btn.grid(row=row, column=col, padx=12, pady=12)

            col += 1
            if col == 3:
                col = 0
                row += 1

    def create_bottom_bar(self):
        bottom = tk.Frame(self.root, bg=CARD, height=70)
        bottom.pack(side="bottom", fill="x")

        tk.Button(
            bottom,
            text="📁 اختيار المجلد",
            command=self.select_folder,
            font=("Arial", 12),
            bg=BTN_GREEN,
            fg=TEXT,
            width=18,
            height=2,
        ).pack(side="left", padx=30, pady=10)

        tk.Button(
            bottom,
            text="⚙️ تنظيم الملفات",
            command=self.organize_selected,
            font=("Arial", 12, "bold"),
            bg=BTN_ORANGE,
            fg=TEXT,
            width=18,
            height=2,
        ).pack(side="right", padx=30, pady=10)

    # ---------------- Logic ----------------
    def log(self, message):
        time = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{time}] {message}\n")
        self.log_area.see(tk.END)

    def select_folder(self):
        self.selected_path = filedialog.askdirectory()
        if self.selected_path:
            self.log(f"تم اختيار المجلد: {self.selected_path}")

    def get_category(self, suffix):
        for category, exts in self.EXTENSIONS.items():
            if suffix.lower() in exts:
                return category
        return None

    def organize_selected(self):
        if not self.selected_path:
            messagebox.showwarning("تنبيه", "اختاري المجلد الأول")
            return

        chosen = [c for c, v in self.selected_categories.items() if v.get()]
        if not chosen:
            messagebox.showwarning("تنبيه", "اختاري نوع ملفات واحد على الأقل")
            return

        path = Path(self.selected_path)
        moved = 0

        try:
            for item in path.iterdir():
                if item.is_dir():
                    continue

                category = self.get_category(item.suffix)
                if category not in chosen:
                    continue

                dest = path / category
                dest.mkdir(exist_ok=True)

                shutil.move(str(item), str(dest / item.name))
                self.log(f"نقل: {item.name} → {category}")
                moved += 1

            self.log("-" * 40)
            self.log(f"تم الانتهاء | عدد الملفات: {moved}")
            messagebox.showinfo("نجاح", f"تم تنظيم {moved} ملف بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", str(e))


# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()








