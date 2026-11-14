"""Bilingual content for the privacy, terms and credits pages. Imported by build_site.py."""

REPO = "programmermars/open-source-games-site"
REPO_URL = f"https://github.com/{REPO}"
ISSUES_URL = f"{REPO_URL}/issues"
MAINTAINER = "programmermars"
EFFECTIVE = "2026-11-14"

# Games the site embeds or links to for play: who made them and under which terms.
PLAY_CREDITS = [
    # id, title, authors, source, code license, assets / other terms (zh, en)
    ("ancient-beast", "Ancient Beast", "FreezingMoon", "https://github.com/FreezingMoon/AncientBeast", "AGPL-3.0",
     ("美术与音频：CC BY-SA 4.0", "Art and audio: CC BY-SA 4.0")),
    ("anarch", "Anarch", "drummyfish", "https://gitlab.com/drummyfish/anarch", "CC0 1.0",
     ("代码与素材都是公有领域", "Code and assets are public domain")),
    ("athena-crisis", "Athena Crisis", "Nakazawa Tech", "https://github.com/nkzw-tech/athena-crisis", "MIT",
     ("品牌、美术、音效等素材另有授权，不可自由再分发", "Branding, art and sound are licensed separately and are not free to redistribute")),
    ("brogue-ce", "Brogue CE", "tmewett and contributors; browser port by brturn", "https://github.com/tmewett/BrogueCE", "AGPL-3.0",
     ("网页版是第三方非官方移植：github.com/brturn/BrogueCE", "The browser version is an unofficial third-party port: github.com/brturn/BrogueCE")),
    ("hypersomnia", "Hypersomnia", "Team Hypersomnia", "https://github.com/TeamHypersomnia/Hypersomnia", "AGPL-3.0", None),
    ("isocity", "IsoCity", "amilich", "https://github.com/amilich/isometric-city", "MIT", None),
    ("micropolisjs", "micropolisJS", "Graeme McCutcheon", "https://github.com/graememcc/micropolisJS", "GPL-3.0 with additional terms",
     ("“Micropolis” 是 Micropolis GmbH 的商标，按 Micropolis 公共名称许可使用", "“Micropolis” is a trademark of Micropolis GmbH, used under the Micropolis Public Name License")),
    ("server-survival", "Server Survival", "pshenok", "https://github.com/pshenok/server-survival", "MIT", None),
    ("whatajong", "Whatajong", "masylum", "https://github.com/masylum/whatajong", "MIT", None),
    ("wipeout", "wipEout rewrite", "Dominic Szablewski (phoboslab)", "https://github.com/phoboslab/wipeout-rewrite", "No license file",
     ("作者只允许非商业使用；游戏数据是 Psygnosis 原版素材，由作者托管，本站从不托管", "The author allows non-commercial use only; the game data is the original Psygnosis material, hosted by the author and never by this site")),
]


