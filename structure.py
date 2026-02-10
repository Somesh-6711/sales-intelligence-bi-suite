from pathlib import Path

PROJECT_NAME = "Sales Intelligence BI Suite (Tableau + MySQL + Python)"

FOLDERS = [
    "data/raw",
    "data/processed",
    "data/outputs",
    "sql",
    "notebooks",
    "src",
    "dashboards/tableau_dashboard_screenshots",
    "docs",
    "tests",
]

FILES = {
    "README.md": f"# {PROJECT_NAME}\n\n",
    "requirements.txt": "",
    ".gitignore": "",
    ".env.example": "MYSQL_HOST=localhost\nMYSQL_PORT=3306\nMYSQL_USER=root\nMYSQL_PASSWORD=your_password\nMYSQL_DB=sales_bi\n",
    "sql/schema.sql": "-- MySQL schema will go here\n",
    "sql/views.sql": "-- KPI views will go here\n",
    "src/__init__.py": "",
    "src/config.py": "# Load env vars here\n",
    "src/extract_load.py": "# Load raw data into MySQL\n",
    "src/transform_clean.py": "# Clean + transform data\n",
    "src/validate_quality.py": "# Data quality checks\n",
    "src/refresh_pipeline.py": "# Orchestrate pipeline steps\n",
    "docs/kpi_definitions.md": "# KPI Definitions\n",
    "docs/data_dictionary.md": "# Data Dictionary\n",
    "docs/user_guide.md": "# User Guide\n",
}

GITIGNORE_CONTENT = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
venv/
.env
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# Data (keep raw optional; adjust as you like)
data/processed/
data/outputs/

# IDE
.vscode/
.idea/
"""

def main():
    root = Path(__file__).resolve().parent

    # Create folders
    for folder in FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)

    # Create files if missing
    for rel_path, content in FILES.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")

    # Write/overwrite .gitignore (safe default)
    (root / ".gitignore").write_text(GITIGNORE_CONTENT, encoding="utf-8")

    print("✅ Project structure created/updated.")

if __name__ == "__main__":
    main()
