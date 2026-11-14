"""Gera os SVGs do perfil (grafite suave com detalhes em vermelho). Rode: python brand/build.py

Cada bloco é um card de 1280 px; o README os separa por títulos de seção.
"""
import base64
from pathlib import Path
from xml.sax.saxutils import escape

NOANIM = bool(__import__("os").environ.get("NOANIM"))  # só para prévias estáticas
ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
W = 1280
MONO = "'JetBrains Mono', 'SF Mono', Consolas, Menlo, 'DejaVu Sans Mono', monospace"
# grafite suave e tons quentes; o vermelho é só detalhe
BG, BAR, LINE, CARD = "#1A1C21", "#202328", "#30333A", "#23262C"
RED, RED_L, RED_D = "#E86262", "#F09C98", "#6A3537"
TXT, MUTED, DIM, FAINT = "#ECE8E3", "#B1B3B8", "#42454C", "#80838A"

# link do Água Limpa (repositório do Pedro, ainda privado)
AGUA_URL = "https://github.com/Pedro-Osaka/projeto-agua"


def t(x, y, s, size=16, fill=TXT, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def fade(content, i=0, dur=0.7):
    if NOANIM:
        return content
    """Entrada suave (sobe 10 px e aparece). Sem suporte a SMIL, fica visível normalmente."""
    d = min(0.12 * i, 1.6)
    total = d + dur
    k = f"{d / total:.3f}"
    return (f'<g>{content}'
            f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{k};1" dur="{total:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 10;0 10;0 0" keyTimes="0;{k};1" '
            f'dur="{total:.2f}s" calcMode="spline" keySplines="0 0 1 1;.2 .7 .3 1" fill="freeze"/></g>')


def wrap(s, n):
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def shape(h, top, bottom, r=20):
    """Retângulo com cantos arredondados só em cima e/ou embaixo."""
    a, b = (r if top else 0), (r if bottom else 0)
    return (f"M{a} 0H{W - a}Q{W} 0 {W} {a}V{h - b}Q{W} {h} {W - b} {h}H{b}Q0 {h} 0 {h - b}V{a}Q0 0 {a} 0Z")


def block(h, title, body, label, top=True, bottom=True, bar=True):
    a = escape(label, {'"': "&quot;"})
    p = shape(h, top, bottom)
    head = ""
    if bar:
        head = (f'<rect width="{W}" height="48" fill="{BAR}"/>'
                f'<path d="M10 48.5H{W}" stroke="{LINE}"/>')
        dots = (f'<circle cx="36" cy="24" r="5" fill="{DIM}"/><circle cx="54" cy="24" r="5" fill="{DIM}"/>'
                f'<circle cx="72" cy="24" r="5" fill="{RED}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
                + t(100, 29, f"gabriel@dev:~$ {title}", fill=MUTED))
    else:
        dots = ""
    edge = ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{a}">
<title>{a}</title>
<defs><clipPath id="c"><path d="{p}"/></clipPath>
<linearGradient id="rail" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED_D}"/><stop offset=".5" stop-color="{RED}"/><stop offset="1" stop-color="{RED_D}"/>
<animate attributeName="y2" values="1;2;1" dur="6s" repeatCount="indefinite"/></linearGradient></defs>
<g clip-path="url(#c)"><rect width="{W}" height="{h}" fill="{BG}"/>{head}{edge}<rect width="5" height="{h}" fill="url(#rail)"/></g>
<path d="{p}" fill="none" stroke="{LINE}" stroke-width="2"/>
{dots}
{body}
</svg>
'''


def chip(x, y, s, fill=CARD, stroke=LINE, color=TXT, size=15):
    w = len(s) * size * 0.6 + 28
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="34" rx="9" fill="{fill}" stroke="{stroke}"/>'
            + t(x + 14, y + 22, s, size, color)), w


def chips(x, y, items, **kw):
    out = []
    for s in items:
        c, w = chip(x, y, s, **kw)
        out.append(c)
        x += w + 10
    return "".join(out)


def img64(name):
    return "data:image/jpeg;base64," + base64.b64encode((ROOT / "previews" / f"{name}.jpg").read_bytes()).decode()


# ---------------------------------------------------------------- banner e botões

def banner():
    h = 420
    body = [
        f'<defs><radialGradient id="g" cx="85%" cy="30%" r="65%"><stop offset="0" stop-color="{RED}" stop-opacity=".14">'
        f'<animate attributeName="stop-opacity" values=".14;.08;.14" dur="7s" repeatCount="indefinite"/></stop>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
        f'<pattern id="p" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#22252B"/></pattern></defs>',
        f'<rect x="8" y="49" width="{W-8}" height="{h-49}" fill="url(#p)"/>',
        f'<rect x="8" y="49" width="{W-8}" height="{h-49}" fill="url(#g)"/>',
        fade(t(70, 130, "> whoami", 20, FAINT), 0),
        fade(t(70, 205, "Gabriel do Valle", 64, TXT, 700), 1),
        fade(t(70, 255, "IA · Automação · Desenvolvimento Web", 26, MUTED), 2),
        fade(t(70, 300, "Transformo processos manuais em sistemas.", 20, MUTED), 3),
    ]
    x, cs = 70, []
    for s, hot in [("Resende, RJ", False), ("Full-stack", False), ("Sistemas de Informação · 4º período", False),
                   ("Disponível para projetos", True)]:
        c, w = chip(x, 335, s, color=RED_L if hot else TXT, stroke=RED_D if hot else LINE)
        cs.append(c)
        x += w + 12
    body.append(fade("".join(cs), 4))
    body.append(fade(
        f'<rect x="1010" y="110" width="200" height="200" rx="30" fill="{CARD}" stroke="{LINE}" stroke-width="2"/>'
        + t(1110, 238, "GV", 84, RED, 700, "middle")
        + f'<rect x="1098" y="262" width="24" height="5" fill="{RED}">'
          '<animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>', 2))
    return block(h, "./apresentar --perfil", "\n".join(body),
                 "Gabriel do Valle. IA, automação e desenvolvimento web. Resende, RJ. Full-stack. "
                 "Sistemas de Informação, 4º período. Disponível para projetos.", top=True, bottom=True)


def button(label, icon_path, filled=True):
    w = int(len(label) * 13 * 0.62 + 76)
    bg, fg = (RED, "#FFFFFF") if filled else (CARD, TXT)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="42" viewBox="0 0 {w} 42" role="img" aria-label="{label}">
<title>{label}</title>
<rect x=".5" y=".5" width="{w-1}" height="41" rx="10" fill="{bg}" stroke="{RED if filled else LINE}"/>
<svg x="20" y="12" width="18" height="18" viewBox="0 0 24 24"><path fill="none" stroke="{fg}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="{icon_path}"/></svg>
{t(48, 26, label.upper(), 13, fg, 600, extra=' letter-spacing="1.2"')}
</svg>
'''


ICONS = {
    "portfolio": ("Portfólio", "M12 2a10 10 0 100 20 10 10 0 000-20zM2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20", True),
    "projetos": ("Ver projetos", "M3 7h7l2 2h9v10H3zM3 7V5h6l2 2", False),
    "email": ("E-mail", "M3 5h18v14H3zM3 5l9 8 9-8", False),
}


# ---------------------------------------------------------------- coluna principal (blocos colados)

def perfil():
    cells = [
        ("atuacao", "Desenvolvedor web autônomo", "sites, sistemas e automações"),
        ("formacao", "Sistemas de Informação", "4º período · UniDomBosco (AEDB)"),
        ("foco", "IA aplicada a processos", "agentes, integrações e LLMs"),
        ("entrega", "Da arquitetura ao deploy", "sistema rodando e documentado"),
    ]
    body, cw = [], 587
    for i, (k, v, sub) in enumerate(cells):
        x, y = 50 + (i % 2) * (cw + 16), 68 + (i // 2) * 106
        body.append(fade(f'<rect x="{x}" y="{y}" width="{cw}" height="90" rx="12" fill="{CARD}" stroke="{LINE}"/>'
                         + t(x + 20, y + 25, "$", fill=RED) + t(x + 39, y + 25, k, fill=MUTED)
                         + t(x + 20, y + 53, v, 22) + t(x + 20, y + 75, sub, fill=MUTED), i))
    label = "Perfil. " + "; ".join(f"{k}: {v} ({s})" for k, v, s in cells)
    return block(68 + 2 * 106 + 18, "cat perfil", "\n".join(body), label, top=True)


EXPERIENCE = [
    ("2026 – atual", "Desenvolvedor web", "Autônomo",
     "Sites, sistemas e automações para clientes: site da Santos Barber Studio e sistema de controle de caixa com painel e relatórios."),
    ("mai/2025 – mar/2026", "Jovem Aprendiz (CIEE)", "Colégio Santa Ângela",
     "Manutenção e suporte em computadores, atendimento e suporte interno, planilhas e relatórios administrativos (Excel e VBA)."),
    ("2025 – em andamento", "Sistemas de Informação", "Centro Universitário Dom Bosco (AEDB)",
     "Bacharelado, 4º período, em andamento."),
]


def experience():
    body, y = [], 78
    body.append(f'<path d="M66 {y + 10}V{y + 3 * 112 - 50}" stroke="{DIM}" stroke-width="2" stroke-dasharray="4 6"/>')
    for i, (period, role, org, desc) in enumerate(EXPERIENCE):
        lines = wrap(desc, 100)
        g = (f'<circle cx="66" cy="{y + 8}" r="8" fill="{BG}" stroke="{RED}" stroke-width="2"/>'
             f'<circle cx="66" cy="{y + 8}" r="3" fill="{RED}"/>'
             + t(96, y + 15, role, 22, TXT, 700)
             + t(96 + len(role) * 22 * 0.6 + 16, y + 15, f"· {org}", 18, MUTED)
             + t(1230, y + 15, period, 15, FAINT, anchor="end"))
        for j, ln in enumerate(lines):
            g += t(96, y + 44 + j * 24, ln, 16, MUTED)
        body.append(fade(g, i))
        y += 112
    label = "Experiência e formação. " + " ".join(f"{r}, {o} ({p}): {d}" for p, r, o, d in EXPERIENCE)
    return block(y + 4, "cat experiencia.log", "\n".join(body), label)


def card(name, path, status, desc, tags, foot, preview, extra=""):
    """Projeto sem moldura: prévia à esquerda, texto à direita, linha fina separando do próximo."""
    lines = wrap(desc, 62)
    py = 36
    h = max(py + 92 + len(lines) * 26 + 100, py + 248 + 36)
    stext, filled = status
    sw = len(stext) * 13 * 0.6 + 40
    px = 50
    if preview:
        pv = (f'<clipPath id="pv"><rect x="{px}" y="{py}" width="440" height="248" rx="12"/></clipPath>'
              f'<image href="{img64(preview)}" x="{px}" y="{py}" width="440" height="248" clip-path="url(#pv)" preserveAspectRatio="xMidYMin slice"/>'
              f'<rect x="{px}" y="{py}" width="440" height="248" rx="12" fill="none" stroke="{LINE}"/>')
    else:
        pv = extra
    tx = 524
    g = [t(tx, py + 16, path, 14, FAINT),
         t(tx, py + 56, name, 30, TXT, 700),
         f'<rect x="{1230 - sw:.0f}" y="{py}" width="{sw:.0f}" height="28" rx="14" fill="{CARD}" stroke="{RED_D if filled else LINE}"/>',
         f'<circle cx="{1230 - sw + 17:.0f}" cy="{py + 14}" r="4" fill="{RED if filled else FAINT}"/>',
         t(1230 - sw + 28, py + 19, stext.upper(), 13, RED_L if filled else MUTED, 600)]
    y = py + 92
    for ln in lines:
        g.append(t(tx, y, ln, 17, MUTED))
        y += 26
    g.append(chips(tx, y + 2, tags, size=14))
    g.append(t(tx, y + 64, f"▸ {foot}", 14, FAINT))
    label = f"{name} — {stext}. {desc} Tecnologias: {', '.join(tags)}. {foot}."
    return block(h, "", fade(pv, 0) + fade("".join(g), 1), label, bar=False)


def crm_placeholder():
    """Sem captura pública (área logada): painel ilustrativo, sinalizado como tal."""
    x, y = 50, 36
    rows = [("novo", "Barbearia Centro", "sem_site"), ("novo", "Pet Shop Ana", "quebrado"),
            ("contatado", "Oficina JR", "so_redes"), ("fechado", "Studio Nails", "funcional")]
    g = (f'<rect x="{x}" y="{y}" width="440" height="248" rx="12" fill="{CARD}" stroke="{LINE}"/>'
         + t(x + 20, y + 32, "lista Contatar", 16, TXT, 600)
         + t(x + 420, y + 32, "ilustrativo", 12, FAINT, anchor="end"))
    for i, (st, nome, site) in enumerate(rows):
        yy = y + 62 + i * 44
        g += (f'<rect x="{x + 16}" y="{yy}" width="408" height="34" rx="8" fill="{BG}" stroke="{LINE}"/>'
              + t(x + 30, yy + 22, nome, 13, TXT) + t(x + 250, yy + 22, site, 12, MUTED)
              + t(x + 410, yy + 22, st, 12, RED_L if st == "fechado" else MUTED, anchor="end"))
    return g


STACK = [
    ("IA & Automação", ["Claude API", "OpenAI API", "RAG", "LangChain", "n8n", "Webhooks"]),
    ("Front-end", ["React", "Next.js", "TypeScript", "Tailwind CSS", "Framer Motion", "Three.js"]),
    ("Back-end & Dados", ["Node.js", "Python", "PostgreSQL", "SQLite", "Supabase", "Prisma"]),
    ("Cloud & Entrega", ["AWS (EC2, S3, IAM)", "Vercel", "Docker", "Git & GitHub", "CI/CD", "Cloudflare"]),
    ("UI/UX", ["Figma", "Design System", "Acessibilidade", "Responsivo"]),
]


def stack():
    body, y = [], 70
    for i, (title, items) in enumerate(STACK):
        body.append(fade(t(50, y + 20, f"./{title}", 17, TXT, 600) + chips(50, y + 34, items), i))
        y += 90
    label = "Tech Stack. " + " ".join(f"{g}: {', '.join(i)}." for g, i in STACK)
    return block(y + 10, "ls stack/", "\n".join(body), label)


FACULDADE = [
    ("barberflow", "BarberFlow", ("No ar na AWS", True),
     "Agendamento online para barbearias, publicado na AWS: EC2 com Node.js e SQLite, pacote no S3 lido por role do IAM e só a porta 80 aberta. Custo estimado de US$ 11,90/mês.",
     ["EC2", "S3", "IAM", "Node.js", "SQLite"], "Projeto Integrador · 2026 · clique para ver o case"),
    ("agua-limpa", "Água Limpa, Vida Sustentável", ("Concluído", False),
     "Projeto de extensão com a SANEAR: site de conscientização sobre água e saneamento, filtro de garrafa PET e ações com a comunidade em Resende.",
     ["HTML", "CSS", "JavaScript", "Firebase"], "extensão universitária · grupo de 9 · 3 cursos · 2026"),
]

PROJECTS = [
    ("santos-barber", "Santos Barber Studio", ("No ar", True),
     "Site da barbearia em Resende, RJ: serviços com preço e duração, aviso de aberto agora, mapa com rota, avaliações com login e agendamento pelo WhatsApp.",
     ["Site institucional", "SEO local", "WhatsApp"], "projeto para cliente · santosbarberstudios.com"),
    ("crm-leads", "CRM de Leads", ("Em produção", True),
     "CRM de prospecção: importa negócios do Google Maps, verifica site e Instagram de cada um e monta a lista de quem contatar, com funil e exportação em XLSX.",
     ["Next.js", "Supabase", "TypeScript"], "repositório privado · área logada"),
    ("controle-de-caixa", "Controle de Caixa", ("Entregue", False),
     "Lançamento do dia por contadores, cadastro de serviços e painel que calcula faturamento, despesas e lucro, com relatórios por qualquer período.",
     ["Sistema web", "Dashboard", "Relatórios"], "projeto para cliente · código privado"),
    ("site-pessoal", "Site pessoal", ("Publicado", True),
     "Portfólio com cases de clientes, stack e serviços. Next.js com export estático, publicado no GitHub Pages.",
     ["Next.js", "TypeScript", "Framer Motion"], "gabrielvallecg.github.io"),
]


def footer():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="40" viewBox="0 0 420 40" role="img" aria-label="Fim do perfil">
<title>Fim do perfil</title>
<path d="M0 20H130M290 20H420" stroke="{DIM}"/>
{t(210, 26, "gabriel@dev:~$ exit", 15, FAINT, anchor="middle")}
</svg>
'''


# ---------------------------------------------------------------- BarberFlow: arquitetura (página do case)

def arquitetura():
    h = 470

    def box(x, y, w, hh, title, sub, hot=False):
        s = (f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="12" fill="{CARD}" stroke="{RED if hot else LINE}"'
             f'{" stroke-width=\"2\"" if hot else ""}/>' + t(x + w / 2, y + 32, title, 18, TXT, 700, "middle"))
        for i, ln in enumerate(sub):
            s += t(x + w / 2, y + 58 + i * 22, ln, 14, MUTED, anchor="middle")
        return s

    def arrow(x1, y1, x2, y2, label="", dashed=False):
        d = ' stroke-dasharray="6 6"' if dashed else ""
        s = (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{RED}" stroke-width="2"{d} marker-end="url(#ar)">'
             f'<animate attributeName="stroke-dashoffset" values="24;0" dur="1.2s" repeatCount="indefinite"/></path>') if dashed else \
            f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{RED}" stroke-width="2" marker-end="url(#ar)"/>'
        if label:
            s += t((x1 + x2) / 2, (y1 + y2) / 2 - 10, label, 13, RED_L, anchor="middle")
        return s

    body = [f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0L10 5L0 10z" fill="{RED}"/></marker></defs>',
            fade(box(50, 150, 200, 110, "Navegador", ["cliente e", "barbeiro"]), 0),
            fade(f'<rect x="330" y="90" width="560" height="300" rx="16" fill="none" stroke="{RED_D}" stroke-dasharray="6 6"/>'
                 + t(350, 116, "Security Group · só porta 80", 14, RED_L), 1),
            fade(box(380, 140, 460, 150, "EC2 t3.micro · Amazon Linux", ["site + API em Node.js", "banco SQLite no disco EBS", "(persiste entre sessões do lab)"], True), 2),
            fade(box(380, 310, 220, 64, "Role do IAM", []) + t(490, 362, "acesso ao S3 sem chave", 12, MUTED, anchor="middle"), 3),
            fade(box(970, 100, 240, 110, "Amazon S3", ["pacote do site", "e config de e-mail"]), 3),
            fade(box(970, 250, 240, 110, "Gmail SMTP", ["códigos e", "confirmações"]), 4),
            fade(box(970, 380, 240, 64, "CloudShell", []) + t(1090, 432, "script cria tudo", 12, MUTED, anchor="middle"), 5),
            fade(arrow(250, 205, 376, 205, "HTTP :80"), 2),
            fade(arrow(842, 190, 966, 160, "baixa no boot", True), 4),
            fade(arrow(842, 245, 966, 300, "envia e-mail", True), 5),
            fade(arrow(966, 412, 890, 380, ""), 6)]
    return block(h, "cat barberflow/arquitetura.svg", "\n".join(body),
                 "Arquitetura do BarberFlow na AWS: o navegador acessa a EC2 pela porta 80 (Security Group). "
                 "A EC2 t3.micro roda o site, a API em Node.js e o SQLite no disco EBS; no boot baixa o pacote do S3 "
                 "usando uma role do IAM. E-mails saem pelo Gmail SMTP. Tudo foi criado por script no CloudShell.",
                 top=True, bottom=True)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {
        "banner.svg": banner(), "perfil.svg": perfil(), "experiencia.svg": experience(),
        "stack.svg": stack(),
        "footer.svg": footer(), "barberflow-arquitetura.svg": arquitetura(),
    }
    files |= {f"btn-{k}.svg": button(*v) for k, v in ICONS.items()}
    for k, *p in FACULDADE:
        files[f"faculdade-{k}.svg"] = card(*p[:1], f"faculdade / {k}", *p[1:], preview=k)
    for i, (k, *p) in enumerate(PROJECTS):
        files[f"project-{k}.svg"] = card(*p[:1], f"gabrielvallecg / {k}", *p[1:],
                                         preview=None if k == "crm-leads" else k,
                                         extra=crm_placeholder() if k == "crm-leads" else "")
    for n, s in files.items():
        (OUT / n).write_text(s, encoding="utf-8")
    print(len(files), "arquivos em", OUT)