def privacy():
    zh = f"""
<p class="lead">一句话：本站不收集、不保存、不出售你的个人数据。没有账号，没有 Cookie，没有广告，没有统计或追踪脚本。</p>
<h2>本站在你的设备上保存什么</h2>
<p>只有两项偏好：界面语言和亮/暗主题，保存在你浏览器的 localStorage 里，不会发送给任何人。清除浏览器的网站数据即可删除。</p>
<h2>托管服务商会处理什么</h2>
<p>本站是放在 Cloudflare 上的静态网页。为了把网页送到你的浏览器并防御攻击，Cloudflare 会处理每次访问的技术信息，例如 IP 地址、浏览器类型和访问时间，按 <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare 隐私政策</a>处理。维护者最多只能看到 Cloudflare 提供的汇总数字（例如每天的访问量），看不到具体是谁在访问。</p>
<h2>字体和外部资源</h2>
<p>本站使用的字体放在本站自己的服务器上，打开页面时不会连接 Google 或其他第三方。</p>
<h2>游戏和外部链接</h2>
<p>游戏不在本站运行，而是由各自作者的网站提供。你点「开始玩」时，游戏网站会在本页的播放窗口中加载；点「新标签打开」或任何外部链接时，你会直接访问那个网站。这些网站会收到你的 IP 地址等信息，可能使用 Cookie、账号或在线多人功能，适用它们自己的隐私政策。没点开之前，本站不会加载任何游戏网站。</p>
<h2>儿童</h2>
<p>本站不收集任何人的个人数据，包括儿童。部分游戏有在线多人或聊天功能，家长请留意孩子玩的是哪个游戏。</p>
<h2>在 GitHub 上联系我们</h2>
<p>如果你在 <a href="{ISSUES_URL}">GitHub Issues</a> 反馈问题，你发布的内容是公开的，适用 GitHub 的隐私政策。</p>
<h2>变更</h2>
<p>本政策如有修改，会更新本页的生效日期，修改记录可在代码仓库中查看。</p>
"""
    en = f"""
<p class="lead">In one line: this site does not collect, store or sell your personal data. There are no accounts, no cookies, no ads, and no analytics or tracking scripts.</p>
<h2>What the site keeps on your device</h2>
<p>Two preferences only: interface language and light or dark theme, kept in your browser's localStorage and never sent anywhere. Clearing this site's data in your browser deletes them.</p>
<h2>What the hosting provider processes</h2>
<p>This is a static website hosted on Cloudflare. To deliver pages and defend against attacks, Cloudflare processes technical data about each request, such as IP address, browser type and time, under the <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare Privacy Policy</a>. The maintainer can at most see aggregate numbers Cloudflare provides, such as visits per day, never who visited.</p>
<h2>Fonts and outside resources</h2>
<p>The fonts are served from this site itself. Opening a page makes no request to Google or any other third party.</p>
<h2>Games and outside links</h2>
<p>The games do not run on this site; their authors host them. When you press “Play here”, the game's site loads inside this page's player. When you open a game in a new tab or follow any outside link, you visit that site directly. Those sites receive your IP address and similar data, may use cookies, accounts or online multiplayer, and follow their own privacy policies. Until you open one, this site loads no game site at all.</p>
<h2>Children</h2>
<p>This site collects no personal data from anyone, children included. Some games have online multiplayer or chat; parents should check which game a child is playing.</p>
<h2>Contacting us on GitHub</h2>
<p>If you report something in <a href="{ISSUES_URL}">GitHub Issues</a>, what you post is public and GitHub's privacy policy applies.</p>
<h2>Changes</h2>
<p>If this policy changes, the effective date on this page changes with it, and the history is visible in the code repository.</p>
"""
    return zh, en


