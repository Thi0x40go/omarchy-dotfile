#!/bin/bash
status=$(playerctl status 2>/dev/null | tr -d '\r\n')
if [ -z "$status" ]; then
    # Output empty string so the module hides itself when Spotify is closed
    echo ""
    exit 0
fi

title=$(playerctl metadata title 2>/dev/null | tr -d '\r\n')
artist=$(playerctl metadata artist 2>/dev/null | tr -d '\r\n')
album=$(playerctl metadata album 2>/dev/null | tr -d '\r\n')

# Escape backslashes and double quotes for JSON safety
title=${title//\\/\\\\}
title=${title//\"/\\\"}
artist=${artist//\\/\\\\}
artist=${artist//\"/\\\"}
album=${album//\\/\\\\}
album=${album//\"/\\\"}

# Limit length of title/artist if too long
track_info="$artist - $title"
if [ ${#track_info} -gt 40 ]; then
    track_info="${track_info:0:37}..."
fi

# Use only the standard Spotify icon (no play/pause icon in the bar text)
icon=""

tooltip="󰓇  Controle do Spotify\n\n"
tooltip+="🎵 Música: $title\n"
tooltip+="👤 Artista: $artist\n"
tooltip+="💿 Álbum: $album\n\n"
tooltip+="🖱️ Controles Rápidos no Widget:\n"
tooltip+="  • Clique Esquerdo: Pausar / Retomar\n"
tooltip+="  • Scroll p/ Cima: Próxima Música\n"
tooltip+="  • Scroll p/ Baixo: Música Anterior"

# Print valid JSON for Waybar
printf '{"text": "%s %s", "tooltip": "%s"}\n' "$icon" "$track_info" "$tooltip"
