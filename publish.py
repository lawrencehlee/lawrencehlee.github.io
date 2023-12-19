import json
import markdown
import os
import shutil
import http.server
import socketserver
import sys


def clear_public():
    print("Clearing public directory")
    shutil.rmtree("public")
    os.mkdir("public")


def copy_root():
    for root_html_file in [filename for filename in os.listdir("app") if ".html" in filename]:
        print(f"Copying {root_html_file}")
        shutil.copy(f"app/{root_html_file}", "public/")

    print("Copying assets")
    shutil.copytree("app/assets", "public/assets")


def render_blogs():
    with open("app/blog/_template.html", 'r') as template_file:
        to_render = template_file.read()
    for md_file in [filename for filename in os.listdir("app/blog") if ".md" in filename]:
        print(f"Rendering {md_file}")
        base_filename = md_file[:-3]  # Strip .md
        with open(f"app/blog/{md_file}", 'r') as file:
            contents = file.read()

        html = markdown.markdown(contents)
        title = contents.split("\n")[0].replace("#", "").strip()
        to_render = to_render.replace("{{ body }}", html).replace("{{ title }}", title)

        os.mkdir("public/blog")
        with open(f"public/blog/{base_filename}.html", 'w') as output_file:
            output_file.write(to_render)


if __name__ == "__main__":
    clear_public()
    copy_root()
    render_blogs()

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        os.chdir("public")
        with socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler) as httpd:
            print("Serving at port 8000")
            httpd.serve_forever()