def terms():
    zh = f"""
<p class="lead">本站是一个免费、非商业的开源游戏目录：不收费，不卖东西，不放广告。使用本站即表示你同意以下条款。</p>
<h2>本站提供什么</h2>
<p>本站整理了开源游戏和商业游戏开源重制的清单，并为其中可以在浏览器里玩的游戏提供入口：有的在本页的播放窗口中加载，有的在新标签打开。所有游戏都由各自的作者托管，本站不托管任何游戏文件。</p>
<h2>游戏属于它们的作者</h2>
<p>每个游戏、游戏名称和商标都属于其作者或权利人。你玩、修改或再分发某个游戏时，要遵守那个游戏自己的许可证和条款，详见<a href="../credits/">致谢与许可</a>。本站列出一个游戏，不代表本站与其作者有任何合作或背书关系。</p>
<h2>第三方网站</h2>
<p>游戏网站和外部链接由第三方运营。本站无法控制它们的内容、可用性、安全或隐私做法，它们随时可能变化或下线。如果你发现某个链接失效、被转手或指向可疑内容，请在 <a href="{ISSUES_URL}">GitHub Issues</a> 告诉我们，我们会尽快移除。</p>
<h2>合理使用</h2>
<ul>
<li>不要攻击、压测或扫描本站，也不要用自动程序大量请求导致服务变慢。</li>
<li>不要把本站嵌入其他网站，或冒充本站及其维护者。</li>
<li>不要利用本站从事违法活动。</li>
</ul>
<p>对滥用流量，我们可以通过 Cloudflare 限速或封锁，不另行通知。</p>
<h2>按现状提供</h2>
<p>本站按「现状」免费提供，不保证随时可用、内容准确或没有错误。在法律允许的最大范围内，维护者不对因使用本站或第三方游戏造成的任何损失负责。</p>
<h2>开源许可与本条款的关系</h2>
<p>本站代码以 MIT 许可证开源，游戏清单数据来自 bobeff/open-source-games，以 CC0 1.0 发布。这些许可证规定你如何使用代码和数据；本条款规定你如何使用这个网站。</p>
<h2>侵权与下架</h2>
<p>如果你认为本站某个链接或内容侵犯了你的权利，请通过 <a href="{ISSUES_URL}">GitHub Issues</a> 联系我们并说明理由。核实后我们会移除相关链接。</p>
<h2>变更</h2>
<p>条款如有修改，会更新本页的生效日期。修改后继续使用本站，即表示你接受新条款。</p>
"""
    en = f"""
<p class="lead">This is a free, non-commercial directory of open-source games: nothing to pay, nothing for sale, no ads. By using the site you agree to these terms.</p>
<h2>What the site offers</h2>
<p>The site lists open-source games and open-source remakes of commercial games, and gives a way into the ones that run in a browser: some load in this site's player, others open in a new tab. Every game is hosted by its authors; this site hosts no game files.</p>
<h2>Games belong to their authors</h2>
<p>Every game, game name and trademark belongs to its authors or rights holders. When you play, modify or redistribute a game, follow that game's own license and terms; see <a href="../credits/">Credits &amp; licenses</a>. Listing a game does not mean its authors are affiliated with or endorse this site.</p>
<h2>Third-party sites</h2>
<p>Game sites and outside links are run by third parties. This site does not control their content, availability, security or privacy practices, which may change or disappear at any time. If you find a link that is dead, has changed hands or points at something suspicious, tell us in <a href="{ISSUES_URL}">GitHub Issues</a> and we will remove it.</p>
<h2>Fair use</h2>
<ul>
<li>Do not attack, load-test or scan the site, or send automated requests in volumes that slow it down.</li>
<li>Do not embed the site in another site or pose as the site or its maintainer.</li>
<li>Do not use the site for anything unlawful.</li>
</ul>
<p>Abusive traffic may be rate-limited or blocked through Cloudflare without notice.</p>
<h2>Provided as is</h2>
<p>The site is provided free and “as is”, with no promise that it is always available, accurate or error-free. To the fullest extent the law allows, the maintainer is not liable for any loss arising from using the site or any third-party game.</p>
<h2>Open-source licenses and these terms</h2>
<p>The site's code is open source under the MIT License, and the list data comes from bobeff/open-source-games under CC0 1.0. Those licenses govern how you use the code and data; these terms govern how you use this website.</p>
<h2>Rights and takedowns</h2>
<p>If you believe a link or content on this site infringes your rights, contact us through <a href="{ISSUES_URL}">GitHub Issues</a> with your reasons. Once confirmed, we remove the link.</p>
<h2>Changes</h2>
<p>If these terms change, the effective date on this page changes with them. Using the site after a change means you accept the new terms.</p>
"""
    return zh, en


