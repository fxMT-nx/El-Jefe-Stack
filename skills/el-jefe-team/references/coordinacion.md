# Coordinación del equipo

- **Tablero:** `team_task_list` para ver; `team_task_update` con la `revision` actual, nunca una vieja. Cada tarea declara skills, herramientas, criterio de aceptación y `write_scopes`.
- **Mensajes:** `send_message` para redirigir a un miembro en marcha; `interrupt_agent` si está atascado o se sale del alcance.
- **Espera:** `wait_agent` cuando dependas de un miembro; al despertar, re-lista (`list_agents`, `team_task_list`) antes de decidir.
- **Conflictos de archivos:** secuencia con `blocked_by` o asigna un único dueño; los scopes son advisory, no un lock.
- **Sin tope de miembros:** crea los que el trabajo necesite, cada uno con una pieza disjunta y un brief autocontenido; reutiliza nombres.
