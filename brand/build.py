"""Gera os SVGs do perfil (tema preto e vermelho). Rode: python brand/build.py"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 1280
MONO = "'JetBrains Mono', 'SF Mono', Consolas, Menlo, 'DejaVu Sans Mono', monospace"
BG, BAR, LINE, CARD = "#0A0A0A", "#141010", "#2A1A1A", "#170F0F"
RED, RED_L, RED_D = "#E5383B", "#FF6B6B", "#7A1416"
TXT, MUTED, DIM = "#F2F2F2", "#A3A3A3", "#3A2A2A"


def t(x, y, s, size=16, fill=TXT, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def wrap(s, n):
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def window(h, title, body, label):
    """Janela de terminal: barra no topo, faixa vermelha à esquerda."""
    a = escape(label, {'"': "&quot;"})
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{a}">
<title>{a}</title>
<defs><clipPath id="c"><rect width="{W}" height="{h}" rx="20"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="{W}" height="{h}" fill="{BG}"/>
<rect width="{W}" height="48" fill="{BAR}"/><rect width="10" height="{h}" fill="{RED}"/></g>
<path d="M10 48.5H{W}" stroke="{LINE}"/>
<rect x=".5" y=".5" width="{W-1}" height="{h-1}" rx="20" fill="none" stroke="{LINE}"/>
<circle cx="36" cy="24" r="5" fill="{DIM}"/><circle cx="54" cy="24" r="5" fill="{DIM}"/><circle cx="72" cy="24" r="5" fill="{RED}"/>
{t(100, 29, f"gabriel@dev:~$ {title}", fill=MUTED)}
{body}
</svg>
'''


def chip(x, y, s, fill=CARD, stroke=LINE, color=TXT, size=15):
    w = len(s) * size * 0.6 + 28
    return f'<rect x="{x}" y="{y}" width="{w:.0f}" height="34" rx="8" fill="{fill}" stroke="{stroke}"/>' + \
        t(x + 14, y + 22, s, size, color), w


def banner():
    h = 420
    body = [
        f'<defs><radialGradient id="g" cx="85%" cy="30%" r="60%"><stop offset="0" stop-color="{RED}" stop-opacity=".35"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
        f'<pattern id="p" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#1A1212"/></pattern></defs>',
        f'<rect x="10" y="49" width="{W-10}" height="{h-49}" fill="url(#p)"/>',
        f'<rect x="10" y="49" width="{W-10}" height="{h-49}" fill="url(#g)"/>',
        t(70, 130, "> whoami", 20, RED),
        t(70, 205, "Gabriel do Valle", 64, TXT, 700),
        t(70, 255, "IA · Automação · Desenvolvimento Web", 26, RED_L),
        t(70, 300, "Transformo processos manuais em sistemas.", 20, MUTED),
    ]
    x = 70
    for s in ["Resende, RJ", "Full-stack", "Disponível para projetos"]:
        c, w = chip(x, 335, s, color=TXT if s != "Disponível para projetos" else RED_L,
                    stroke=LINE if s != "Disponível para projetos" else RED_D)
        body.append(c)
        x += w + 12
    # monograma com cursor piscando
    body.append(f'<rect x="1000" y="110" width="200" height="200" rx="28" fill="{CARD}" stroke="{RED_D}" stroke-width="2"/>')
    body.append(t(1100, 238, "GV", 84, RED, 700, "middle"))
    body.append(f'<rect x="1088" y="262" width="24" height="5" fill="{RED}">'
                '<animate attributeName="opacity" values="1;0;1" dur="1.2s" repeatCount="indefinite"/></rect>')
    return window(h, "./apresentar --perfil", "\n".join(body),
                  "Gabriel do Valle. IA, automação e desenvolvimento web. Resende, RJ. Full-stack. Disponível para projetos.")


def button(label, icon_path):
    w = int(len(label) * 13 * 0.62 + 76)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="42" viewBox="0 0 {w} 42" role="img" aria-label="{label}">
<title>{label}</title>
<rect x=".5" y=".5" width="{w-1}" height="41" rx="9" fill="{RED}" stroke="{RED}"/>
<svg x="20" y="12" width="18" height="18" viewBox="0 0 24 24"><path fill="none" stroke="#FFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="{icon_path}"/></svg>
{t(48, 26, label.upper(), 13, "#FFFFFF", 600, extra=' letter-spacing="1.2"')}
</svg>
'''


def perfil():
    cells = [
        ("atuacao", "Desenvolvedor full-stack", "sites, CRMs, painéis e automações"),
        ("foco", "IA aplicada a processos", "agentes, integrações e LLMs"),
        ("entrega", "Da arquitetura ao deploy", "sistema rodando e documentado"),
        ("formacao", "Sistemas de Informação", "Faculdade Dom Bosco (AEDB)"),
    ]
    body, cw = [], 587
    for i, (k, v, sub) in enumerate(cells):
        x, y = 50 + (i % 2) * (cw + 16), 68 + (i // 2) * 106
        body += [f'<rect x="{x}" y="{y}" width="{cw}" height="90" rx="12" fill="{CARD}" stroke="{LINE}"/>',
                 t(x + 20, y + 25, "$", fill=RED), t(x + 39, y + 25, k, fill=RED_L),
                 t(x + 20, y + 53, v, 22), t(x + 20, y + 75, sub, fill=MUTED)]
    label = "Perfil. " + "; ".join(f"{k}: {v} ({s})" for k, v, s in cells)
    return window(68 + 2 * 106 + 18, "cat perfil", "\n".join(body), label)


STACK = [
    ("IA & Automação", ["Claude API", "OpenAI API", "RAG", "LangChain", "n8n", "Webhooks"]),
    ("Front-end", ["React", "Next.js", "TypeScript", "Tailwind CSS", "Framer Motion", "Three.js"]),
    ("Back-end & Dados", ["Node.js", "Python", "PostgreSQL", "Supabase", "Prisma", "REST"]),
    ("Infra & Entrega", ["Vercel", "AWS", "Docker", "Git & GitHub", "CI/CD", "Cloudflare"]),
    ("UI/UX", ["Figma", "Design System", "Acessibilidade", "Responsivo"]),
]


def stack():
    body, y = [], 70
    for title, items in STACK:
        body.append(t(50, y + 20, f"./{title}", 17, RED_L, 600))
        x, y = 50, y + 34
        for s in items:
            c, w = chip(x, y, s)
            body.append(c)
            x += w + 10
        y += 56
    label = "Tech Stack. " + " ".join(f"{g}: {', '.join(i)}." for g, i in STACK)
    return window(y + 10, "ls stack/", "\n".join(body), label)


# status: (texto, preenchido?)  preenchido = no ar / publicado
PROJECTS = [
    ("santos-barber", "Santos Barber Studio", ("No ar", True),
     "Site da barbearia Santos Barber Studio (Resende, RJ): serviços com preço e duração, horário com aviso de aberto agora, mapa com rota, avaliações com login e agendamento pelo WhatsApp.",
     ["Site institucional", "SEO local", "Responsivo", "WhatsApp"], "projeto para cliente · santosbarberstudios.com"),
    ("crm-leads", "CRM de Leads", ("Em produção", True),
     "CRM de prospecção: importa planilhas de negócios do Google Maps, verifica o site e o Instagram de cada um e monta a lista de quem contatar, com funil e exportação em XLSX.",
     ["Next.js", "TypeScript", "Supabase", "Tailwind CSS", "Vercel"], "repositório privado · uso próprio"),
    ("party-hub", "Party Hub", ("Publicado", True),
     "Jogos de festa no celular, sem instalar nada: O Impostor, Palavras!, Ache Sua Dupla e Mímica. As partidas rodam direto entre os aparelhos, sem backend próprio.",
     ["JavaScript", "WebRTC", "PeerJS", "Tailwind CSS"], "código aberto · jogue no navegador"),
    ("controle-de-caixa", "Controle de Caixa", ("Entregue", False),
     "Sistema de caixa com lançamento do dia por contadores, cadastro de serviços e painel que calcula faturamento, despesas e lucro, com relatórios por qualquer período.",
     ["Sistema web", "Dashboard", "Relatórios", "Controle financeiro"], "projeto para cliente · código privado"),
    ("site-pessoal", "Site pessoal", ("Publicado", True),
     "Portfólio com cases de clientes, stack e serviços. Next.js com export estático, publicado no GitHub Pages.",
     ["Next.js", "TypeScript", "Framer Motion", "GitHub Pages"], "gabrielvallecg.github.io"),
]


def project(name, status, desc, tags, foot):
    lines = wrap(desc, 98)
    h = 150 + len(lines) * 28 + 40
    stext, filled = status
    sw = len(stext) * 15 * 0.6 + 44
    body = [t(50, 95, name, 30, TXT, 700),
            f'<rect x="{1230 - sw:.0f}" y="72" width="{sw:.0f}" height="34" rx="17" fill="{RED if filled else "none"}" stroke="{RED}"/>',
            f'<circle cx="{1230 - sw + 20:.0f}" cy="89" r="5" fill="{"#FFF" if filled else RED}"/>',
            t(1230 - sw + 32, 94, stext, 15, "#FFF" if filled else RED_L, 600)]
    y = 140
    for ln in lines:
        body.append(t(50, y, ln, 18, MUTED))
        y += 28
    x, y = 50, y + 2
    for s in tags:
        c, w = chip(x, y, s, color=RED_L, stroke=RED_D)
        body.append(c)
        x += w + 10
    body.append(t(50, y + 68, f"# {foot}", 15, "#6B5B5B"))
    label = f"{name} — {stext}. {desc} Tecnologias: {', '.join(tags)}. {foot}."
    return window(h + 46, f"cat projetos/{name.lower().replace(' ', '-')}.md", "\n".join(body), label)


def footer():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="40" viewBox="0 0 420 40" role="img" aria-label="Fim do perfil">
<title>Fim do perfil</title>
<path d="M0 20H150M270 20H420" stroke="{RED_D}"/>
{t(210, 26, "gabriel@dev:~$ exit", 15, RED, anchor="middle")}
</svg>
'''


ICONS = {
    "portfolio": ("Portfólio", "M12 2a10 10 0 100 20 10 10 0 000-20zM2 12h20M12 2a15 15 0 010 20M12 2a15 15 0 000 20"),
    "email": ("E-mail", "M3 5h18v14H3zM3 5l9 8 9-8"),
    "partyhub": ("Party Hub", "M6 11h4M8 9v4M15 12h.01M18 10h.01M17.3 5H6.7a4 4 0 00-4 3.6L2 15a3 3 0 005.2 2l1.3-2h7l1.3 2a3 3 0 005.2-2l-.7-6.4A4 4 0 0017.3 5z"),
}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    files = {"banner.svg": banner(), "perfil.svg": perfil(), "stack.svg": stack(), "footer.svg": footer()}
    files |= {f"btn-{k}.svg": button(*v) for k, v in ICONS.items()}
    files |= {f"project-{p[0]}.svg": project(*p[1:]) for p in PROJECTS}
    for n, s in files.items():
        (OUT / n).write_text(s, encoding="utf-8")
    print(len(files), "arquivos em", OUT)
