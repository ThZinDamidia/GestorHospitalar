import tkinter as tk
from tkinter import ttk, messagebox, font
import re

# ─── Importações do sistema hospitalar ────────────────────────────────────────
from medico import (
    criar_medico, listar_medicos, consultar_medico,
    atualizar_medico, remover_medico, medico_existe
)
from paciente import (
    criar_paciente, listar_pacientes, consultar_paciente,
    atualizar_paciente, remover_paciente
)
from unidade import (
    criar_unidade, listar_unidades, consultar_unidade,
    atualizar_unidade, remover_unidade, unidade_existe
)
from consulta import (
    criar_consulta, listar_consultas, consultar_consulta,
    atualizar_consulta, cancelar_consulta, remover_consulta
)


# ══════════════════════════════════════════════════════════════════════════════
#  PALETA DE CORES & CONSTANTES VISUAIS
# ══════════════════════════════════════════════════════════════════════════════

COR = {
    "fundo":          "#0D1117",
    "painel":         "#161B22",
    "card":           "#1C2333",
    "card_hover":     "#21293D",
    "borda":          "#30363D",
    "borda_destaque": "#1F6FEB",
    "primario":       "#1F6FEB",
    "primario_hover": "#388BFD",
    "sucesso":        "#2EA043",
    "sucesso_hover":  "#3FB950",
    "perigo":         "#DA3633",
    "perigo_hover":   "#F85149",
    "aviso":          "#D29922",
    "texto":          "#E6EDF3",
    "texto_sec":      "#8B949E",
    "texto_dim":      "#484F58",
    "destaque":       "#58A6FF",
    "tag_azul_bg":    "#0D419D",
    "tag_verde_bg":   "#033A16",
    "tag_vermelho_bg":"#67060C",
    "input_bg":       "#010409",
    "sidebar_ativo":  "#21293D",
    "sidebar_hover":  "#1C2333",
}

FONTE_TITULO  = ("Georgia", 20, "bold")
FONTE_SECAO   = ("Georgia", 13, "bold")
FONTE_LABEL   = ("Courier New", 10)
FONTE_LABEL_B = ("Courier New", 10, "bold")
FONTE_INPUT   = ("Courier New", 11)
FONTE_BTN     = ("Courier New", 10, "bold")
FONTE_TABELA  = ("Courier New", 10)
FONTE_SMALL   = ("Courier New", 9)
FONTE_BADGE   = ("Courier New", 8, "bold")

PAD = {"padx": 10, "pady": 6}


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS DE UI
# ══════════════════════════════════════════════════════════════════════════════

def _entry(parent, var, placeholder="", largura=30, estado="normal"):
    """Campo de entrada estilizado com placeholder."""
    frame = tk.Frame(parent, bg=COR["borda"], padx=1, pady=1)
    e = tk.Entry(frame, textvariable=var, width=largura, font=FONTE_INPUT,
                 bg=COR["input_bg"], fg=COR["texto"], insertbackground=COR["destaque"],
                 relief="flat", state=estado, disabledbackground=COR["card"],
                 disabledforeground=COR["texto_sec"])
    e.pack(fill="x", padx=2, pady=2)

    if placeholder:
        if not var.get():
            e.insert(0, placeholder)
            e.config(fg=COR["texto_dim"])

        def _on_focus_in(ev):
            if e.get() == placeholder:
                e.delete(0, "end")
                e.config(fg=COR["texto"])

        def _on_focus_out(ev):
            if not e.get():
                e.insert(0, placeholder)
                e.config(fg=COR["texto_dim"])

        e.bind("<FocusIn>", _on_focus_in)
        e.bind("<FocusOut>", _on_focus_out)

    e.bind("<FocusIn>",  lambda ev: frame.config(bg=COR["borda_destaque"]), add="+")
    e.bind("<FocusOut>", lambda ev: frame.config(bg=COR["borda"]), add="+")
    return frame, e


