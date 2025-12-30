import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import sys
import pandas as pd

# 导入核心处理模块和版本信息
from core import single_core
from core import dual_core_gui_adapter
from core._version import __version__, __author__

# ================= 配置区 =================
# 语言包字典
TRANSLATIONS = {
    "title": {"zh": "酶标仪数据预处理", "en": "mProcess - Data Handler"},
    "mode_label": {"zh": "选择处理模式:", "en": "Select Mode:"},
    "single": {"zh": "单通道 (Intensity)", "en": "Single (Intensity)"},
    "dual": {"zh": "双通道 (Ratio)", "en": "Dual (Ratio)"},
    "file_label": {"zh": "📁 选择 Excel 文件:", "en": "📁 Select Excel File:"},
    "browse_btn": {"zh": "🔍 浏览文件", "en": "🔍 Browse"},
    "status_waiting": {"zh": "", "en": ""},
    "status_processing": {"zh": "⏳ 正在处理，请稍候...", "en": "⏳ Processing, please wait..."},
    "status_done": {"zh": "✅ 处理完成", "en": "✅ Done"},
    "status_error": {"zh": "❌ 出错", "en": "❌ Error"},
    "run_btn": {"zh": "🟢 开始处理", "en": "🟢 Run Process"},
    "quit_btn": {"zh": "❌ 关闭程序", "en": "❌ Exit"},
    "warn_title": {"zh": "警告", "en": "Warning"},
    "warn_no_file": {"zh": "请选择有效的 Excel 文件", "en": "Please select a valid Excel file."},
    "info_title": {"zh": "完成", "en": "Success"},
    "info_success": {"zh": "以下文件已生成：\n\n", "en": "Files generated:\n\n"},
    "err_title": {"zh": "错误", "en": "Error"},
    "lang_switch": {"zh": "English", "en": "中文"},  # 按钮显示的是“去往”的语言
    "copyright": {"zh": f"© 2025 {__author__} — v{__version__}", "en": f"© 2025 {__author__} — v{__version__}"}
}

# 当前语言状态 (默认中文)
current_lang = "zh"
# 存储UI元素的引用，以便更新文字
ui_elements = {}

