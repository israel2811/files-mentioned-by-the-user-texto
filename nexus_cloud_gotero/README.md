# NEXUS Cloud Gotero

Paquete portable para mover trabajo pesado de NEXUS fuera de la laptop.

Objetivo: que la Dell solo sincronice/controle, mientras Codespaces o GitHub
Actions procesan exports grandes, chunks, inventarios y dedup.

## Uso recomendado

1. Crea o abre un repo privado, por ejemplo `nexus-cloud-runner`.
2. Copia esta carpeta al repo.
3. Sube los exports grandes a una carpeta `input/` dentro del repo, o sincronizalos
   desde Drive con `rclone` si ya lo tienes configurado.
4. Abre Codespaces en ese repo.
5. Ejecuta los comandos por lotes:

```bash
python scripts/chatgpt_export_to_md.py --input input/chatgpt_export --output output/chatgpt_md
python scripts/chunk_text_files.py --input input/gigantes --output output/chunks --max-kb 500
python scripts/inventory_md5.py --root input/drive_snapshot --output output/inventario_completo.csv --dupes output/duplicados_md5_verificados.csv
```

## Que descarga de la PC

- Parseo de `conversations-000..005.json` de ChatGPT.
- Troceo de archivos de 10 MB a 117 MB sin pasar por el chat.
- Hash MD5/SHA256 por streaming.
- Reportes CSV reproducibles.
- Preparacion de `.md` limpios para importarlos/convetirlos a Google Docs.

## Que no descarga magicamente

- GUI Windows de Antigravity o Claude Desktop. Para eso hace falta VM Windows
  remota/RDP/Chrome Remote Desktop.
- Cookies/sesiones locales de Chrome, salvo export o navegador remoto logueado.
- `G:\Mi unidad` directo desde Codespaces. Hay que sincronizar via repo, Drive API,
  rclone o ZIP exportado.

## Regla NEXUS

No borrar permanente. Todo duplicado confirmado se reporta primero. Si se mueve,
va a `99_DUPLICADOS` o una cuarentena equivalente.

