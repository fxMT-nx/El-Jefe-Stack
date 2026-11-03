# Preset

- `el-jefe.patch.yml` — bloque listo para pegar al final de `$DSH_HOME/profiles/<perfil>/cordis.patch.yml`. **Redefine `standard`** (mismo id) sustituyendo su `config.plugins`: persona El Jefe + set de herramientas estándar. No declares un preset nuevo desde el patch de usuario: DSH falla con `dsh-scope: scope key is already bound to a parent` al crear sesiones.
- `mcp-browseros.example.yml` — ejemplo de capa home-level (`$DSH_HOME/cordis.patch.yml`) para conectar el MCP de BrowserOS neo. Ajusta URL/puerto.

Después de aplicarlo: recarga (HMR) o reinicia DSH y crea una sesión nueva; el chip debe decir **El Jefe**.

Para volver al standard original: borra el bloque del patch (o restaura el backup) y reinicia.