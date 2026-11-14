# 0002. Etiquetas de dominio y área en WOS-46985

- **Estado:** aceptada
- **Fecha:** 2026-11-13

## Contexto

La clasificación es jerárquica: primero el dominio y luego el área dentro de ese dominio. Para
eso cada área debe pertenecer a **un solo** dominio. Al revisar `Meta-data/Data.xlsx` (Fase I)
se encontraron inconsistencias en las etiquetas originales:

| Problema | Ejemplo | Filas |
| --- | --- | --- |
| El id global de área `Y` aparece en dos dominios | `Y=40` *Depression*: 380 en Psychology y 130 en Medical | 3 valores de `Y` |
| `Y=76` mezcla dos áreas sin relación | *Anxiety* (Medical, 262) y *Bamboo as a Building Material* (Civil, 2) | 264 |
| El texto de `area` tiene variantes dentro de un mismo `Y` | `Y=71`: *Smart Material* (363), *Nano Concrete* (7), *Transparent Concrete* (3) | 8 valores de `Y` |
| `Domain` y `area` traen espacios sobrantes | `"CS "`, `" Computer vision  "` | todas |

`Y1` (dominio) es consistente: cada valor corresponde a un único texto de `Domain`. No hay
valores nulos ni resúmenes duplicados.

## Decisión

- **Dominio** = `Y1` (7 clases, ids 0–6).
- **Área** = el par (`Y1`, `Y`), renumerado de forma contigua como `id_area`. Así *Depression*
  de Psychology y *Depression* de Medical son dos áreas distintas, cada una bajo su dominio.
- **Nombre del área** = el texto de `area` más frecuente dentro del par. Las demás variantes se
  guardan como `alias` en `categorias.json`.
- Se descartan las áreas con menos de `datos.min_documentos_por_area` documentos (10, en
  `ml/configs/base.yaml`). Con el dataset actual solo se descarta *Bamboo as a Building
  Material* (2 filas).
- La partición 70/15/15 se estratifica por `id_area` con semilla 42.

Resultado: **46.983 documentos, 7 dominios y 136 áreas**
(train 32.888 · val 7.047 · test 7.048). Se conserva `y_original` para poder comparar con la
literatura, que reporta 134 áreas.

## Alternativas consideradas

- **Usar `Y` tal cual (134 áreas):** es lo que reporta la literatura, pero 3 áreas quedarían
  con dos dominios padre y el clasificador jerárquico no podría entrenar un modelo por dominio
  sin contradicciones.
- **Usar el texto de `area` (145 pares dominio-área):** crea clases de 1 a 7 documentos que son
  errores de etiquetado, imposibles de aprender y de estratificar.
- **Eliminar las filas de los `Y` conflictivos:** perdería ~1.150 documentos válidos de
  *Depression*, *Schizophrenia* y *Anxiety*.

## Consecuencias

- La jerarquía es consistente por construcción y se puede entrenar un clasificador de área por
  dominio.
- El número de áreas (136) difiere del citado en la propuesta (134); hay que explicarlo en el
  informe final.
- Algunas áreas siguen teniendo ruido de etiqueta (p. ej. `Y=25` mezcla *Analog signal
  processing* y *Electrical generator*). Queda documentado en los `alias` y se revisará en las
  matrices de confusión de la Fase III.
