import markdown
from flask import Flask
import markdown.extensions.fenced_code

app = Flask(__name__)


@app.route("/")
def index():
    readme_file = open("./question_base/Exams5and6.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["mdx_math"]
    )
    # md = markdown.Markdown(extensions=['mdx_math'])
    # result = md.convert('$$e^x$$')
    return md_template_string


if __name__ == "__main__":
    app.run()