def resource_path(relative_path):
    """获取资源绝对路径 (适配打包后的 exe)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_text(key):
    """根据当前语言获取文本"""
    return TRANSLATIONS[key].get(current_lang, "N/A")

def toggle_language(root):
    """切换语言并刷新界面"""
    global current_lang
    current_lang = "en" if current_lang == "zh" else "zh"
    update_ui_text(root)

def update_ui_text(root):
    """刷新所有界面元素的文本"""
    root.title(get_text("title"))
    
    # 更新普通 Label 和 Button
    ui_elements['mode_label'].config(text=get_text("mode_label"))
    ui_elements['single_radio'].config(text=get_text("single"))
    ui_elements['dual_radio'].config(text=get_text("dual"))
    ui_elements['file_label'].config(text=get_text("file_label"))
    ui_elements['copyright_label'].config(text=get_text("copyright"))
    ui_elements['lang_btn'].config(text=get_text("lang_switch"))

    # 更新 Canvas 自定义按钮的文本
    for btn_key in ['browse_btn', 'run_btn', 'quit_btn']:
        canvas, text_id = ui_elements[btn_key]
        canvas.itemconfigure(text_id, text=get_text(btn_key))

def start_gui():
    root = tk.Tk()
    root.geometry("300x560") #稍微加高一点以容纳语言按钮
    root.configure(bg="#FFF5E5")
    root.resizable(False, False)
    
    # 初始化时设置标题
    root.title(TRANSLATIONS["title"]["zh"])

    selected_file = tk.StringVar()
    mode_var = tk.StringVar(value="single")

    # === 语言切换按钮 (右上角) ===
    lang_frame = tk.Frame(root, bg="#FFF5E5")
    lang_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    
    lang_btn = tk.Button(lang_frame, text="English", font=("Arial", 9), 
                         command=lambda: toggle_language(root),
                         bg="white", relief=tk.GROOVE)
    lang_btn.pack(side=tk.RIGHT)
    ui_elements['lang_btn'] = lang_btn

    # === Logo ===
    try:
        # 注意：这里路径改为了 assets
        img_path = resource_path(os.path.join("assets", "WK.png"))
        img = Image.open(img_path).resize((70, 70))
        logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(root, image=logo_img, bg="#FFF5E5")
        logo_label.image = logo_img
        logo_label.pack(pady=5)
    except Exception as e:
        print(f"⚠️ 图片加载失败：{e}")

    # === 模式选择 ===
    mode_title = tk.Frame(root, bg="#FFF5E5")
    mode_title.pack(pady=6)
    tk.Label(mode_title, text="⚙️", fg="orange", font=("Arial", 11), bg="#FFF5E5").pack(side=tk.LEFT)
    lbl_mode = tk.Label(mode_title, text=TRANSLATIONS["mode_label"]["zh"], font=("Arial", 11), bg="#FFF5E5")
    lbl_mode.pack(side=tk.LEFT)
    ui_elements['mode_label'] = lbl_mode

    mode_frame = tk.Frame(root, bg="#FFF5E5")
    mode_frame.pack(pady=5)

    style_common = {
        "indicatoron": False,
        "width": 14, #稍微宽一点适应英文
        "font": ("Arial", 10, "bold"),
        "relief": tk.FLAT,
        "activebackground": "pink",
        "selectcolor": "orange"
    }

    rb_single = tk.Radiobutton(mode_frame, text=TRANSLATIONS["single"]["zh"], variable=mode_var, value="single", **style_common)
    rb_dual = tk.Radiobutton(mode_frame, text=TRANSLATIONS["dual"]["zh"], variable=mode_var, value="dual", **style_common)
    
    rb_single.pack(pady=2)
    rb_dual.pack(pady=2)
    
    ui_elements['single_radio'] = rb_single
    ui_elements['dual_radio'] = rb_dual

    # 按钮样式联动
    def update_button_styles(*args):
        if mode_var.get() == "single":
            rb_single.config(bg="pink", fg="black")
            rb_dual.config(bg="orange", fg="white")
        else:
            rb_dual.config(bg="pink", fg="black")
            rb_single.config(bg="orange", fg="white")

    update_button_styles()
    mode_var.trace_add("write", update_button_styles)

    # === 文件选择 ===
    lbl_file = tk.Label(root, text=TRANSLATIONS["file_label"]["zh"], bg="#FFF5E5")
    lbl_file.pack(pady=(10, 2))
    ui_elements['file_label'] = lbl_file
    
    file_entry = tk.Entry(root, width=38)
    file_entry.pack(pady=2)

    def choose_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            selected_file.set(file_path)
            file_entry.delete(0, tk.END)
            file_entry.insert(0, os.path.basename(file_path))

    # 自定义按钮 - 浏览
    ui_elements['browse_btn'] = create_custom_button(root, "browse_btn", choose_file)

    # === 状态与进度 ===
    status_label = tk.Label(root, text="", fg="green", bg="#FFF5E5", font=("Arial", 10))
    status_label.pack(pady=5)

    progress = ttk.Progressbar(root, mode='determinate', length=200)
    progress.pack(pady=5)
    progress.pack_forget()

    # === 运行逻辑 ===
    def run_clicked():
        file_path = selected_file.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning(get_text("warn_title"), get_text("warn_no_file"))
            return
        
        try:
            selected_mode = mode_var.get()
            sheet_count = len(pd.ExcelFile(file_path).sheet_names)

            # 估算步骤
            if selected_mode == "single":
                estimated_steps = sheet_count * 12 + 10 
            else:
                estimated_steps = sheet_count * 5 * 8 + 10

            progress.config(maximum=estimated_steps, value=0)
            progress.pack()
            status_label.config(text=get_text("status_processing"))
            root.update_idletasks()

            def update_progress():
                progress['value'] += 1
                root.update_idletasks()

            if selected_mode == "single":
                files = single_core.run_main(file_path, on_step=update_progress)
            else:
                files = dual_core_gui_adapter.run_main(file_path, on_step=update_progress)

            status_label.config(text=get_text("status_done"))
            progress['value'] = estimated_steps
            root.update_idletasks()
            
            messagebox.showinfo(get_text("info_title"), get_text("info_success") + "\n".join(files))
            root.after(1000, progress.pack_forget)

        except Exception as e:
            progress.pack_forget()
            status_label.config(text=get_text("status_error"))
            messagebox.showerror(get_text("err_title"), str(e))

    # 自定义按钮 - 运行与退出
    ui_elements['run_btn'] = create_custom_button(root, "run_btn", run_clicked)
    ui_elements['quit_btn'] = create_custom_button(root, "quit_btn", root.quit)

    # === 底部版权 ===
    lbl_copy = tk.Label(root, text=TRANSLATIONS["copyright"]["zh"], fg="gray", bg="#FFF5E5", font=("Arial", 8))
    lbl_copy.pack(side=tk.BOTTOM, pady=8)
    ui_elements['copyright_label'] = lbl_copy

    root.mainloop()

def create_custom_button(parent, text_key, command):
    """
    创建自定义Canvas按钮
    返回: (canvas_object, text_item_id) 用于后续更新文本
    """
    canvas = tk.Canvas(parent, width=180, height=40, bg="#FFF5E5", highlightthickness=0)
    canvas.pack(pady=5)
    
    # 绘制按钮背景
    canvas.create_rectangle(10, 8, 170, 32, fill="orange", outline="#DDD", width=1)
    
    # 绘制文字 (初始使用中文)
    initial_text = TRANSLATIONS[text_key]["zh"]
    text_id = canvas.create_text(90, 20, text=initial_text, fill="white", font=("Arial", 10, "bold"))
    
    # 绑定事件
    canvas.tag_bind(text_id, "<Button-1>", lambda e: command())
    canvas.tag_bind("all", "<Enter>", lambda e: canvas.config(cursor="hand2"))
    
    # 对于点击整个矩形区域也生效
    canvas.bind("<Button-1>", lambda e: command())

    return canvas, text_id

if __name__ == "__main__":
    start_gui()