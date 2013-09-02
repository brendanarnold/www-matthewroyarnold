import os
import shutil
import distutils.dir_util
from jinja2 import Template, FileSystemLoader, Environment
from scss import Scss

# Build variables

DEBUG = True
TEMPLATES_DIR = "templates"
WWW_TEMPLATES_DIR = "\\www"
SITE_DIR = TEMPLATES_DIR + WWW_TEMPLATES_DIR
STATIC_DIR = "static"
BUILD_DIR = "build"
CSS_DIR = "css"
COMPILED_CSS_FN = "mra_compiled.css"
# Referenced from the template directory, also needs to be forward slash
BASE_TEMPLATE_FN = "base_templates/desktop_web.tmpl"
CSS_TEMPLATE_EXT = ".scss"
HTML_TEMPLATE_EXT = ".tmpl"

# Site variables
EMAIL = 'matthewroyarnold@gmail.com'
TEL = 'UK 07805 543612'

env = Environment(loader = FileSystemLoader(TEMPLATES_DIR))


# Process HTML files first
for (path, dirs, fns) in os.walk(SITE_DIR):
    # Templates use forward slash so need to substitute
    tpath = path.replace('\\', '/')
    # Templates also referred to wrt. template directory, so need to
    # remove the template directory from the path so left with e.g.
    # '/www/exhibitions'
    tpath = tpath[len(TEMPLATES_DIR):]
    for fn in fns:
        if not fn.endswith(HTML_TEMPLATE_EXT):
            continue
        # tfp is e.g. /www/exhibitions/index.tmpl or /www/about.tmpl
        tfp = tpath + '/' + fn
        t = env.get_template(tfp)
        # Files in subfolders need their relative paths changing - next
        # few lines builds the relevant path
        root_path = ''
        wpath = tfp[len(WWW_TEMPLATES_DIR):] # Gets the relative web path e.g. /about.tmpl
        for i in range(len([d for d in wpath.split('/') if d.strip() != '']) - 1):
            root_path += '../'
        if not root_path:
            root_path = './'
        # Get the breadcrumb URLs
        curr_path = root_path
        for d in (d.strip() for d in wpath.split('/')):
            # The root
            if not d:
                breadcrumb_urls = [(root_path, 'home')]
            # The template
            elif d == 'index.tmpl':
                del breadcrumb_urls[-1]
            elif not d.endswith('.tmpl'):
                curr_path += d
                breadcrumb_urls.append( (curr_path + '/', d) ) 
        # Finally get the template
        src = t.render(base_template = BASE_TEMPLATE_FN, 
            root_path = root_path,
            breadcrumb_urls = breadcrumb_urls,
            email = EMAIL,
            tel = TEL)

        # Create build directory if it does not already exist
        bdirn = os.path.join(BUILD_DIR, path[len(SITE_DIR)+1:])
        if not os.path.isdir(bdirn):
            print "Creating directory: " + bdirn
            os.makedirs(bdirn)
        # Write to file
        out_fn = os.path.join(bdirn, fn.split('.')[0] + '.html')
        with open(out_fn, 'w') as out_fh:
            out_fh.write(src)
        print out_fn

# Compile CSS
css = Scss()
csstdir = os.path.join(TEMPLATES_DIR, CSS_DIR)
out_str = ''
for fn in os.listdir(csstdir):
    fp = os.path.join(csstdir, fn)
    if not fp.endswith(CSS_TEMPLATE_EXT):
        continue
    with open(fp) as fh:
        fstr = fh.read()
    out_str = out_str + css.compile(fstr)
out_dir = os.path.join(BUILD_DIR, 'css')
if not os.path.isdir(out_dir):
    print "Creating directory: " + out_dir
    os.makedirs(out_dir)
out_fn = os.path.join(out_dir, COMPILED_CSS_FN)
with open(out_fn, 'w') as fh:
    fh.write(out_str)
    print "CSS compiled to: " + out_fn

# Finally copy static files
distutils.dir_util.copy_tree(STATIC_DIR, BUILD_DIR)
print "Copied static files"
