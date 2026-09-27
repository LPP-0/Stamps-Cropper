import customtkinter as ctk
from tkinter import messagebox

class AppUI:
    def __init__(self, master):
        self.master = master
        
        self.master.title("Recortador de Selos")
        self.master.geometry("800x750")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()

    def validate_number(self, text):
        return text == "" or text.isdigit()

    def show_help(self):
        ajuda_texto = (
            "Estas margens (medidas em píxeis) definem o espaço extra do fundo verde "
            "que é mantido em volta de cada selo.\n\n"
            "Podes aumentar estes valores se quiseres deixar mais espaço em branco, "
            "ou reduzir para cortar mais rente ao selo."
        )
        messagebox.showinfo("Ajuda - Margens de Recorte", ajuda_texto)

    def setup_ui(self):
        vcmd = (self.master.register(self.validate_number), '%P')

        self.main_container = ctk.CTkScrollableFrame(self.master, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.top_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_frame.pack(padx=20, pady=(10, 5), fill="x")

        # A caixa de destino agora ocupa a largura toda no topo
        self.dest_frame = ctk.CTkFrame(self.top_frame, height=40, fg_color=("gray85", "gray25"))
        self.dest_frame.pack(fill="x", expand=True)

        dest_inner = ctk.CTkFrame(self.dest_frame, fg_color="transparent")
        dest_inner.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.btn_select_folder = ctk.CTkButton(
            dest_inner, text="Mudar Destino", width=100, height=30,
            fg_color="gray75", text_color="black", hover_color="gray60",
            command=self.master.select_output_folder
        )
        self.btn_select_folder.pack(side="right", padx=(10, 0))

        self.lbl_folder_path = ctk.CTkLabel(
            dest_inner, text="Destino: Desktop/Resultados_Selos", 
            font=ctk.CTkFont(weight="bold"), anchor="w", justify="left", wraplength=500
        )
        self.lbl_folder_path.pack(side="left", fill="x", expand=True)

        self.btn_add_images = ctk.CTkButton(
            self.main_container, text="+ Adicionar (ou arrastar)", height=35,
            font=ctk.CTkFont(weight="bold", size=14),
            command=self.master.select_images
        )
        self.btn_add_images.pack(fill="x", padx=20, pady=(15, 0))

        self.preview_frame = ctk.CTkScrollableFrame(self.main_container, height=180)
        self.preview_frame.pack(fill="x", padx=20, pady=(5, 15))

        self.config_frame = ctk.CTkFrame(self.main_container)
        self.config_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(self.config_frame, text="Prefixo:").grid(row=0, column=0, padx=15, pady=8, sticky="w")
        self.entry_prefix = ctk.CTkEntry(self.config_frame, placeholder_text="Ex: GMY")
        self.entry_prefix.grid(row=0, column=1, padx=15, pady=8, sticky="ew")
        ctk.CTkButton(self.config_frame, text="Limpar", width=60, command=lambda: self.entry_prefix.delete(0, 'end')).grid(row=0, column=2, padx=(0, 15), pady=8)

        ctk.CTkLabel(self.config_frame, text="Contador:").grid(row=1, column=0, padx=15, pady=8, sticky="w")
        self.entry_counter = ctk.CTkEntry(self.config_frame, placeholder_text="Ex: 9632", validate="key", validatecommand=vcmd)
        self.entry_counter.grid(row=1, column=1, padx=15, pady=8, sticky="ew")
        ctk.CTkButton(self.config_frame, text="Limpar", width=60, command=lambda: self.entry_counter.delete(0, 'end')).grid(row=1, column=2, padx=(0, 15), pady=8)

        ctk.CTkLabel(self.config_frame, text="Sufixo:").grid(row=2, column=0, padx=15, pady=8, sticky="w")
        self.entry_suffix = ctk.CTkEntry(self.config_frame, placeholder_text="Ex: - ALEMANHA - USD")
        self.entry_suffix.grid(row=2, column=1, padx=15, pady=8, sticky="ew")
        ctk.CTkButton(self.config_frame, text="Limpar", width=60, command=lambda: self.entry_suffix.delete(0, 'end')).grid(row=2, column=2, padx=(0, 15), pady=8)

        self.config_frame.columnconfigure(1, weight=1)

        self.margin_frame = ctk.CTkFrame(self.main_container)
        self.margin_frame.pack(padx=20, pady=10, fill="x")
        
        header_frame = ctk.CTkFrame(self.margin_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=4, pady=(5, 10), sticky="ew")
        
        ctk.CTkLabel(header_frame, text="Ajuste de Margens (px):", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=15)
        ctk.CTkButton(header_frame, text="?", width=30, height=30, corner_radius=15, command=self.show_help).pack(side="right", padx=15)

        ctk.CTkLabel(self.margin_frame, text="Cima:").grid(row=1, column=0, padx=(15, 5), pady=5, sticky="e")
        self.pad_top = ctk.CTkEntry(self.margin_frame, width=60, validate="key", validatecommand=vcmd)
        self.pad_top.insert(0, "20")
        self.pad_top.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self.margin_frame, text="Baixo:").grid(row=1, column=2, padx=(15, 5), pady=5, sticky="e")
        self.pad_bottom = ctk.CTkEntry(self.margin_frame, width=60, validate="key", validatecommand=vcmd)
        self.pad_bottom.insert(0, "50")
        self.pad_bottom.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(self.margin_frame, text="Esq:").grid(row=2, column=0, padx=(15, 5), pady=(5, 15), sticky="e")
        self.pad_left = ctk.CTkEntry(self.margin_frame, width=60, validate="key", validatecommand=vcmd)
        self.pad_left.insert(0, "20")
        self.pad_left.grid(row=2, column=1, padx=5, pady=(5, 15), sticky="w")

        ctk.CTkLabel(self.margin_frame, text="Dir:").grid(row=2, column=2, padx=(15, 5), pady=(5, 15), sticky="e")
        self.pad_right = ctk.CTkEntry(self.margin_frame, width=60, validate="key", validatecommand=vcmd)
        self.pad_right.insert(0, "20")
        self.pad_right.grid(row=2, column=3, padx=5, pady=(5, 15), sticky="w")

        self.margin_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.btn_process = ctk.CTkButton(self.main_container, text="Recortar Selos", fg_color="green", 
                                         hover_color="darkgreen", height=40, font=ctk.CTkFont(weight="bold", size=14),
                                         command=self.master.run_processing)
        self.btn_process.pack(padx=20, pady=(10, 20), fill="x")