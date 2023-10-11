from pathlib import Path
import glob
import exifread


def on_page_markdown(markdown, page, config, files):
    if "cordons" not in page.title.lower():
        return

    # markdown += "## Packs Adultes\n\n"

    markdown += '<div class="grid cards" markdown>\n\n'

    for file_path in sorted(
        glob.glob(f"{config.docs_dir}/assets/images/cordons/adulte/*")
    ):
        f = open(file_path, "rb")
        tags = exifread.process_file(f)
        description = tags.get("Image ImageDescription")
        if description is None:
            print(f"ERROR: {file_path} has no 'ImageDescription' ({tags})")

        file_url = Path(file_path).relative_to(config.docs_dir)

        markdown += f"- ![{description}]({file_url}){{lazyload}}\n    {description}\n"

    # context["images"] = images

    markdown += "\n</div>\n"

    # print(markdown)
    return markdown