def credits(esc, entries_total, list_commit):
    def rows(lang):
        out = []
        for _id, title, authors, src, code, extra in PLAY_CREDITS:
            other = esc(extra[0] if lang == "zh" else extra[1]) if extra else "—"
            out.append(
                f"<tr><th scope=\"row\">{esc(title)}</th><td>{esc(authors)}</td>"
                f"<td><a href=\"{esc(src)}\">{esc(src.split('://', 1)[1])}</a></td>"
                f"<td>{esc(code)}</td><td>{other}</td></tr>"
            )
        return "".join(out)

    table = lambda lang, heads: (
        "<div class=\"table-wrap\"><table class=\"credits\"><thead><tr>"
        + "".join(f"<th scope=\"col\">{h}</th>" for h in heads)
        + f"</tr></thead><tbody>{rows(lang)}</tbody></table></div>"
    )

    zh = f"""
<p class="lead">这个网站站在许多开源作者的肩膀上。下面写明每一份内容来自谁、按什么许可使用。</p>
<h2>游戏清单</h2>
<p>全部 {entries_total} 个项目的名称、简介和链接来自 <a href="https://github.com/bobeff/open-source-games">bobeff/open-source-games</a>（版本 {esc(list_commit)}），由 bobeff 和<a href="https://github.com/bobeff/open-source-games/graphs/contributors">所有贡献者</a>整理，以 CC0 1.0 公有领域发布。中文简介由本站翻译。</p>
<h2>可以在浏览器里玩的游戏</h2>
<p>这些游戏都由作者自己托管，本站只是在播放窗口中加载或链接过去，没有复制或修改它们的任何文件。</p>
{table("zh", ["游戏", "作者", "源代码", "代码许可", "其他条款"])}
<p>清单里其余每个项目的作者和源代码，都在条目旁的「源码」链接里。</p>
<h2>字体与设计</h2>
<ul>
<li><a href="https://github.com/Omnibus-Type/Archivo">Archivo</a>，Omnibus-Type，SIL Open Font License 1.1。</li>
<li><a href="https://github.com/IBM/plex">IBM Plex Mono</a>，IBM，SIL Open Font License 1.1。</li>
<li>配色取自 1984 年 IBM EGA 显卡的 16 色调色板；页面使用「Open Source Games」设计系统。</li>
</ul>
<p>字体许可证全文随字体文件一起发布在 <code>assets/fonts/</code>。</p>
<h2>本站代码</h2>
<p>本站代码以 MIT 许可证开源：<a href="{REPO_URL}">{REPO}</a>。欢迎 fork、提问题或提交改进。</p>
<h2>商标</h2>
<p>文中提到的游戏名称、公司名称和商标都属于各自的权利人，在这里只用来说明出处。</p>
"""
    en = f"""
<p class="lead">This site stands on the work of many open-source authors. Here is who made each part and the license it is used under.</p>
<h2>The game list</h2>
<p>The names, descriptions and links of all {entries_total} projects come from <a href="https://github.com/bobeff/open-source-games">bobeff/open-source-games</a> (version {esc(list_commit)}), curated by bobeff and <a href="https://github.com/bobeff/open-source-games/graphs/contributors">all its contributors</a> and dedicated to the public domain under CC0 1.0. The Chinese descriptions are this site's translation.</p>
<h2>Games you can play in the browser</h2>
<p>Their authors host every one of these games. This site loads them in its player or links to them, and copies or modifies none of their files.</p>
{table("en", ["Game", "Authors", "Source", "Code license", "Other terms"])}
<p>For every other project in the list, its authors and code are behind the “source” link next to the entry.</p>
<h2>Fonts and design</h2>
<ul>
<li><a href="https://github.com/Omnibus-Type/Archivo">Archivo</a> by Omnibus-Type, SIL Open Font License 1.1.</li>
<li><a href="https://github.com/IBM/plex">IBM Plex Mono</a> by IBM, SIL Open Font License 1.1.</li>
<li>The colors come from the 16-color palette of IBM's 1984 EGA graphics card; the pages use the Open Source Games design system.</li>
</ul>
<p>The full font licenses ship with the font files in <code>assets/fonts/</code>.</p>
<h2>This site's code</h2>
<p>The site's code is open source under the MIT License: <a href="{REPO_URL}">{REPO}</a>. Forks, issues and improvements are welcome.</p>
<h2>Trademarks</h2>
<p>Game names, company names and trademarks mentioned here belong to their owners and are used only to identify the work.</p>
"""
    return zh, en
