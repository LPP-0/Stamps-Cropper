import customtkinter as ctk
import os
import platform
import subprocess
from PIL import Image
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

from ui import AppUI
from drag_manager import DragManager
from processor import process_stamps

class TkinterDnDApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class AppController(TkinterDnDApp):
    def __init__(self):
        super().__init__()

        self.image_paths = []
        self.output_folder_path = ""
        
        # Inicia a UI
        self.ui = AppUI(self)
        
        # Inicia o Gestor de Eventos do Rato
        self.drag_manager = DragManager(self)

        # Regista o próprio botão azul
        self.ui.btn_add_images.drop_target_register(DND_FILES)
        self.ui.btn_add_images.dnd_bind('<<Drop>>', self.on_drop_images)

        # Regista a moldura exterior
        self.ui.preview_frame.drop_target_register(DND_FILES)
        self.ui.preview_frame.dnd_bind('<<Drop>>', self.on_drop_images)
        
        # Regista o canvas interno do ScrollableFrame
        self.ui.preview_frame._parent_canvas.drop_target_register(DND_FILES)
        self.ui.preview_frame._parent_canvas.dnd_bind('<<Drop>>', self.on_drop_images)

        self.refresh_preview()

    def on_drop_images(self, event):
        dropped_files = self.tk.splitlist(event.data)
        valid_extensions = ('.jpg', '.jpeg', '.png')
        
        added_new = False
        for file_path in dropped_files:
            if file_path.lower().endswith(valid_extensions):
                if file_path not in self.image_paths:
                    self.image_paths.append(file_path)
                    added_new = True
                    
        if added_new:
            self.refresh_preview()

    def select_images(self):
        file_types = [("Imagens", "*.jpg *.jpeg *.png")]
        paths = filedialog.askopenfilenames(title="Selecionar Imagens", filetypes=file_types)
        if paths:
            for p in paths:
                if p not in self.image_paths:
                    self.image_paths.append(p)
            self.refresh_preview()

    def select_output_folder(self):
        path = filedialog.askdirectory(title="Selecionar Pasta")
        if path:
            self.output_folder_path = path
            self.ui.lbl_folder_path.configure(text=f"Destino: {path}")

    def remove_image(self, index):
        self.image_paths.pop(index)
        self.refresh_preview()

    def refresh_preview(self):
        for widget in self.ui.preview_frame.winfo_children():
            widget.destroy()

        if not self.image_paths:
            lbl_empty = ctk.CTkLabel(
                self.ui.preview_frame, 
                text="A lista está vazia.\nArraste imagens para aqui.", 
                text_color=("gray50", "gray50"), 
                font=ctk.CTkFont(size=14)
            )
            lbl_empty.pack(expand=True, pady=40)
            
            lbl_empty.drop_target_register(DND_FILES)
            lbl_empty.dnd_bind('<<Drop>>', self.on_drop_images)
            return

        for i, path in enumerate(self.image_paths):
            row_frame = ctk.CTkFrame(
                self.ui.preview_frame, fg_color=("gray85", "gray20"), corner_radius=8,
                border_width=1, border_color=("gray70", "gray30"), cursor="fleur"
            )
            row_frame.pack(fill="x", pady=4, padx=5, ipady=3)
            
            try:
                img = Image.open(path)
                img.thumbnail((40, 40))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
                lbl_img = ctk.CTkLabel(row_frame, image=ctk_img, text="", cursor="fleur")
                lbl_img.pack(side="left", padx=10, pady=5)
            except:
                pass
            
            filename = os.path.basename(path)
            if len(filename) > 25:
                filename = filename[:22] + "..."
            
            lbl_name = ctk.CTkLabel(row_frame, text=filename, width=150, anchor="w", font=ctk.CTkFont(weight="bold"), cursor="fleur")
            lbl_name.pack(side="left", padx=10, fill="x", expand=True)
            
            lbl_drag = ctk.CTkLabel(row_frame, text="☰", font=ctk.CTkFont(size=18), text_color="gray", cursor="fleur")
            lbl_drag.pack(side="left", padx=10)
            
            btn_remove = ctk.CTkButton(row_frame, text="X", width=30, fg_color="#d9534f", hover_color="#c9302c", command=lambda idx=i: self.remove_image(idx))
            btn_remove.pack(side="left", padx=10)

            widgets_to_bind = [row_frame, lbl_img, lbl_name, lbl_drag]
            for w in widgets_to_bind:
                w.bind("<ButtonPress-1>", lambda e, idx=i, f=row_frame: self.drag_manager.on_drag_start(e, idx, f))
                w.bind("<B1-Motion>", self.drag_manager.on_drag_motion)
                w.bind("<ButtonRelease-1>", self.drag_manager.on_drag_release)

    def run_processing(self):
        if not self.image_paths:
            messagebox.showerror("Erro", "Tem de adicionar pelo menos uma imagem à lista.")
            return

        target_folder = self.output_folder_path
        if not target_folder:
            desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            target_folder = os.path.join(desktop, "Resultados_Selos")

        if not self.ui.entry_counter.get().strip():
            messagebox.showerror("Erro", "O Contador Inicial não pode estar vazio.")
            return

        prefix = self.ui.entry_prefix.get().strip()
        start_counter = int(self.ui.entry_counter.get().strip())
        suffix = self.ui.entry_suffix.get() 

        try:
            pt = int(self.ui.pad_top.get().strip()) if self.ui.pad_top.get().strip() else 20
            pb = int(self.ui.pad_bottom.get().strip()) if self.ui.pad_bottom.get().strip() else 50
            pl = int(self.ui.pad_left.get().strip()) if self.ui.pad_left.get().strip() else 20
            pr = int(self.ui.pad_right.get().strip()) if self.ui.pad_right.get().strip() else 20
        except ValueError:
            messagebox.showerror("Erro", "As margens têm de ser números inteiros.")
            return

        total_stamps = 0
        current_counter = start_counter

        try:
            for img_path in self.image_paths:
                processed_in_file, next_counter = process_stamps(
                    image_path=img_path,
                    output_folder=target_folder,
                    prefix=prefix,
                    start_counter=current_counter,
                    suffix=suffix,
                    pad_top=pt, pad_bottom=pb, pad_left=pl, pad_right=pr
                )
                total_stamps += processed_in_file
                current_counter = next_counter 
            
            messagebox.showinfo("Sucesso", f"{total_stamps} selos processados no total!\nGuardados em: {target_folder}")
            
            if platform.system() == "Windows":
                os.startfile(target_folder)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", target_folder])
            else:
                subprocess.Popen(["xdg-open", target_folder])
                
        except Exception as e:
            messagebox.showerror("Erro no Processamento", str(e))