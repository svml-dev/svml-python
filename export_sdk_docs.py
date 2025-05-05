import pdoc
import pdoc.doc
import importlib
import json
import os
import inspect
import re
import importlib.util
import pkgutil
from typing import get_type_hints
import shutil

OUTPUT_DIR = "docs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "svml_public.json")
MDX_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "svml-sdk.mdx")
os.makedirs(OUTPUT_DIR, exist_ok=True)

mod = importlib.import_module("svml.client")
module = pdoc.doc.Module(mod)

# --- Modular docstring parsing and rendering ---
def get_docstring_type(docstring):
    if not docstring:
        return None
    first_line = docstring.strip().split('\n')[0].lower()
    if first_line.startswith('type:'):
        return first_line.split(':', 1)[1].strip()
    return None

def parse_method_docstring(docstring):
    # Simple Google-style parser for Args, Returns, Raises, Example, Notes
    sections = {'args': [], 'returns': '', 'raises': '', 'example': '', 'notes': ''}
    if not docstring:
        return sections
    lines = [line.rstrip() for line in docstring.strip().split('\n')]
    current = None
    for l in lines:
        if l.startswith('Args:') or l.startswith('Required Args:'):
            current = 'args'
            continue
        elif l.startswith('Returns:'):
            current = 'returns'
            continue
        elif l.startswith('Raises:'):
            current = 'raises'
            continue
        elif l.startswith('Example:'):
            current = 'example'
            continue
        elif l.startswith('Notes:'):
            current = 'notes'
            continue
        elif l == '' or l.startswith('---'):
            continue
        if current == 'args':
            m = re.match(r'([\w_]+) \(([^)]+)\): (.*)', l)
            if m:
                name, typ, desc = m.groups()
                sections['args'].append((name.strip(), typ.strip(), desc.strip()))
            else:
                m2 = re.match(r'([\w_]+): (.*)', l)
                if m2:
                    name, desc = m2.groups()
                    sections['args'].append((name.strip(), '', desc.strip()))
        elif current in ('returns', 'raises', 'example', 'notes'):
            if sections[current]:
                sections[current] += '\n' + l
            else:
                sections[current] = l
    return sections

def parse_response_docstring(docstring):
    # Parse Attributes section, capturing multi-line indented blocks for each attribute
    if not docstring:
        return {'attributes': {}, 'example': ''}
    lines = docstring.split('\n')
    # Skip type: ... line if present
    if lines and lines[0].strip().lower().startswith('type:'):
        lines = lines[1:]
    in_attrs = False
    attr_desc = {}
    current_attr = None
    current_desc = []
    example = ''
    for i, line in enumerate(lines):
        l = line.rstrip('\n')
        if l.strip().startswith('Attributes:'):
            in_attrs = True
            continue
        if in_attrs:
            m = re.match(r'\s*([\w_]+) \(([^)]+)\): (.*)', l)
            if m:
                if current_attr:
                    attr_desc[current_attr] = '\n'.join(current_desc).rstrip()
                current_attr = m.group(1).strip()
                current_desc = [m.group(3).strip()]
                continue
            m2 = re.match(r'\s*([\w_]+): (.*)', l)
            if m2:
                if current_attr:
                    attr_desc[current_attr] = '\n'.join(current_desc).rstrip()
                current_attr = m2.group(1).strip()
                current_desc = [m2.group(2).strip()]
                continue
            if l.strip() == '' or (l and not l.startswith(' ')):
                if current_attr:
                    attr_desc[current_attr] = '\n'.join(current_desc).rstrip()
                    current_attr = None
                    current_desc = []
                if l.strip() and not l.startswith(' '):
                    in_attrs = False
                continue
            if current_attr and (l.startswith('    ') or l.startswith('\t')):
                current_desc.append(l.strip())
        # Example section
        if l.strip().startswith('Example:'):
            example = '\n'.join(lines[i+1:]).strip()
            break
    if current_attr:
        attr_desc[current_attr] = '\n'.join(current_desc).rstrip()
    return {'attributes': attr_desc, 'example': example}

def parse_class_docstring(docstring):
    # Stub for future class doc parsing
    return {}

def render_method_to_mdx(parsed):
    out = ''
    if parsed['args']:
        out += '**Arguments:**\n\n'
        for name, typ, desc in parsed['args']:
            if typ:
                out += f'- **{name} ({typ})**: {desc}\n'
            else:
                out += f'- **{name}**: {desc}\n'
        out += '\n'
    if parsed['returns']:
        out += f'**Returns:**\n{parsed["returns"]}\n\n'
    if parsed['raises']:
        out += f'**Raises:**\n{parsed["raises"]}\n\n'
    if parsed['example']:
        out += f'**Example:**\n```python\n{parsed["example"]}\n```\n\n'
    if parsed['notes']:
        out += f'**Notes:**\n{parsed["notes"]}\n\n'
    return out