def _combo(parent, var, valores, largura=28):
    """Combobox estilizado."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("H.TCombobox",
                    fieldbackground=COR["input_bg"],
                    background=COR["card"],
                    foreground=COR["texto"],
                    selectbackground=COR["primario"],
                    selectforeground=COR["texto"],
                    borderwidth=1,
                    relief="flat")
    cb = ttk.Combobox(parent, textvariable=var, values=valores,
                      width=largura, font=FONTE_INPUT, state="readonly",
                      style="H.TCombobox")
    return cb


def _btn(parent, texto, comando, cor="primario", largura=18):
    """Botão estilizado com hover."""
    cores = {
        "primario": (COR["primario"],       COR["primario_hover"]),
        "sucesso":  (COR["sucesso"],         COR["sucesso_hover"]),
        "perigo":   (COR["perigo"],          COR["perigo_hover"]),
        "aviso":    (COR["aviso"],           "#E3B341"),
        "neutro":   (COR["card_hover"],      COR["borda"]),
    }
    bg_n, bg_h = cores.get(cor, cores["primario"])

    b = tk.Button(parent, text=texto, command=comando, width=largura,
                  font=FONTE_BTN, bg=bg_n, fg=COR["texto"],
                  activebackground=bg_h, activeforeground=COR["texto"],
                  relief="flat", cursor="hand2", bd=0,
                  padx=8, pady=6)
    b.bind("<Enter>", lambda e: b.config(bg=bg_h))
    b.bind("<Leave>", lambda e: b.config(bg=bg_n))
    return b


def _label(parent, texto, fonte=None, cor=None, ancora="w"):
    return tk.Label(parent, text=texto,
                    font=fonte or FONTE_LABEL,
                    bg=COR["card"],
                    fg=cor or COR["texto_sec"],
                    anchor=ancora)


def _separador(parent):
    tk.Frame(parent, bg=COR["borda"], height=1).pack(fill="x", pady=8)


def _titulo_secao(parent, texto):
    f = tk.Frame(parent, bg=COR["card"])
    f.pack(fill="x", padx=18, pady=(14, 4))
    tk.Label(f, text=texto, font=FONTE_SECAO,
             bg=COR["card"], fg=COR["destaque"]).pack(side="left")
    tk.Frame(f, bg=COR["borda"], height=1).pack(side="left", fill="x", expand=True, padx=(10, 0), pady=6)


def _badge(parent, texto, cor_bg):
    return tk.Label(parent, text=texto, font=FONTE_BADGE,
                    bg=cor_bg, fg=COR["texto"],
                    padx=6, pady=2, relief="flat")


def _aviso(parent, mensagem, tipo="erro"):
    cores = {"erro": COR["perigo"], "ok": COR["sucesso"], "info": COR["primario"]}
    cor = cores.get(tipo, COR["aviso"])
    popup = tk.Toplevel(parent)
    popup.title("")
    popup.configure(bg=COR["painel"])
    popup.resizable(False, False)
    popup.grab_set()
    # Centrar
    popup.update_idletasks()
    x = parent.winfo_rootx() + parent.winfo_width() // 2 - 200
    y = parent.winfo_rooty() + parent.winfo_height() // 2 - 80
    popup.geometry(f"400x160+{x}+{y}")

    icones = {"erro": "✖", "ok": "✔", "info": "ℹ"}
    icone = icones.get(tipo, "⚠")

    tk.Frame(popup, bg=cor, width=5).pack(side="left", fill="y")
    corpo = tk.Frame(popup, bg=COR["painel"], padx=20, pady=20)
    corpo.pack(fill="both", expand=True)
    tk.Label(corpo, text=f"{icone}  {mensagem}", font=FONTE_INPUT,
             bg=COR["painel"], fg=COR["texto"], wraplength=340, justify="left").pack(anchor="w")
    tk.Frame(corpo, bg=COR["painel"], height=12).pack()
    _btn(corpo, "OK", popup.destroy, cor="neutro" if tipo == "info" else tipo, largura=10).pack(anchor="e")


def _confirmar(parent, mensagem, callback):
    popup = tk.Toplevel(parent)
    popup.title("Confirmar")
    popup.configure(bg=COR["painel"])
    popup.resizable(False, False)
    popup.grab_set()
    popup.update_idletasks()
    x = parent.winfo_rootx() + parent.winfo_width() // 2 - 210
    y = parent.winfo_rooty() + parent.winfo_height() // 2 - 75
    popup.geometry(f"420x150+{x}+{y}")

    tk.Frame(popup, bg=COR["aviso"], width=5).pack(side="left", fill="y")
    corpo = tk.Frame(popup, bg=COR["painel"], padx=20, pady=20)
    corpo.pack(fill="both", expand=True)
    tk.Label(corpo, text=f"⚠  {mensagem}", font=FONTE_INPUT,
             bg=COR["painel"], fg=COR["texto"], wraplength=350, justify="left").pack(anchor="w")
    tk.Frame(corpo, bg=COR["painel"], height=10).pack()
    botoes = tk.Frame(corpo, bg=COR["painel"])
    botoes.pack(anchor="e")

    def _sim():
        popup.destroy()
        callback()

    _btn(botoes, "Cancelar", popup.destroy, cor="neutro", largura=10).pack(side="left", padx=(0, 6))
    _btn(botoes, "Confirmar", _sim, cor="perigo", largura=10).pack(side="left")


# ══════════════════════════════════════════════════════════════════════════════
#  TABELA REUTILIZÁVEL
# ══════════════════════════════════════════════════════════════════════════════

def _criar_tabela(parent, colunas, alturas=None):
    """Cria Treeview estilizado. Retorna (frame, tree)."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("H.Treeview",
                    background=COR["card"],
                    foreground=COR["texto"],
                    fieldbackground=COR["card"],
                    rowheight=28,
                    font=FONTE_TABELA,
                    borderwidth=0)
    style.configure("H.Treeview.Heading",
                    background=COR["painel"],
                    foreground=COR["destaque"],
                    font=FONTE_LABEL_B,
                    relief="flat",
                    borderwidth=0)
    style.map("H.Treeview",
              background=[("selected", COR["primario"])],
              foreground=[("selected", COR["texto"])])
    style.map("H.Treeview.Heading",
              background=[("active", COR["borda"])])

    frame = tk.Frame(parent, bg=COR["borda"], padx=1, pady=1)
    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(frame, columns=colunas, show="headings",
                        yscrollcommand=vsb.set, xscrollcommand=hsb.set,
                        style="H.Treeview",
                        height=alturas or 12)

    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", minwidth=60, width=130)

    # Zebra stripes
    tree.tag_configure("par",   background=COR["card"])
    tree.tag_configure("impar", background=COR["painel"])

    return frame, tree


def _preencher_tabela(tree, linhas):
    """Limpa e preenche tabela. linhas = lista de tuplos."""
    tree.delete(*tree.get_children())
    for i, linha in enumerate(linhas):
        tag = "par" if i % 2 == 0 else "impar"
        tree.insert("", "end", values=linha, tags=(tag,))


# ══════════════════════════════════════════════════════════════════════════════
#  SECÇÃO: UNIDADES
# ══════════════════════════════════════════════════════════════════════════════

TIPOS_UNIDADE = ["Hospital Regional", "Centro de Saude", "Clinica"]

