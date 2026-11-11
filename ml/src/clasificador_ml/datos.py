"""Carga y preparación del dataset WOS-46985 (Fase I, sección 5.1 del diseño).

Responsabilidades previstas:
- Leer `data/raw/WebOfScience/Meta-data/Data.xlsx`.
- Limpiar filas vacías o duplicadas y normalizar nombres de dominio y área.
- Generar `categorias.json` con la jerarquía dominio -> áreas.
- Dividir 70/15/15 estratificado por área (semilla 42) y guardar en Parquet.
"""