def render_response_to_mdx(parsed, class_name):
    out = f'## {class_name}\n\n'
    out += f'Response from the /{class_name.replace("Response", "").lower()} endpoint of the SVML API.\n\n'
    attrs = parsed['attributes']
    if attrs:
        out += '| Field | Description |\n|-------|-------------|\n'
        for fname, desc in attrs.items():
            out += f'| `{fname}` | {desc.split("\n")[0]} |\n'
        out += '\n'
        # Render structure blocks below the table
        for fname, desc in attrs.items():
            struct_lines = []
            lines = desc.split('\n')
            for i, l in enumerate(lines):
                if l.strip().startswith('STRUCTURE:'):
                    struct_lines = [l2.strip() for l2 in lines[i+1:] if l2.strip()]
                    break
            if struct_lines:
                out += f'#### `{fname}` structure\n\n'
                out += '```json\n'
                out += '\n'.join(struct_lines) + '\n'
                out += '```\n\n'
    if parsed['example']:
        out += '**Example:**\n'
        out += '```json\n' + parsed['example'] + '\n```\n\n'
    return out 

def is_public_method(member):
    return (
        member.kind == "function"
        and not member.name.startswith("_")
        and not (member.name.startswith("__") and member.name.endswith("__"))
    )

def python_type_to_human(t):
    if t is None or t == 'None':
        return ''
    t = str(t)
    if t in ("<class 'str'>", 'str'):
        return 'string'
    if t in ("<class 'int'>", 'int'):
        return 'integer'
    if t in ("<class 'float'>", 'float'):
        return 'float'
    if t in ("<class 'bool'>", 'bool'):
        return 'boolean'
    if t in ("<class 'list'>", 'list'):
        return 'list'
    if t in ("<class 'dict'>", 'dict'):
        return 'dict'
    if t == 'NoneType':
        return 'null'
    return t.replace("<class '", '').replace("'>", '')

def parse_param_descriptions(docstring):
    # Handles Google style and new style: name (type): desc, name (type, optional): desc, with or without leading dash
    param_desc = {}
    if not docstring:
        return param_desc
    # Find all lines that look like an argument
    arg_lines = re.findall(r'^[ \t\-]*([\w_]+) \(([^)]+)\): (.*)$', docstring, re.MULTILINE)
    for name, _type, desc in arg_lines:
        param_desc[name.strip()] = desc.strip()
    return param_desc

def serialize_param(param, param_desc):
    if param.name in ("kwargs", "args"):  # filter out kwargs/args
        return None
    return {
        "name": param.name,
        "type": python_type_to_human(param.annotation) if param.annotation is not inspect._empty else '',
        "default": param.default if param.default is not inspect._empty else '',
        "description": param_desc.get(param.name, ''),
    }

def get_params(func, docstring):
    sig = inspect.signature(func.obj)
    param_desc = parse_param_descriptions(docstring)
    return [p for p in (serialize_param(param, param_desc) for param in sig.parameters.values() if param.name != "self") if p]

def serialize_client_class(cls):
    # Parse param descriptions for __init__
    init_doc = cls.members.get("__init__").docstring if "__init__" in cls.members else ""
    return {
        "name": cls.name,
        "docstring": cls.docstring,
        "kind": "class",
        "init": {
            "docstring": init_doc,
            "params": get_params(cls.members.get("__init__"), init_doc) if "__init__" in cls.members else [],
        },
        "methods": [
            {
                "name": m.name,
                "docstring": m.docstring,
                "params": get_params(m, m.docstring),
                "return_type": str(inspect.signature(m.obj).return_annotation) if inspect.signature(m.obj).return_annotation is not inspect._empty else None,
            }
            for m in cls.members.values() if is_public_method(m)
        ]
    }

# Find SVMLClient in the module
svml_client = next((m for m in module.members.values() if m.name == "SVMLClient"), None)
if svml_client:
    doc_tree = serialize_client_class(svml_client)
else:
    doc_tree = {}

with open(OUTPUT_FILE, "w") as f:
    json.dump(doc_tree, f, indent=2)

print(f"Public API documentation generated at {OUTPUT_FILE}")

# MDX export improvements
def parse_docstring_sections(docstring):
    """
    Parse a Google-style docstring into sections: required_args, optional_args, returns, raises, example, notes.
    Returns a dict with lists of (name, type, desc) for args, and strings for other sections.
    """
    sections = {
        'required_args': [],
        'optional_args': [],
        'returns': '',
        'raises': '',
        'example': '',
        'notes': ''
    }
    if not docstring:
        return sections
    lines = [line.rstrip() for line in docstring.strip().split('\n')]
    current = None
    for idx, line in enumerate(lines):
        l = line.strip()
        if l.startswith('Required Args:'):
            current = 'required_args'
            continue
        elif l.startswith('Optional Args:'):
            current = 'optional_args'
            continue
        elif l.startswith('Returns:'):
            current = 'returns'
            continue
        elif l.startswith('Raises:'):
            current = 'raises'
            continue
        elif l.startswith('Example:'):
            current = 'example'
            continue
        elif l.startswith('Notes:'):
            current = 'notes'
            continue
        elif l == '' or l.startswith('---'):
            continue
        if current in ('required_args', 'optional_args'):
            m = re.match(r'([\w_]+) \(([^)]+)\): (.*)', l)
            if m:
                name, typ, desc = m.groups()
                sections[current].append((name.strip(), typ.strip(), desc.strip()))
            else:
                # fallback: try to match name: desc
                m2 = re.match(r'([\w_]+): (.*)', l)
                if m2:
                    name, desc = m2.groups()
                    sections[current].append((name.strip(), '', desc.strip()))
        elif current in ('returns', 'raises', 'example', 'notes'):
            if sections[current]:
                sections[current] += '\n' + l
            else:
                sections[current] = l
    return sections