def _frame_unidade(notebook):
    frame = tk.Frame(notebook, bg=COR["card"])

    # ── Cabeçalho ──
    cab = tk.Frame(frame, bg=COR["card"], padx=18, pady=14)
    cab.pack(fill="x")
    tk.Label(cab, text="🏥  Unidades de Saúde", font=FONTE_TITULO,
             bg=COR["card"], fg=COR["texto"]).pack(side="left")

    # ── Painel principal (esquerdo: form | direito: tabela) ──
    corpo = tk.Frame(frame, bg=COR["card"])
    corpo.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    # ────── FORMULÁRIO ──────
    form_outer = tk.Frame(corpo, bg=COR["painel"], padx=2, pady=2)
    form_outer.pack(side="left", fill="y", padx=(0, 14))

    form = tk.Frame(form_outer, bg=COR["card"], padx=18, pady=14)
    form.pack(fill="both", expand=True)

    # Variáveis
    v_nome     = tk.StringVar()
    v_local    = tk.StringVar()
    v_tipo     = tk.StringVar()
    v_cap      = tk.StringVar()
    v_id_sel   = tk.StringVar()   # ID seleccionado na tabela

    def _limpar():
        v_nome.set(""); v_local.set(""); v_tipo.set(""); v_cap.set("")
        v_id_sel.set("")
        lbl_sel.config(text="— nenhuma selecionada —", fg=COR["texto_dim"])

    _titulo_secao(form, "Nova Unidade / Editar")

    rows = [
        ("Nome",           v_nome,  "ex: Hospital Central"),
        ("Localização",    v_local, "ex: Lisboa"),
        ("Capacidade Máx.",v_cap,   "nº de médicos"),
    ]
    entradas = {}
    for label_txt, var, ph in rows:
        tk.Label(form, text=label_txt, font=FONTE_LABEL_B,
                 bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(6, 1))
        fr, e = _entry(form, var, ph)
        fr.pack(fill="x")
        entradas[label_txt] = e

    tk.Label(form, text="Tipo", font=FONTE_LABEL_B,
             bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(6, 1))
    cb_tipo = _combo(form, v_tipo, TIPOS_UNIDADE)
    cb_tipo.pack(fill="x")

    tk.Frame(form, bg=COR["card"], height=10).pack()

    # Label ID selecionado
    lbl_sel = tk.Label(form, text="— nenhuma selecionada —",
                       font=FONTE_SMALL, bg=COR["card"], fg=COR["texto_dim"])
    lbl_sel.pack(anchor="w", pady=(2, 8))

    # ── Validação ──
    def _validar():
        if not v_nome.get().strip():
            _aviso(frame, "O campo Nome é obrigatório."); return False
        if not v_local.get().strip():
            _aviso(frame, "A Localização é obrigatória."); return False
        if not v_tipo.get():
            _aviso(frame, "Seleccione o Tipo de unidade."); return False
        try:
            c = int(v_cap.get())
            if c <= 0: raise ValueError
        except ValueError:
            _aviso(frame, "Capacidade deve ser um número inteiro positivo."); return False
        return True

    # ── CRUD ──
    def _criar():
        if not _validar(): return
        code, obj = criar_unidade(v_nome.get().strip(), v_local.get().strip(),
                                  v_tipo.get(), int(v_cap.get()))
        if code == 201:
            _aviso(frame, f"Unidade criada com ID {obj['id_unidade']}.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _atualizar():
        uid = v_id_sel.get()
        if not uid:
            _aviso(frame, "Seleccione uma unidade na tabela para editar."); return
        if not _validar(): return
        code, obj = atualizar_unidade(
            uid,
            v_nome.get().strip() or None,
            v_local.get().strip() or None,
            v_tipo.get() or None,
            int(v_cap.get()) if v_cap.get() else None,
        )
        if code == 200:
            _aviso(frame, f"Unidade {uid} atualizada.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _remover():
        uid = v_id_sel.get()
        if not uid:
            _aviso(frame, "Seleccione uma unidade na tabela para remover."); return
        _confirmar(frame, f"Remover a unidade {uid}? Esta acção é irreversível.",
                   lambda: _fazer_remover(uid))

    def _fazer_remover(uid):
        code, obj = remover_unidade(uid)
        if code == 200:
            _aviso(frame, f"Unidade '{obj}' removida.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    # Botões
    btn_frame = tk.Frame(form, bg=COR["card"])
    btn_frame.pack(fill="x", pady=(4, 0))
    _btn(btn_frame, "＋ Criar",   _criar,     "sucesso", 12).pack(side="left", padx=(0, 4))
    _btn(btn_frame, "✎ Atualizar",_atualizar, "primario", 12).pack(side="left", padx=(0, 4))
    _btn(btn_frame, "✖ Remover",  _remover,   "perigo",  12).pack(side="left")

    tk.Frame(form, bg=COR["card"], height=6).pack()
    _btn(form, "⟳ Limpar campos", _limpar, "neutro", 22).pack()

    # ────── TABELA ──────
    tabela_frame = tk.Frame(corpo, bg=COR["card"])
    tabela_frame.pack(side="left", fill="both", expand=True)

    _titulo_secao(tabela_frame, "Unidades Registadas")

    colunas = ["ID", "Nome", "Tipo", "Localização", "Médicos", "Capacidade"]
    tbl_frame, tree = _criar_tabela(tabela_frame, colunas)
    tbl_frame.pack(fill="both", expand=True)

    # Pesquisa
    pesq_frame = tk.Frame(tabela_frame, bg=COR["card"])
    pesq_frame.pack(fill="x", pady=(6, 0))
    tk.Label(pesq_frame, text="🔍 Pesquisar:", font=FONTE_LABEL,
             bg=COR["card"], fg=COR["texto_sec"]).pack(side="left")
    v_pesq = tk.StringVar()
    _, e_pesq = _entry(pesq_frame, v_pesq, "Nome ou ID...")
    e_pesq.pack = lambda **kw: None  # já foi packed no _entry frame
    pesq_frame.children["!frame"].pack(side="left", padx=6)
    v_pesq.trace_add("write", lambda *a: _listar())

    def _listar():
        code, obj = listar_unidades()
        if code != 200:
            _preencher_tabela(tree, [])
            return
        filtro = v_pesq.get().lower().strip()
        linhas = []
        for uid, d in obj.items():
            if filtro and filtro not in uid.lower() and filtro not in d["nome"].lower():
                continue
            linhas.append((uid, d["nome"], d["tipo"], d["localizacao"],
                           d["medicos_vinculados"], d["capacidade_maxima"]))
        _preencher_tabela(tree, linhas)

    def _on_select(ev):
        sel = tree.selection()
        if not sel: return
        vals = tree.item(sel[0], "values")
        uid = vals[0]
        code, obj = consultar_unidade(uid)
        if code != 200: return
        v_id_sel.set(uid)
        v_nome.set(obj["nome"])
        v_local.set(obj["localizacao"])
        v_tipo.set(obj["tipo"])
        v_cap.set(str(obj["capacidade_maxima"]))
        lbl_sel.config(text=f"A editar: {uid} — {obj['nome']}", fg=COR["destaque"])

    tree.bind("<<TreeviewSelect>>", _on_select)
    _btn(tabela_frame, "⟳ Atualizar lista", _listar, "neutro", 20).pack(pady=(6, 0))
    _listar()

    return frame


# ══════════════════════════════════════════════════════════════════════════════
#  SECÇÃO: MÉDICOS
# ══════════════════════════════════════════════════════════════════════════════

def _frame_medico(notebook):
    frame = tk.Frame(notebook, bg=COR["card"])

    cab = tk.Frame(frame, bg=COR["card"], padx=18, pady=14)
    cab.pack(fill="x")
    tk.Label(cab, text="👨‍⚕️  Médicos", font=FONTE_TITULO,
             bg=COR["card"], fg=COR["texto"]).pack(side="left")

    corpo = tk.Frame(frame, bg=COR["card"])
    corpo.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    # ── FORMULÁRIO ──
    form_outer = tk.Frame(corpo, bg=COR["painel"], padx=2, pady=2)
    form_outer.pack(side="left", fill="y", padx=(0, 14))
    form = tk.Frame(form_outer, bg=COR["card"], padx=18, pady=14)
    form.pack(fill="both", expand=True)

    v_nome     = tk.StringVar()
    v_nasc     = tk.StringVar()
    v_nac      = tk.StringVar()
    v_espec    = tk.StringVar()
    v_registo  = tk.StringVar()
    v_idiomas  = tk.StringVar()
    v_pforte   = tk.StringVar()
    v_pfraco   = tk.StringVar()
    v_unidade  = tk.StringVar()
    v_horario  = tk.StringVar()
    v_cargo    = tk.StringVar()
    v_id_sel   = tk.StringVar()

    def _limpar():
        for v in [v_nome, v_nasc, v_nac, v_espec, v_registo,
                  v_idiomas, v_pforte, v_pfraco, v_unidade, v_horario, v_cargo]:
            v.set("")
        v_id_sel.set("")
        lbl_sel.config(text="— nenhum selecionado —", fg=COR["texto_dim"])

    _titulo_secao(form, "Novo Médico / Editar")

    campos = [
        ("Nome completo",    v_nome,    "ex: Ana Costa"),
        ("Data Nascimento",  v_nasc,    "YYYY-MM-DD"),
        ("Nacionalidade",    v_nac,     "ex: Portuguesa"),
        ("Especialidade",    v_espec,   "ex: Cardiologia"),
        ("Data Registo",     v_registo, "YYYY-MM-DD"),
        ("Idiomas",          v_idiomas, "ex: PT, EN"),
        ("Ponto Forte",      v_pforte,  "ex: Diagnóstico"),
        ("Ponto Fraco",      v_pfraco,  "ex: Pós-operatório"),
        ("ID Unidade",       v_unidade, "ex: U001"),
        ("Horário de Turno", v_horario, "ex: 08:00-16:00"),
        ("Cargo",            v_cargo,   "ex: Especialista"),
    ]
    for label_txt, var, ph in campos:
        tk.Label(form, text=label_txt, font=FONTE_LABEL_B,
                 bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(4, 1))
        fr, _ = _entry(form, var, ph)
        fr.pack(fill="x")

    tk.Frame(form, bg=COR["card"], height=8).pack()
    lbl_sel = tk.Label(form, text="— nenhum selecionado —",
                       font=FONTE_SMALL, bg=COR["card"], fg=COR["texto_dim"])
    lbl_sel.pack(anchor="w", pady=(0, 6))

    def _validar():
        import re as _re
        if not v_nome.get().strip():
            _aviso(frame, "Nome obrigatório."); return False
        for v, label in [(v_nasc, "Data de Nascimento"), (v_registo, "Data de Registo")]:
            if not _re.match(r"^\d{4}-\d{2}-\d{2}$", v.get().strip()):
                _aviso(frame, f"{label} inválida. Use YYYY-MM-DD."); return False
        if not v_unidade.get().strip():
            _aviso(frame, "ID da Unidade obrigatório."); return False
        uid = v_unidade.get().strip().upper()
        if not unidade_existe(uid):
            _aviso(frame, f"Unidade '{uid}' não encontrada. Registe a unidade primeiro."); return False
        return True

    def _criar():
        if not _validar(): return
        code, obj = criar_medico(
            v_nome.get().strip(), v_nasc.get().strip(), v_nac.get().strip(),
            v_espec.get().strip(), v_registo.get().strip(), v_idiomas.get().strip(),
            v_pforte.get().strip(), v_pfraco.get().strip(),
            v_unidade.get().strip().upper(), v_horario.get().strip(), v_cargo.get().strip()
        )
        if code == 201:
            _aviso(frame, f"Médico criado com ID {obj['id_medico']}.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _atualizar():
        mid = v_id_sel.get()
        if not mid:
            _aviso(frame, "Seleccione um médico na tabela."); return
        uid = v_unidade.get().strip().upper() if v_unidade.get().strip() else None
        if uid and not unidade_existe(uid):
            _aviso(frame, f"Unidade '{uid}' não encontrada."); return
        code, obj = atualizar_medico(
            mid,
            v_nome.get().strip() or None, v_nasc.get().strip() or None,
            v_nac.get().strip() or None, v_espec.get().strip() or None,
            v_registo.get().strip() or None, v_idiomas.get().strip() or None,
            v_pforte.get().strip() or None, v_pfraco.get().strip() or None,
            uid, v_horario.get().strip() or None, v_cargo.get().strip() or None
        )
        if code == 200:
            _aviso(frame, f"Médico {mid} atualizado.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _remover():
        mid = v_id_sel.get()
        if not mid:
            _aviso(frame, "Seleccione um médico na tabela."); return
        _confirmar(frame, f"Remover o médico {mid}?",
                   lambda: _fazer_remover(mid))

    def _fazer_remover(mid):
        code, obj = remover_medico(mid)
        if code == 200:
            _aviso(frame, f"Médico '{obj}' removido.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    btn_frame = tk.Frame(form, bg=COR["card"])
    btn_frame.pack(fill="x", pady=(4, 0))
    _btn(btn_frame, "＋ Criar",    _criar,     "sucesso", 12).pack(side="left", padx=(0, 4))
    _btn(btn_frame, "✎ Atualizar", _atualizar, "primario", 12).pack(side="left", padx=(0, 4))
    _btn(btn_frame, "✖ Remover",   _remover,   "perigo",  12).pack(side="left")
    tk.Frame(form, bg=COR["card"], height=4).pack()
    _btn(form, "⟳ Limpar campos", _limpar, "neutro", 22).pack()

    # ── TABELA ──
    tabela_frame = tk.Frame(corpo, bg=COR["card"])
    tabela_frame.pack(side="left", fill="both", expand=True)

    _titulo_secao(tabela_frame, "Médicos Registados")

    colunas = ["ID", "Nome", "Especialidade", "Cargo", "Unidade", "Horário"]
    tbl_frame, tree = _criar_tabela(tabela_frame, colunas)
    tbl_frame.pack(fill="both", expand=True)

    pesq_frame = tk.Frame(tabela_frame, bg=COR["card"])
    pesq_frame.pack(fill="x", pady=(6, 0))
    tk.Label(pesq_frame, text="🔍 Pesquisar:", font=FONTE_LABEL,
             bg=COR["card"], fg=COR["texto_sec"]).pack(side="left")
    v_pesq = tk.StringVar()
    _, _ = _entry(pesq_frame, v_pesq, "Nome, ID ou especialidade...")
    pesq_frame.children["!frame"].pack(side="left", padx=6)
    v_pesq.trace_add("write", lambda *a: _listar())

    def _listar():
        code, obj = listar_medicos()
        if code != 200:
            _preencher_tabela(tree, []); return
        filtro = v_pesq.get().lower().strip()
        linhas = []
        for mid, d in obj.items():
            if filtro and not any(filtro in str(v).lower()
                                  for v in [mid, d["nome"], d["especialidade"], d["cargo"]]):
                continue
            linhas.append((mid, d["nome"], d["especialidade"],
                           d["cargo"], d["id_unidade"], d["horario_turno"]))
        _preencher_tabela(tree, linhas)

    def _on_select(ev):
        sel = tree.selection()
        if not sel: return
        mid = tree.item(sel[0], "values")[0]
        code, obj = consultar_medico(mid)
        if code != 200: return
        v_id_sel.set(mid)
        v_nome.set(obj.get("nome", ""))
        v_nasc.set(obj.get("data_nascimento", ""))
        v_nac.set(obj.get("nacionalidade", ""))
        v_espec.set(obj.get("especialidade", ""))
        v_registo.set(obj.get("data_registo", ""))
        v_idiomas.set(obj.get("idiomas", ""))
        v_pforte.set(obj.get("ponto_forte", ""))
        v_pfraco.set(obj.get("ponto_fraco", ""))
        v_unidade.set(obj.get("id_unidade", ""))
        v_horario.set(obj.get("horario_turno", ""))
        v_cargo.set(obj.get("cargo", ""))
        lbl_sel.config(text=f"A editar: {mid} — {obj['nome']}", fg=COR["destaque"])

    tree.bind("<<TreeviewSelect>>", _on_select)
    _btn(tabela_frame, "⟳ Atualizar lista", _listar, "neutro", 20).pack(pady=(6, 0))
    _listar()

    return frame


# ══════════════════════════════════════════════════════════════════════════════
#  SECÇÃO: PACIENTES
# ══════════════════════════════════════════════════════════════════════════════

def _frame_paciente(notebook):
    frame = tk.Frame(notebook, bg=COR["card"])

    cab = tk.Frame(frame, bg=COR["card"], padx=18, pady=14)
    cab.pack(fill="x")
    tk.Label(cab, text="🧑‍🤝‍🧑  Pacientes", font=FONTE_TITULO,
             bg=COR["card"], fg=COR["texto"]).pack(side="left")

    corpo = tk.Frame(frame, bg=COR["card"])
    corpo.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    # ── FORMULÁRIO ──
    form_outer = tk.Frame(corpo, bg=COR["painel"], padx=2, pady=2)
    form_outer.pack(side="left", fill="y", padx=(0, 14))
    form = tk.Frame(form_outer, bg=COR["card"], padx=18, pady=14)
    form.pack(fill="both", expand=True)

    v_nome    = tk.StringVar()
    v_nasc    = tk.StringVar()
    v_nac     = tk.StringVar()
    v_sangue  = tk.StringVar()
    v_alerg   = tk.StringVar()
    v_doencas = tk.StringVar()
    v_cirurg  = tk.StringVar()
    v_medico  = tk.StringVar()
    v_nif_sel = tk.StringVar()   # NIF int do paciente selecionado

    def _limpar():
        for v in [v_nome, v_nasc, v_nac, v_sangue, v_alerg, v_doencas, v_cirurg, v_medico]:
            v.set("")
        v_nif_sel.set("")
        lbl_sel.config(text="— nenhum selecionado —", fg=COR["texto_dim"])
        lbl_nif.config(text="NIF gerado automaticamente", fg=COR["texto_dim"])

    TIPOS_SANGUE = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

    _titulo_secao(form, "Novo Paciente / Editar")

    campos_pac = [
        ("Nome completo",      v_nome,    "ex: João Silva"),
        ("Data Nascimento",    v_nasc,    "YYYY-MM-DD"),
        ("Nacionalidade",      v_nac,     "ex: Portuguesa"),
        ("Alergias",           v_alerg,   "ex: Penicilina"),
        ("Doenças Crónicas",   v_doencas, "ex: Diabetes"),
        ("Cirurgias Anteriores", v_cirurg,"ex: Apendicite 2010"),
        ("Médico Responsável", v_medico,  "ex: M001"),
    ]
    for label_txt, var, ph in campos_pac:
        tk.Label(form, text=label_txt, font=FONTE_LABEL_B,
                 bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(4, 1))
        fr, _ = _entry(form, var, ph)
        fr.pack(fill="x")

    tk.Label(form, text="Tipo Sanguíneo", font=FONTE_LABEL_B,
             bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(4, 1))
    cb_sangue = _combo(form, v_sangue, TIPOS_SANGUE, 12)
    cb_sangue.pack(anchor="w")

    tk.Frame(form, bg=COR["card"], height=8).pack()
    lbl_nif = tk.Label(form, text="NIF gerado automaticamente",
                       font=FONTE_SMALL, bg=COR["card"], fg=COR["texto_dim"])
    lbl_nif.pack(anchor="w")
    lbl_sel = tk.Label(form, text="— nenhum selecionado —",
                       font=FONTE_SMALL, bg=COR["card"], fg=COR["texto_dim"])
    lbl_sel.pack(anchor="w", pady=(2, 6))

    def _validar():
        import re as _re
        if not v_nome.get().strip():
            _aviso(frame, "Nome obrigatório."); return False
        if not _re.match(r"^\d{4}-\d{2}-\d{2}$", v_nasc.get().strip()):
            _aviso(frame, "Data de Nascimento inválida. Use YYYY-MM-DD."); return False
        if not v_sangue.get():
            _aviso(frame, "Seleccione o Tipo Sanguíneo."); return False
        med = v_medico.get().strip().upper()
        if not med:
            _aviso(frame, "ID do Médico Responsável é obrigatório."); return False
        if not medico_existe(med):
            _aviso(frame, f"Médico '{med}' não encontrado. Registe o médico primeiro."); return False
        return True

    def _criar():
        if not _validar(): return
        code, obj = criar_paciente(
            v_nome.get().strip(), v_nasc.get().strip(), v_nac.get().strip(),
            v_sangue.get(), v_alerg.get().strip(), v_doencas.get().strip(),
            v_cirurg.get().strip(), v_medico.get().strip().upper()
        )
        if code == 201:
            _aviso(frame, f"Paciente criado. NIF: {obj['nif']}", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _atualizar():
        nif_str = v_nif_sel.get()
        if not nif_str:
            _aviso(frame, "Seleccione um paciente na tabela."); return
        try:
            nif = int(nif_str)
        except ValueError:
            _aviso(frame, "NIF inválido."); return
        med = v_medico.get().strip().upper() if v_medico.get().strip() else None
        if med and not medico_existe(med):
            _aviso(frame, f"Médico '{med}' não encontrado."); return
        code, obj = atualizar_paciente(
            nif,
            v_nome.get().strip() or None, v_nasc.get().strip() or None,
            v_nac.get().strip() or None, v_sangue.get() or None,
            v_alerg.get().strip() or None, v_doencas.get().strip() or None,
            v_cirurg.get().strip() or None, med
        )
        if code == 200:
            _aviso(frame, f"Paciente NIF {nif} atualizado.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _remover():
        nif_str = v_nif_sel.get()
        if not nif_str:
            _aviso(frame, "Seleccione um paciente na tabela."); return
        _confirmar(frame, f"Remover paciente NIF {nif_str}?",
                   lambda: _fazer_remover(int(nif_str)))

    def _fazer_remover(nif):
        code, obj = remover_paciente(nif)
        if code == 200:
            _aviso(frame, f"Paciente '{obj}' removido.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    btn_frame = tk.Frame(form, bg=COR["card"])
    btn_frame.pack(fill="x", pady=(4, 0))
    _btn(btn_frame, "＋ Criar",    _criar,     "sucesso", 12).pack(side="left", padx=(0, 4))
    _btn(btn_frame, "✎ Atualizar", _atualizar, "primario", 12).pack(side="left", padx=(0, 4))
    _btn(btn_frame, "✖ Remover",   _remover,   "perigo",  12).pack(side="left")
    tk.Frame(form, bg=COR["card"], height=4).pack()
    _btn(form, "⟳ Limpar campos", _limpar, "neutro", 22).pack()

    # ── TABELA ──
    tabela_frame = tk.Frame(corpo, bg=COR["card"])
    tabela_frame.pack(side="left", fill="both", expand=True)
    _titulo_secao(tabela_frame, "Pacientes Registados")
    colunas = ["NIF", "Nome", "Tipo Sanguíneo", "Médico", "Data Nasc.", "Nacionalidade"]
    tbl_frame, tree = _criar_tabela(tabela_frame, colunas)
    tbl_frame.pack(fill="both", expand=True)

    pesq_frame = tk.Frame(tabela_frame, bg=COR["card"])
    pesq_frame.pack(fill="x", pady=(6, 0))
    tk.Label(pesq_frame, text="🔍 Pesquisar:", font=FONTE_LABEL,
             bg=COR["card"], fg=COR["texto_sec"]).pack(side="left")
    v_pesq = tk.StringVar()
    _, _ = _entry(pesq_frame, v_pesq, "Nome ou NIF...")
    pesq_frame.children["!frame"].pack(side="left", padx=6)
    v_pesq.trace_add("write", lambda *a: _listar())

    def _listar():
        code, obj = listar_pacientes()
        if code != 200:
            _preencher_tabela(tree, []); return
        filtro = v_pesq.get().lower().strip()
        linhas = []
        for nif, d in obj.items():
            if filtro and filtro not in str(nif) and filtro not in d["nome"].lower():
                continue
            linhas.append((nif, d["nome"], d["tipo_sanguineo"],
                           d["id_medico"], d.get("data_nascimento", ""), d.get("nacionalidade", "")))
        _preencher_tabela(tree, linhas)

    def _on_select(ev):
        sel = tree.selection()
        if not sel: return
        nif_str = str(tree.item(sel[0], "values")[0])
        try:
            nif = int(nif_str)
        except ValueError:
            return
        code, obj = consultar_paciente(nif)
        if code != 200: return
        v_nif_sel.set(str(nif))
        v_nome.set(obj.get("nome", ""))
        v_nasc.set(obj.get("data_nascimento", ""))
        v_nac.set(obj.get("nacionalidade", ""))
        v_sangue.set(obj.get("tipo_sanguineo", ""))
        v_alerg.set(obj.get("alergias", ""))
        v_doencas.set(obj.get("doencas_cronicas", ""))
        v_cirurg.set(obj.get("cirurgias_anteriores", ""))
        v_medico.set(obj.get("id_medico", ""))
        lbl_sel.config(text=f"A editar: NIF {nif} — {obj['nome']}", fg=COR["destaque"])
        lbl_nif.config(text=f"NIF: {nif}", fg=COR["aviso"])

    tree.bind("<<TreeviewSelect>>", _on_select)
    _btn(tabela_frame, "⟳ Atualizar lista", _listar, "neutro", 20).pack(pady=(6, 0))
    _listar()

    return frame


# ══════════════════════════════════════════════════════════════════════════════
#  SECÇÃO: CONSULTAS
# ══════════════════════════════════════════════════════════════════════════════

ESTADOS_CONSULTA = ["Agendada", "Realizada", "Cancelada"]

def _frame_consulta(notebook):
    frame = tk.Frame(notebook, bg=COR["card"])

    cab = tk.Frame(frame, bg=COR["card"], padx=18, pady=14)
    cab.pack(fill="x")
    tk.Label(cab, text="📋  Consultas", font=FONTE_TITULO,
             bg=COR["card"], fg=COR["texto"]).pack(side="left")

    corpo = tk.Frame(frame, bg=COR["card"])
    corpo.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    # ── FORMULÁRIO ──
    form_outer = tk.Frame(corpo, bg=COR["painel"], padx=2, pady=2)
    form_outer.pack(side="left", fill="y", padx=(0, 14))
    form = tk.Frame(form_outer, bg=COR["card"], padx=18, pady=14)
    form.pack(fill="both", expand=True)

    v_medico   = tk.StringVar()
    v_nif      = tk.StringVar()
    v_dt       = tk.StringVar()
    v_sintomas = tk.StringVar()
    v_obs      = tk.StringVar()
    v_estado   = tk.StringVar()
    v_id_sel   = tk.StringVar()

    def _limpar():
        for v in [v_medico, v_nif, v_dt, v_sintomas, v_obs, v_estado]:
            v.set("")
        v_id_sel.set("")
        lbl_sel.config(text="— nenhuma selecionada —", fg=COR["texto_dim"])

    _titulo_secao(form, "Nova Consulta / Editar")

    campos_con = [
        ("ID Médico",      v_medico,   "ex: M001"),
        ("NIF Paciente",   v_nif,      "ex: 123456789"),
        ("Data e Hora",    v_dt,       "YYYY-MM-DD HH:MM"),
        ("Sintomas",       v_sintomas, "Descrição dos sintomas"),
        ("Observações",    v_obs,      "Notas clínicas (opcional)"),
    ]
    for label_txt, var, ph in campos_con:
        tk.Label(form, text=label_txt, font=FONTE_LABEL_B,
                 bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(4, 1))
        fr, _ = _entry(form, var, ph)
        fr.pack(fill="x")

    tk.Label(form, text="Estado", font=FONTE_LABEL_B,
             bg=COR["card"], fg=COR["texto_sec"], anchor="w").pack(fill="x", pady=(4, 1))
    cb_estado = _combo(form, v_estado, ESTADOS_CONSULTA, 18)
    cb_estado.pack(anchor="w")

    tk.Frame(form, bg=COR["card"], height=8).pack()
    lbl_sel = tk.Label(form, text="— nenhuma selecionada —",
                       font=FONTE_SMALL, bg=COR["card"], fg=COR["texto_dim"])
    lbl_sel.pack(anchor="w", pady=(0, 6))

    def _validar_criar():
        import re as _re
        mid = v_medico.get().strip().upper()
        if not mid:
            _aviso(frame, "ID do Médico obrigatório."); return False
        if not medico_existe(mid):
            _aviso(frame, f"Médico '{mid}' não encontrado."); return False
        try:
            nif = int(v_nif.get().strip())
        except ValueError:
            _aviso(frame, "NIF do paciente deve ser numérico."); return False
        if not _re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", v_dt.get().strip()):
            _aviso(frame, "Data/hora inválida. Use YYYY-MM-DD HH:MM."); return False
        if not v_sintomas.get().strip():
            _aviso(frame, "Sintomas são obrigatórios."); return False
        return True

    def _criar():
        if not _validar_criar(): return
        try:
            nif = int(v_nif.get().strip())
        except ValueError:
            _aviso(frame, "NIF inválido."); return
        code, obj = criar_consulta(
            v_medico.get().strip().upper(), nif,
            v_dt.get().strip(), v_sintomas.get().strip(), v_obs.get().strip()
        )
        if code == 201:
            _aviso(frame, f"Consulta criada com ID {obj['id_consulta']}.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _atualizar():
        cid = v_id_sel.get()
        if not cid:
            _aviso(frame, "Seleccione uma consulta na tabela."); return
        estado = v_estado.get() if v_estado.get() else None
        code, obj = atualizar_consulta(
            cid,
            v_dt.get().strip() or None,
            v_sintomas.get().strip() or None,
            v_obs.get().strip() or None,
            estado
        )
        if code == 200:
            _aviso(frame, f"Consulta {cid} atualizada.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _cancelar():
        cid = v_id_sel.get()
        if not cid:
            _aviso(frame, "Seleccione uma consulta na tabela."); return
        _confirmar(frame, f"Cancelar a consulta {cid}?",
                   lambda: _fazer_cancelar(cid))

    def _fazer_cancelar(cid):
        code, obj = cancelar_consulta(cid)
        if code == 200:
            _aviso(frame, f"Consulta {cid} cancelada.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    def _remover():
        cid = v_id_sel.get()
        if not cid:
            _aviso(frame, "Seleccione uma consulta na tabela."); return
        _confirmar(frame, f"Remover permanentemente a consulta {cid}?",
                   lambda: _fazer_remover(cid))

    def _fazer_remover(cid):
        code, obj = remover_consulta(cid)
        if code == 200:
            _aviso(frame, f"Consulta {cid} removida.", "ok")
            _limpar(); _listar()
        else:
            _aviso(frame, f"Erro {code}: {obj}")

    btn_frame = tk.Frame(form, bg=COR["card"])
    btn_frame.pack(fill="x", pady=(4, 0))
    _btn(btn_frame, "＋ Criar",    _criar,     "sucesso",  10).pack(side="left", padx=(0, 3))
    _btn(btn_frame, "✎ Atualizar", _atualizar, "primario", 10).pack(side="left", padx=(0, 3))
    _btn(btn_frame, "⏸ Cancelar",  _cancelar,  "aviso",    10).pack(side="left", padx=(0, 3))
    _btn(btn_frame, "✖ Remover",   _remover,   "perigo",   10).pack(side="left")
    tk.Frame(form, bg=COR["card"], height=4).pack()
    _btn(form, "⟳ Limpar campos", _limpar, "neutro", 22).pack()

    # ── TABELA ──
    tabela_frame = tk.Frame(corpo, bg=COR["card"])
    tabela_frame.pack(side="left", fill="both", expand=True)
    _titulo_secao(tabela_frame, "Consultas Registadas")
    colunas = ["ID", "Data/Hora", "Médico", "NIF Paciente", "Estado", "Sintomas"]
    tbl_frame, tree = _criar_tabela(tabela_frame, colunas)
    tbl_frame.pack(fill="both", expand=True)

    # Filtros
    filtros_frame = tk.Frame(tabela_frame, bg=COR["card"])
    filtros_frame.pack(fill="x", pady=(6, 0))

    tk.Label(filtros_frame, text="🔍 Médico:", font=FONTE_LABEL,
             bg=COR["card"], fg=COR["texto_sec"]).pack(side="left")
    v_f_med = tk.StringVar()
    _, _ = _entry(filtros_frame, v_f_med, "ID...")
    filtros_frame.children["!frame"].pack(side="left", padx=(4, 12))

    tk.Label(filtros_frame, text="Estado:", font=FONTE_LABEL,
             bg=COR["card"], fg=COR["texto_sec"]).pack(side="left")
    v_f_est = tk.StringVar()
    cb_f_est = _combo(filtros_frame, v_f_est, ["", "Agendada", "Realizada", "Cancelada"], 12)
    cb_f_est.pack(side="left", padx=4)

    v_f_med.trace_add("write", lambda *a: _listar())
    v_f_est.trace_add("write", lambda *a: _listar())

    def _listar():
        f_med = v_f_med.get().strip().upper() or None
        f_est = v_f_est.get().strip() or None
        code, obj = listar_consultas(f_med, None, f_est)
        if code != 200:
            _preencher_tabela(tree, []); return
        linhas = [(cid, d["data_hora"], d["id_medico"], d["id_paciente"],
                   d["estado"], d["sintomas"][:40]) for cid, d in obj.items()]
        _preencher_tabela(tree, linhas)

    def _on_select(ev):
        sel = tree.selection()
        if not sel: return
        cid = tree.item(sel[0], "values")[0]
        code, obj = consultar_consulta(cid)
        if code != 200: return
        v_id_sel.set(cid)
        v_medico.set(obj.get("id_medico", ""))
        v_nif.set(str(obj.get("id_paciente", "")))
        v_dt.set(obj.get("data_hora", ""))
        v_sintomas.set(obj.get("sintomas", ""))
        v_obs.set(obj.get("observacoes", ""))
        v_estado.set(obj.get("estado", ""))
        lbl_sel.config(text=f"A editar: {cid}", fg=COR["destaque"])

    tree.bind("<<TreeviewSelect>>", _on_select)
    _btn(tabela_frame, "⟳ Atualizar lista", _listar, "neutro", 20).pack(pady=(6, 0))
    _listar()

    return frame


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def _frame_dashboard(notebook, tab_ctrl):
    frame = tk.Frame(notebook, bg=COR["card"])

    cab = tk.Frame(frame, bg=COR["card"], padx=24, pady=20)
    cab.pack(fill="x")
    tk.Label(cab, text="Sistema de Gestão Hospitalar", font=FONTE_TITULO,
             bg=COR["card"], fg=COR["texto"]).pack(side="left")
    tk.Label(cab, text="Dashboard", font=("Courier New", 11),
             bg=COR["card"], fg=COR["texto_sec"]).pack(side="left", padx=(14, 0), pady=(6, 0))

    _separador(frame)

    # ── Cards de estatísticas ──
    stats_frame = tk.Frame(frame, bg=COR["card"], padx=24)
    stats_frame.pack(fill="x", pady=(4, 16))

    def _stat_card(parent, titulo, valor_fn, icone, cor_acc):
        card = tk.Frame(parent, bg=COR["painel"], padx=20, pady=14,
                        relief="flat", bd=0)
        card.pack(side="left", padx=(0, 14), pady=4, fill="y")
        tk.Label(card, text=icone, font=("Segoe UI Emoji", 22),
                 bg=COR["painel"], fg=cor_acc).grid(row=0, column=0, rowspan=2, padx=(0, 14))
        lbl_v = tk.Label(card, text="—", font=("Georgia", 26, "bold"),
                         bg=COR["painel"], fg=cor_acc)
        lbl_v.grid(row=0, column=1, sticky="w")
        tk.Label(card, text=titulo, font=FONTE_SMALL,
                 bg=COR["painel"], fg=COR["texto_sec"]).grid(row=1, column=1, sticky="w")
        return lbl_v, valor_fn

    lbls = []
    lbls.append(_stat_card(stats_frame, "Unidades",  lambda: len(listar_unidades()[1]) if listar_unidades()[0] == 200 else 0,  "🏥", COR["destaque"]))
    lbls.append(_stat_card(stats_frame, "Médicos",   lambda: len(listar_medicos()[1]) if listar_medicos()[0] == 200 else 0,    "👨‍⚕️", COR["sucesso"]))
    lbls.append(_stat_card(stats_frame, "Pacientes", lambda: len(listar_pacientes()[1]) if listar_pacientes()[0] == 200 else 0,"🧑‍🤝‍🧑", COR["aviso"]))
    lbls.append(_stat_card(stats_frame, "Consultas", lambda: len(listar_consultas()[1]) if listar_consultas()[0] == 200 else 0,"📋", COR["primario"]))

    def _refresh_stats():
        for lbl, fn in lbls:
            lbl.config(text=str(fn()))

    _refresh_stats()

    _separador(frame)

    # ── Atalhos rápidos ──
    _titulo_secao(frame, "Acesso Rápido")
    atalhos = tk.Frame(frame, bg=COR["card"], padx=24)
    atalhos.pack(fill="x", pady=8)

    acoes = [
        ("🏥  Gerir Unidades",  1, "primario"),
        ("👨‍⚕️  Gerir Médicos",   2, "sucesso"),
        ("🧑  Gerir Pacientes", 3, "aviso"),
        ("📋  Gerir Consultas", 4, "neutro"),
    ]
    for texto, tab_idx, cor in acoes:
        _btn(atalhos, texto, lambda i=tab_idx: tab_ctrl.select(i),
             cor=cor, largura=20).pack(side="left", padx=(0, 10))

    _separador(frame)

    # ── Últimas consultas ──
    _titulo_secao(frame, "Últimas Consultas")
    colunas_ult = ["ID", "Data/Hora", "Médico", "Paciente (NIF)", "Estado"]
    tbl_fr, tree_ult = _criar_tabela(frame, colunas_ult, alturas=8)
    tbl_fr.pack(fill="x", padx=24, pady=(0, 16))

    def _refresh_consultas():
        code, obj = listar_consultas()
        if code != 200:
            _preencher_tabela(tree_ult, []); return
        items = list(obj.items())[-10:]  # Últimas 10
        linhas = [(cid, d["data_hora"], d["id_medico"], d["id_paciente"], d["estado"])
                  for cid, d in items]
        _preencher_tabela(tree_ult, linhas)

    _refresh_consultas()

    btn_ref = tk.Frame(frame, bg=COR["card"], padx=24)
    btn_ref.pack(fill="x")
    def _refresh_tudo():
        _refresh_stats()
        _refresh_consultas()
    _btn(btn_ref, "⟳ Atualizar Dashboard", _refresh_tudo, "neutro", 24).pack(anchor="w")

    return frame


# ══════════════════════════════════════════════════════════════════════════════
#  JANELA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    root.title("Sistema de Gestão Hospitalar")
    root.geometry("1280x820")
    root.minsize(1100, 700)
    root.configure(bg=COR["fundo"])

    # ── Barra de topo ──
    topbar = tk.Frame(root, bg=COR["painel"], height=48, padx=18)
    topbar.pack(fill="x", side="top")
    topbar.pack_propagate(False)
    tk.Label(topbar, text="⚕  Hospital Manager", font=("Georgia", 14, "bold"),
             bg=COR["painel"], fg=COR["texto"]).pack(side="left", pady=10)
    tk.Label(topbar, text="v1.0", font=FONTE_SMALL,
             bg=COR["painel"], fg=COR["texto_dim"]).pack(side="left", padx=8, pady=10)
    # Linha de separação
    tk.Frame(root, bg=COR["borda_destaque"], height=2).pack(fill="x")

    # ── Notebook (abas) ──
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("H.TNotebook",
                    background=COR["fundo"],
                    borderwidth=0,
                    tabmargins=[0, 0, 0, 0])
    style.configure("H.TNotebook.Tab",
                    background=COR["painel"],
                    foreground=COR["texto_sec"],
                    font=FONTE_LABEL_B,
                    padding=[18, 10],
                    borderwidth=0,
                    focuscolor=COR["painel"])
    style.map("H.TNotebook.Tab",
              background=[("selected", COR["card"]), ("active", COR["sidebar_hover"])],
              foreground=[("selected", COR["destaque"]), ("active", COR["texto"])],
              expand=[("selected", [0, 0, 0, 2])])

    nb = ttk.Notebook(root, style="H.TNotebook")
    nb.pack(fill="both", expand=True, padx=0, pady=0)

    # Tabs — Dashboard primeiro, depois os módulos
    dash = _frame_dashboard(nb, nb)
    tab_unidade  = _frame_unidade(nb)
    tab_medico   = _frame_medico(nb)
    tab_paciente = _frame_paciente(nb)
    tab_consulta = _frame_consulta(nb)

    nb.add(dash,         text="  🏠 Dashboard  ")
    nb.add(tab_unidade,  text="  🏥 Unidades  ")
    nb.add(tab_medico,   text="  👨‍⚕️ Médicos  ")
    nb.add(tab_paciente, text="  🧑 Pacientes  ")
    nb.add(tab_consulta, text="  📋 Consultas  ")

    # ── Barra de estado (rodapé) ──
    statusbar = tk.Frame(root, bg=COR["painel"], height=26)
    statusbar.pack(fill="x", side="bottom")
    statusbar.pack_propagate(False)
    tk.Label(statusbar, text="  Sistema de Gestão Hospitalar  •  Dados guardados automaticamente em JSON",
             font=FONTE_SMALL, bg=COR["painel"], fg=COR["texto_dim"]).pack(side="left", pady=4)

    root.mainloop()


if __name__ == "__main__":
    main()