from pathlib import Path
import glob
import exifread

DESCRIPTIONS = {
    "abondance": "- **PIERRE DE SOLEIL** permet de garder la positive attitude. On y croit !\n        - **CITRINE** aide aux négociations ; pierre de l'abondance et de l'argent.\n        - **JADE** attire la chance, la réussite et booste votre efficacité pour réussir.\n",
    "amour de soi": "- **AMÉTHYSTE** supprime les pensées négatives. Apaise. Vous vous aimez.\n        - **PIERRE de LUNE** vous guide tout en douceur pour vous montrer ce qui est bon pour Vous.\n        - **KUNZITE** vous enveloppe tendrement de ses douces ondes rassurantes. Aide au lâcher prise.",
    "bien-être": "- **AMAZONITE** favorise le lâcher prise. Apporte réconfort, équilibre et « zénitude ».\n        - **MALACHITE** accompagne les différents corps (physique et éthérique) dans la guérison. Elle absorbe les pensées, les émotions et les énergies négatives et les pollutions.\n        - **AVENTURINE** donne du courage ; apaise les peurs et aide à surmonter les blessures émotionnelles.",
    "boost business": "- **JADE** attire l'abondance, la réussite et la chance en apportant la gratitude dans votre coeur.\n        - **OBSIDIENNE** balaye les obstacles. A la fois guerrière et bouclier anti-mauvaises ondes. Elle débarrasse tous les obstacles sur votre chemin.\n        - **QUARTZ FUMÉ** recentre pour avancer la tête haute vers vos objectifs. Apporte volonté, détermination, efficacité et pragmatisme.",
    "communication - expression": "- **AIGUE MARINE** rafraîchit les idées quand tout semble embrumé. Les oraux sont facilités (examens scolaires, professionnels, conférences…). Apporte chance et protection.\n        - **AMAZONITE** soutient les hypersensibles ; pouvoir d'affirmation, don de communication juste.\n        - **SODALITE** favorise la communication positive et l'écoute ; permet de garder focus les pensées. Topissime en réunion. Calme les angoisses.",
    "confiance en soi": "- **FLUORITE** chasse le doute, libère l'esprit des pensées encombrantes. Procure la confiance en soi. Décomplexe.\n        - **AVENTURINE** apaise les peurs. Vous invite à croire en Vous. Votre amie pour de nouvelles envies. Vous aide à prendre les choses en main afin de vous donner du courage.\n        - **MALACHITE** dénoue les blocages émotionnels. Pousse à tenter et à oser.",
    "connexion": "- **AMÉTHYSTE** purifie l'aura. Développe vitesse grand V votre intuition. Spiritualité. Paix intérieure.\n        - **LAPIS LAZULI** protège avec effet boomerang les mauvaises pensées qui sont retournées à l'envoyeur. Hautement spirituelle ; contact avec ses guides.\n        - **APATITE** ouvre les portes de l'inconscient. Pierre pour se souvenir de ses rêves.",
    "déblocage": "- **MORGANITE** pointe du doigt vos blocages et vous aide à y répondre. Précieuse alliée en cas de difficultés. Compréhension – Libération.\n        - **AIGUE MARINE** vous êtes sous haute protection. Libre et heureuse. Fini la peur.\n        - **AVENTURINE** apporte motivation, optimisme et vous permet croire en Vous. Fidèle amie pour vous aider à concrétiser vos rêves.",
    "énergie - vitalité": "- **PYRITE** allume la flamme qui est en vous. Regain d'énergie vitesse grand V. Mode bonne humeur «activé».\n        - **OEIL de TIGRE** dynamise, véritable bouclier énergétique. Vous pensiez être arrivé(e) au bout et bien hop hop hop !!! l'oeil de tigre allume la réserve d'énergie.\n        - **CITRINE** inonde d'énergie positive, de joie et de gaieté. Énergie solaire.",
    "féminité": "- **LÉPIDOLITE** réconcilie avec toutes les facettes de votre être profond. Elle rassure et donne confiance.\n        - **CORNALINE** restaure votre féminité naturelle. Pierre hardie, hyper féminine dans toute sa splendeur.\n        - **KUNZITE** pour guérir les blessures du coeur. Amour inconditionnel, énergie maternelle.",
    "masculin": "- **LAPIS LAZULI** renforce la confiance et l'intuition. Une aide incontournable pour affronter les difficultés. Mémoire +. Donne du courage aux timides et aux introvertis.\n        - **OEIL de TIGRE** stimule le courage ; booste la volonté. Pour reprendre du poil de la bête.\n        - **OEIL de FAUCON** Aide au lâcher prise ; décisions éclairées. Esprit serein, hyper focus, novateur et visionnaire.",
    "méditation": "- **KUNZITE** veille sur Vous. Une belle bulle de protection. Lâchez vos résistances.\n        - **OPALE ROSE** des Andes favorise la communion avec les esprits. Relâche les tensions, anti-déprime.\n        - **SÉLÉNITE** vous enveloppe dans ses « hautes Vib » célestes. Mystiquement Vôtre.",
    "passion": "- **CORNALINE** ravive la passion. Relance le dynamisme. Sous la couette ambiance caliente. Pierre altruiste, elle partage ses énergies au contact des autres pierres.\n        - **GRENAT** développe avec subtilité votre pouvoir de séduction. Aide en cas de passage à vide ou de montagnes russes. Chance aux nouveaux couples. Réchauffe l'atmosphère sous la couette. Symbole de la sexualité sacrée.\n        - **PIERRE DE SOLEIL** attire le bonheur. Plaisir de la vie. On rayonne !",
    "pleine lune": "- **PIERRE de LUNE** relie l'esprit avec un fil d'argent à la Lune. Calme le flot d'émotions. Développe votre intuition.\n        - **LABRADORITE** protège des influences extérieures. Pour rester aligné(e). Ancrage les pieds sur terre, la tête en l'air !\n        - **SÉLÉNITE** recharge aussi bien les esprits ainsi que les cristaux. Connexion avec les Anges. Purification, harmonie et paix.",
    "protection": "- **OEIL de FAUCON** veille sur vous ; la force est en Vous. Diffuse des énergies positives. La vie avec des paillettes n'est plus très loin !\n        - **LABRADORITE** évite les fuites d'énergies qui vous laissent à plat. Chasse les ruminations. Véritable bouclier anti « Pac Man ».\n        - **SHUNGITE** vous procure une nouvelle force. L'ultime bouclier XXL par excellence. Ancre votre énergie dans la terre. Anti-stress. Je suis protégé(e). Tout...va...bien !",
    "transformation": "- **OEIL de TIGRE** favorise la prise de décision. Pierre des timides et des procrastineurs.\n        - **MALACHITE** on tourne la page. Les blocages sont dénoués ; l'espoir renaît. La renaissance est proche.\n        - **QUARTZ FUMÉ** donne le signal qu'il faut agir ; l'absolu déclencheur. Apporte pragmatisme et volonté.",
    "zen - sérénité": "- **KUNZITE** vous place dans une bulle de protection. Son aura enveloppant et maternant vous baigne dans le réconfort. Don't touch !\n        - **LÉPIDOLITE** renforce votre sentiment de sécurité. Symbolise la tempérance. Anti-cauchemar. Je suis en parfaite sécurité et sérénité.\n        - **TOURMALINE** atténue les peurs. Donne confiance en soi. Apporte un concentré d'énergies positives. Quiétude et joie de vivre.",
}


def on_page_markdown(markdown, page, config, files):
    if "bracelets" not in page.title.lower():
        return

    markdown += '<div class="grid cards" markdown>\n\n'

    for file_path in sorted(
        glob.glob(f"{config.docs_dir}/assets/images/bracelets/magic_trilogy/*")
    ):
        f = open(file_path, "rb")
        tags = exifread.process_file(f)
        description = tags.get("Image ImageDescription")
        if description is None:
            print(f"ERROR: {file_path} has no 'ImageDescription' ({tags})")

        file_url = Path(file_path).relative_to(config.docs_dir)

        description_key = description.printable.split(":")[0].lower().strip()

        if description_key in DESCRIPTIONS:
            markdown += f'- ![{description}]({file_url}){{loading=lazy}}\n\n    !!! abstract "{description}"\n'
            markdown += f"\n        {DESCRIPTIONS[description_key]}\n\n"
        else:
            print("MISSING description", description_key)

    # context["images"] = images

    markdown += "\n</div>\n"

    print(markdown)
    return markdown
