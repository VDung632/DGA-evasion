import ast
import os

BASE_DIR = "../"

def get_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=file_path)
    imports = []
    for item in node.body:
        if isinstance(item, ast.Import):
            for alias in item.names:
                imports.append(alias.name)
        elif isinstance(item, ast.ImportFrom):
            module = item.module
            if module:
                imports.append(module)
    return imports

def resolve_imports(imports, base_dir):
    resolved_imports = set()
    for imp in imports:
        imp_path = imp.replace('.', os.sep)
        py_file = os.path.join(base_dir, imp_path + ".py")
        if os.path.isfile(py_file):
            resolved_imports.add(py_file)
            new_imports = get_imports(py_file)
            resolved_imports.update(resolve_imports(new_imports, base_dir))
    return resolved_imports

def find_local_imports(main_file):
    base_dir = os.path.dirname(main_file)
    initial_imports = get_imports(main_file)
    all_imports = resolve_imports(initial_imports, BASE_DIR)
    return all_imports

def main():
    main_file = "gan_language.py"  # Replace with your main Python file path
    local_imports = find_local_imports(main_file)
    for imp in local_imports:
        print(imp)

if __name__ == "__main__":
    main()
