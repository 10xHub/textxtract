"""Generate API documentation for textxtract package."""

from pathlib import Path
import mkdocs_gen_files

# Get the source root directory
src_root = Path("textxtract")

# Create the main API index page
with mkdocs_gen_files.open("reference/index.md", "w") as f:
    content = [
        "# API Reference",
        "",
        "Welcome to the Text Extractor API reference documentation.",
        "",
        "## Main Components",
        "",
        "- [Sync Extractor](sync/extractor.md) - Synchronous text extraction",
        "- [Async Extractor](aio/extractor.md) - Asynchronous text extraction",
        "- [Core Components](core/index.md) - Base classes and utilities",
        "- [Handlers](handlers/index.md) - File format handlers",
        "",
    ]
    f.write("\n".join(content))

# Generate documentation for all Python files
for path in sorted(src_root.rglob("*.py")):
    # Skip __pycache__ and test files
    if "__pycache__" in str(path) or "test_" in path.name:
        continue

    module_path = path.relative_to(src_root)
    doc_path = Path("reference", module_path).with_suffix(".md")

    # Create directory structure if needed
    with mkdocs_gen_files.open(doc_path, "w") as f:
        # Convert file path to module name
        if path.name == "__init__.py":
            # For __init__.py files, use the parent directory name
            parts = list(module_path.parent.parts)
            if parts:
                ident = "textxtract." + ".".join(parts)
                title = f"{parts[-1].title()} Module"
            else:
                ident = "textxtract"
                title = "Text Extractor Package"
        else:
            # For regular Python files
            parts = list(module_path.with_suffix("").parts)
            ident = "textxtract." + ".".join(parts)
            title = f"{parts[-1].title()} Module"

        content = [f"# {title}", "", f"::: {ident}"]
        f.write("\n".join(content))

# Create index pages for subdirectories
subdirs = ["core", "handlers", "sync", "aio"]
for subdir in subdirs:
    subdir_path = src_root / subdir
    if subdir_path.exists():
        with mkdocs_gen_files.open(f"reference/{subdir}/index.md", "w") as f:
            content = [f"# {subdir.title()} Module", "", "## Overview", ""]

            if subdir == "core":
                content.extend(
                    [
                        "Core components of the text extraction framework.",
                        "",
                        "- [Base Classes](base.md) - Abstract base classes",
                        "- [Configuration](config.md) - Configuration management",
                        "- [Exceptions](exceptions.md) - Custom exceptions",
                        "- [Registry](registry.md) - Handler registry",
                        "- [Utils](utils.md) - Utility functions",
                    ]
                )
            elif subdir == "handlers":
                content.extend(
                    ["File format handlers for different document types.", ""]
                )
                # List all handler files
                for handler_file in sorted(subdir_path.glob("*.py")):
                    if handler_file.name != "__init__.py":
                        handler_name = handler_file.stem
                        content.append(
                            f"- [{handler_name.upper()} Handler]({handler_name}.md) - {handler_name.upper()} file format handler"
                        )
            elif subdir == "sync":
                content.append("Synchronous text extraction components.")
            elif subdir == "aio":
                content.append("Asynchronous text extraction components.")

            content.extend(["", f"::: textxtract.{subdir}"])
            f.write("\n".join(content))
