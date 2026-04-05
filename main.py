"""
Kiril → Latin Çevirici
Modern, dark-theme desktop application with drag-and-drop support.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import tkinter as tk

from docx_handler import process_docx

# ── Theme Setup ──────────────────────────────────────────────────────────────
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# ── Color Palette ─────────────────────────────────────────────────────────────
BG_DARK       = "#0f1117"
BG_CARD       = "#1a1d27"
BG_CARD2      = "#20243a"
ACCENT        = "#4f6ef7"
ACCENT_HOVER  = "#3a58e8"
SUCCESS       = "#22c55e"
ERROR_COLOR   = "#ef4444"
TEXT_PRIMARY  = "#f1f5f9"
TEXT_MUTED    = "#64748b"
BORDER        = "#2d3147"


class DropZone(ctk.CTkFrame):
    """Custom drag-and-drop styled zone widget."""

    def __init__(self, master, on_file_selected, on_clear, **kwargs):
        super().__init__(
            master,
            fg_color=BG_CARD2,
            corner_radius=16,
            border_width=2,
            border_color=BORDER,
            **kwargs
        )
        self.on_file_selected = on_file_selected
        self.on_clear = on_clear
        self._setup_ui()
        self._setup_drag_drop()

    def _setup_ui(self):
        # Icon
        self.icon_label = ctk.CTkLabel(
            self,
            text="📂",
            font=ctk.CTkFont(size=52),
        )
        self.icon_label.pack(pady=(32, 8))

        self.main_label = ctk.CTkLabel(
            self,
            text="Faylı buraya sürükleyin",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        )
        self.main_label.pack()

        self.sub_label = ctk.CTkLabel(
            self,
            text="Yalnız DOCX faylları dəstəklənir",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_MUTED,
        )
        self.sub_label.pack(pady=(4, 24))

        self.or_label = ctk.CTkLabel(
            self,
            text="── yaxud ──",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_MUTED,
        )
        self.or_label.pack(pady=(0, 16))

        self.browse_btn = ctk.CTkButton(
            self,
            text="  Fayl Seç",
            command=self._browse,
            width=180,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
        )
        self.browse_btn.pack(pady=(0, 32))

        self.clear_btn = ctk.CTkButton(
            self,
            text="✕",
            width=32,
            height=32,
            corner_radius=16,
            fg_color=ERROR_COLOR,
            hover_color="#dc2626",
            text_color="white",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._clear,
            cursor="hand2"
        )

    def _clear(self):
        self.on_clear()

    def _setup_drag_drop(self):
        """Bind drag-and-drop via tkinterdnd2 if available, else silently skip."""
        try:
            import tkinterdnd2  # noqa: F401 – optional dep
            self.drop_target_register("DND_Files")  # type: ignore[attr-defined]
            self.dnd_bind("<<Drop>>", self._on_drop)  # type: ignore[attr-defined]
            self.dnd_bind("<<DragEnter>>", self._on_drag_enter)  # type: ignore[attr-defined]
            self.dnd_bind("<<DragLeave>>", self._on_drag_leave)  # type: ignore[attr-defined]
        except Exception:
            pass  # drag-and-drop not available; browse button still works

    def _on_drag_enter(self, event):
        self.configure(border_color=ACCENT)
        self.icon_label.configure(text="📥")

    def _on_drag_leave(self, event):
        self.configure(border_color=BORDER)
        self.icon_label.configure(text="📂")

    def _on_drop(self, event):
        self.configure(border_color=BORDER)
        self.icon_label.configure(text="📂")
        path = event.data.strip("{}")
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            if ext == ".docx":
                self.on_file_selected(path)
            else:
                messagebox.showwarning("Dəstəklənmir", "Yalnız DOCX faylları dəstəklənir.")

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Sənəd seçin",
            filetypes=[
                ("Word fayllar", "*.docx"),
                ("Bütün fayllar", "*.*"),
            ],
        )
        if path:
            self.on_file_selected(path)

    def set_selected_state(self, filename: str):
        self.icon_label.configure(text="✅")
        self.main_label.configure(text=filename, text_color=SUCCESS)
        self.sub_label.configure(text="Fayl seçildi – çevirmə hazırdır", text_color=TEXT_MUTED)
        self.configure(border_color=SUCCESS)
        self.clear_btn.place(relx=0.93, rely=0.12, anchor="center")

    def reset(self):
        self.icon_label.configure(text="📂")
        self.main_label.configure(text="Faylı buraya sürükleyin", text_color=TEXT_PRIMARY)
        self.sub_label.configure(text="Yalnız DOCX faylları dəstəklənir", text_color=TEXT_MUTED)
        self.configure(border_color=BORDER)
        self.clear_btn.place_forget()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kiril → Latin Çevirici")
        self.geometry("580x680")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)

        # Pəncərənin mərkəzə gəlməsi
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 580) // 2
        y = (self.winfo_screenheight() - 680) // 2
        self.geometry(f"580x680+{x}+{y}")

        # Pəncərə İkonu əlavə edirik (qovluqda icon.ico varsa istifadə edəcək)
        try:
            self.iconbitmap("icon.ico")
        except Exception:
            pass

        # ── State ──────────────────────────────────────────────────
        self.selected_file = None
        self.is_processing = False
        self.current_output = None

        self._build_ui()

    # ─────────────────────────────── UI BUILD ────────────────────────────────

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            title_frame,
            text="Кирил",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=TEXT_MUTED,
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="  →  ",
            font=ctk.CTkFont(family="Segoe UI", size=22),
            text_color=ACCENT,
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Latin",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        # ── Subtitle ─────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="DOCX sənədlərini Azərbaycan latın əlifbasına çevirin",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_MUTED,
        ).pack(pady=(24, 0))

        # ── Drop Zone ─────────────────────────────────────────────────────────
        self.drop_zone = DropZone(
            self, 
            on_file_selected=self._on_file_selected,
            on_clear=self._clear_file
        )
        self.drop_zone.pack(fill="x", padx=32, pady=(20, 0))

        # ── Progress bar ──────────────────────────────────────────────────────
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            mode="indeterminate",
            height=6,
            corner_radius=3,
            progress_color=ACCENT,
            fg_color=BG_CARD,
        )
        self.progress_bar.pack(fill="x")

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Fayl çevrilir, zəhmət olmasa gözləyin...",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=ACCENT,
        )
        self.progress_label.pack(pady=(8, 0))

        # ── Options ───────────────────────────────────────────────────────────
        self.replace_quotes_var = ctk.BooleanVar(value=False)
        self.quote_checkbox = ctk.CTkCheckBox(
            self,
            text="« və » dırnaqlarını \" ilə əvəz et",
            variable=self.replace_quotes_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER
        )
        self.quote_checkbox.pack(pady=(16, 0))

        # ── Convert Button ────────────────────────────────────────────────────
        self.convert_btn = ctk.CTkButton(
            self,
            text="Çevir  →",
            command=self._start_conversion,
            width=240,
            height=52,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            state="disabled",
            text_color=TEXT_PRIMARY,
        )
        self.convert_btn.pack(pady=28)

        # ── Result Card (hidden initially) ────────────────────────────────────
        self.result_card = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)

        result_icon = ctk.CTkLabel(
            self.result_card,
            text="✅",
            font=ctk.CTkFont(size=30),
        )
        result_icon.pack(pady=(20, 4))

        self.result_title = ctk.CTkLabel(
            self.result_card,
            text="Uğurla tamamlandı!",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=SUCCESS,
        )
        self.result_title.pack()

        self.result_path_label = ctk.CTkLabel(
            self.result_card,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_MUTED,
            wraplength=460,
        )
        self.result_path_label.pack(pady=(4, 16))

        self.open_btn = ctk.CTkButton(
            self.result_card,
            text="📁  Qovluğu Aç",
            command=self._open_folder,
            width=180,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=SUCCESS,
            hover_color="#16a34a",
        )
        self.open_btn.pack(pady=(0, 20))

        # ── Footer ────────────────────────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Azərbaycan Kiril → Latin • v2.0",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_MUTED,
        ).pack(side="bottom", pady=12)

    # ─────────────────────────────── LOGIC ───────────────────────────────────

    def _on_file_selected(self, path: str):
        self.selected_file = path
        name = os.path.basename(path)
        size_kb = os.path.getsize(path) / 1024
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"

        # Update drop zone
        self.drop_zone.set_selected_state(name)

        # Reset result card
        self.result_card.pack_forget()

        # Enable convert button
        self.convert_btn.configure(state="normal", text="Çevir  →")

    def _clear_file(self):
        self.selected_file = None
        self.drop_zone.reset()
        self.result_card.pack_forget()
        self.convert_btn.configure(state="disabled", text="Çevir  →")

    def _start_conversion(self):
        if not self.selected_file or self.is_processing:
            return

        # Soruşaq faylı hara yadda saxlayaq
        ext = os.path.splitext(self.selected_file)[1].lower()
        default_name = os.path.basename(self.selected_file).replace(ext, f"_latin{ext}")
        
        save_path = filedialog.asksaveasfilename(
            title="Sənədi yadda saxla",
            initialfile=default_name,
            defaultextension=ext,
            filetypes=[(f"{ext.upper()} Faylı", f"*{ext}")]
        )

        if not save_path:
            return  # İstifadəçi ləğv etdi

        self.save_path = save_path

        self.is_processing = True
        self.result_card.pack_forget()
        self.convert_btn.configure(state="disabled", text="Emal edilir...")

        self.progress_frame.pack(fill="x", padx=32, pady=(16, 0))
        self.progress_bar.start()

        threading.Thread(target=self._run_conversion, daemon=True).start()

    def _run_conversion(self):
        try:
            ext = os.path.splitext(self.selected_file)[1].lower()
            if ext == ".docx":
                replace_q = self.replace_quotes_var.get()
                out = process_docx(self.selected_file, self.save_path, replace_q)
            else:
                raise ValueError(f"Dəstəklənməyən format: {ext} (Yalnız DOCX)")
            self.after(0, self._on_success, out)
        except Exception as exc:
            self.after(0, self._on_error, str(exc))


    def _on_success(self, output_path: str):
        self.is_processing = False
        self.current_output = output_path
        self.progress_bar.stop()
        self.progress_frame.pack_forget()

        self.convert_btn.configure(state="normal", text="Yenidən Çevir  →")

        # Update result card
        self.result_path_label.configure(text=output_path)
        self.result_title.configure(text="Uğurla tamamlandı!", text_color=SUCCESS)
        # Re-configure icon to success
        for w in self.result_card.winfo_children():
            if isinstance(w, ctk.CTkLabel) and w.cget("text") == "❌":
                w.configure(text="✅")
                break

        self.result_card.pack(fill="x", padx=32, pady=(16, 0))
        self.open_btn.pack(pady=(0, 20))

        messagebox.showinfo("Uğurlu", f"Fayl uğurla çevrildi:\n{output_path}")

    def _on_error(self, msg: str):
        self.is_processing = False
        self.progress_bar.stop()
        self.progress_frame.pack_forget()

        self.convert_btn.configure(state="normal", text="Yenidən Çevir  →")
        messagebox.showerror("Xəta", f"Çevirmə zamanı xəta baş verdi:\n{msg}")

    def _open_folder(self):
        if self.current_output and os.path.exists(self.current_output):
            os.system(f'explorer /select,"{os.path.normpath(self.current_output)}"')


if __name__ == "__main__":
    app = App()
    app.mainloop()