def mdx_args_list(args, title):
    if not args:
        return ''
    out = [f'**{title}:**']
    for name, typ, desc in args:
        if typ:
            out.append(f'- **{name} ({typ})**: {desc}')
        else:
            out.append(f'- **{name}**: {desc}')
    out.append('')  # blank line for MDX
    out.append('')  # ensure a second blank line after the list
    return '\n'.join(out)

def mdx_section(title, content):
    if not content:
        return ''
    return f'**{title}:**\n{content}\n\n'

def mdx_param_table(args, required_count=None):
    if not args:
        return ''
    header = '| Name | Type | Req | Description |\n|------|------|-----|-------------|'
    rows = []
    for idx, (name, typ, desc) in enumerate(args):
        req = 'yes' if required_count is None or idx < required_count else 'no'
        rows.append(f"| `{name}` | {typ} | {req} | {desc} |")
    return '\n'.join([header] + rows) + '\n'

def mdx_method_section(method):
    docstring = method['docstring']
    sections = parse_docstring_sections(docstring)
    out = f"\n## `{method['name']}`\n\n"
    if docstring:
        if method['name'] == '__init__':
            out += ''  # skip
        else:
            out += (method['docstring'].split('\n')[0].strip() + '\n\n')  # summary line
    out += mdx_args_list(sections['required_args'], 'Required Arguments')
    out += mdx_args_list(sections['optional_args'], 'Optional Arguments')
    out += mdx_section('Returns', sections['returns'])
    out += mdx_section('Raises', sections['raises'])
    out += mdx_section('Example', sections['example'])
    out += mdx_section('Notes', sections['notes'])
    # Parameter table
    if sections['required_args'] or sections['optional_args']:
        all_args = sections['required_args'] + sections['optional_args']
        out += mdx_param_table(all_args, required_count=len(sections['required_args']))
    # Ensure two blank lines at the end of each method section
    if not out.endswith('\n\n'):
        out += '\n\n'
    return out

with open(MDX_OUTPUT_FILE, "w") as f:
    f.write(f"# SVMLClient (Python SDK)\n\n")
    f.write(f"> {doc_tree.get('docstring', '').replace('\n', ' ')}\n\n---\n\n")
    # Constructor
    init = doc_tree.get('init', {})
    init_docstring = init.get('docstring', '')
    init_sections = parse_docstring_sections(init_docstring)
    param_str = ', '.join([name + (f'=None' if typ.endswith('optional') or name != 'api_key' else '') for name, typ, desc in (init_sections['required_args'] + init_sections['optional_args'])])
    f.write(f"## Constructor\n\n")
    f.write(f"```python\nSVMLClient({param_str})\n```\n\n")
    f.write(mdx_args_list(init_sections['required_args'], 'Required Arguments'))
    f.write(mdx_args_list(init_sections['optional_args'], 'Optional Arguments'))
    f.write(mdx_section('Notes', init_sections['notes']))
    if init_sections['required_args'] or init_sections['optional_args']:
        all_args = init_sections['required_args'] + init_sections['optional_args']
        f.write(mdx_param_table(all_args, required_count=len(init_sections['required_args'])))
    f.write(f"---\n\n## Methods\n\n")
    for method in doc_tree.get('methods', []):
        f.write(mdx_method_section(method))
    # --- Response Classes Section ---
    f.write('\n---\n\n# Response Classes\n\n')

    # Dynamically import all modules in svml.endpoints
    import svml.endpoints
    endpoint_pkg = svml.endpoints
    for _, modname, ispkg in pkgutil.iter_modules(endpoint_pkg.__path__):
        if ispkg:
            continue
        mod = importlib.import_module(f'svml.endpoints.{modname}')
        for name in dir(mod):
            if name.endswith('Response'):
                cls = getattr(mod, name)
                if not isinstance(cls, type):
                    continue
                doc = cls.__doc__ or ''
                doc_type = get_docstring_type(doc)
                if doc_type == 'response':
                    parsed = parse_response_docstring(doc)
                    f.write(render_response_to_mdx(parsed, name))
                # (future: handle other types)

print(f"MDX documentation generated at {MDX_OUTPUT_FILE}")

# Copy MDX to docs site content folder
DEST_MDX = os.path.join(
    '..', '..', 'www', 'www-svml-dev', 'svml-dev-site', 'content', 'docs', 'python', 'svml-sdk.mdx'
)
os.makedirs(os.path.dirname(DEST_MDX), exist_ok=True)
shutil.copyfile(MDX_OUTPUT_FILE, DEST_MDX)
print(f"MDX documentation copied to {DEST_MDX}")

