import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import pandas as pd

# 导入核心处理模块
import single_core
import dual_core_gui_adapter

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def start_gui():
    root = tk.Tk()
    root.title("酶标仪数据预处理")
    root.geometry("280x500")
    root.configure(bg="#FFF5E5")
    root.resizable(False, False)

    selected_file = tk.StringVar()
    mode_var = tk.StringVar(value="single")

    # 顶部 Logo
    try:
        img_path = resource_path("WK.png")
        img = Image.open(img_path).resize((60, 60))
        logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo_img, bg="#FFF5E5")
        logo_label.image = logo_img
        logo_label.pack(pady=10)
    except Exception as e:
        print(f"⚠️ 图片加载失败：{e}")

    # 模式选择
    mode_title = tk.Frame(root, bg="#FFF5E5")
    mode_title.pack(pady=6)
    tk.Label(mode_title, text="⚙️", fg="orange", font=("Arial", 11), bg="#FFF5E5").pack(side=tk.LEFT)
    tk.Label(mode_title, text="选择处理模式:", font=("Arial", 11), bg="#FFF5E5").pack(side=tk.LEFT)

    mode_frame = tk.Frame(root, bg="#FFF5E5")
    mode_frame.pack(pady=5)

    style_common = {
        "indicatoron": False,
        "width": 10,
        "font": ("Arial", 10, "bold"),
        "relief": tk.FLAT,
        "activebackground": "pink",
        "selectcolor": "orange"
    }

    single_btn = tk.Radiobutton(mode_frame, text="单通道", variable=mode_var, value="single", **style_common)
    dual_btn = tk.Radiobutton(mode_frame, text="双通道", variable=mode_var, value="dual", **style_common)

    single_btn.pack(side=tk.LEFT, padx=5)
    dual_btn.pack(side=tk.LEFT, padx=5)

    def update_button_styles(*args):
        if mode_var.get() == "single":
            single_btn.config(bg="pink", fg="black")
            dual_btn.config(bg="orange", fg="white")
        else:
            dual_btn.config(bg="pink", fg="black")
            single_btn.config(bg="orange", fg="white")

    update_button_styles()
    mode_var.trace_add("write", update_button_styles)

    # 文件选择
    tk.Label(root, text="📁 选择 Excel 文件:", bg="#FFF5E5").pack(pady=6)
    file_entry = tk.Entry(root, width=42)
    file_entry.pack()

    def choose_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel 文件", "*.xlsx")])
        if file_path:
            selected_file.set(file_path)
            file_entry.delete(0, tk.END)
            file_entry.insert(0, os.path.basename(file_path))

    create_custom_button(root, "🔍 浏览文件", choose_file)

    # 状态标签
    status_label = tk.Label(root, text="", fg="green", bg="#FFF5E5")
    status_label.pack(pady=6)

    # 进度条
    progress = ttk.Progressbar(root, mode='determinate', length=180)
    progress.pack(pady=6)
    progress.pack_forget()

    # 运行逻辑
    def run_clicked():
        file_path = selected_file.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning("警告", "请选择有效的 Excel 文件")
            return
        try:
            selected_mode = mode_var.get()
            sheet_count = len(pd.ExcelFile(file_path).sheet_names)

            # 估算处理步骤
            if selected_mode == "single":
                estimated_steps = sheet_count * 12 + 10  # 每 sheet 约 12 步 + 后处理
            else:
                estimated_columns_per_module = 8  # T1–T6 + DR + AU
                estimated_steps = sheet_count * 5 * estimated_columns_per_module + 10

            progress.config(mode='determinate', maximum=estimated_steps, value=0)
            progress.pack()
            status_label.config(text="⏳ 正在处理，请稍候...")
            root.update_idletasks()

            def update_progress():
                progress['value'] += 1
                root.update_idletasks()

            if selected_mode == "single":
                files = single_core.run_main(file_path, on_step=update_progress)
            else:
                files = dual_core_gui_adapter.run_main(file_path, on_step=update_progress)

            status_label.config(text="✅ 处理完成")
            progress['value'] = estimated_steps
            root.update_idletasks()
            messagebox.showinfo("完成", "以下文件已生成：\n\n" + "\n".join(files))
            root.after(800, progress.pack_forget)

        except Exception as e:
            progress.pack_forget()
            status_label.config(text="❌ 出错")
            messagebox.showerror("错误", str(e))

    create_custom_button(root, "🟢 开始处理", run_clicked)
    create_custom_button(root, "❌ 关闭程序", root.quit)

    # 底部版权
    tk.Label(root, text="© 2025 Dr. Kui Wang — mProcess V4.0", fg="gray", bg="#FFF5E5").pack(side=tk.BOTTOM, pady=6)

    root.mainloop()

def create_custom_button(parent, text, command):
    canvas = tk.Canvas(parent, width=180, height=40, bg="#FFF5E5", highlightthickness=0)
    canvas.pack(pady=6)
    canvas.create_rectangle(10, 8, 170, 32, fill="orange", outline="#DDD", width=1)
    label = canvas.create_text(90, 20, text=text, fill="white", font=("Arial", 10, "bold"))
    canvas.tag_bind(label, "<Button-1>", lambda e: command())
    canvas.tag_bind("all", "<Enter>", lambda e: canvas.config(cursor="hand2"))

if __name__ == "__main__":
    start_gui()
