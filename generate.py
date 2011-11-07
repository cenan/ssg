import os
import glob

import markdown2
from jinja2 import Environment, FileSystemLoader

import config


def generate():
	env = Environment(loader=FileSystemLoader(config.get("template_dir")))
	template = env.get_template("article.html")
	for f in glob.glob(os.path.join(config.get("source_dir"), "*.md")):
		filename, _ = os.path.splitext(os.path.basename(f))
		context = {}
		input_file = open(f)
		line = input_file.readline()
		while line != "\n":
			k, v = line.split(":")
			context[k] = v.strip()
			line = input_file.readline()
		content = "".join([l for l in input_file])
		context['content'] = markdown2.markdown(content, extras=["code-friendly", "code-color"])
		target_file = os.path.join(config.get("output_dir"), filename) + ".html"
		open(target_file, "w").write(template.render(context))


