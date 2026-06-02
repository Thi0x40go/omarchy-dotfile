#!/bin/bash
state=$(hyprctl hyprmodoro:getState 2>/dev/null | tr -d '\r\n')
time=$(hyprctl hyprmodoro:getTime 2>/dev/null | tr -d '\r\n')
progress=$(hyprctl hyprmodoro:getProgress 2>/dev/null | tr -d '\r\n')

if [ -z "$state" ]; then
    state="STOPPED"
fi
if [ -z "$time" ]; then
    time="00:00"
fi
if [ -z "$progress" ]; then
    progress="0.0"
fi

# Calculate percentage and progress bar using awk
percent=$(awk -v p="$progress" 'BEGIN { printf "%.0f", p * 100 }' 2>/dev/null)
if [ -z "$percent" ]; then
    percent=0
fi

# Limit percentage within 0-100
if [ "$percent" -lt 0 ]; then percent=0; fi
if [ "$percent" -gt 100 ]; then percent=100; fi

bar_size=10
filled=$(awk -v p="$progress" -v size="$bar_size" 'BEGIN { printf "%.0f", p * size }' 2>/dev/null)
if [ -z "$filled" ]; then
    filled=0
fi
if [ "$filled" -lt 0 ]; then filled=0; fi
if [ "$filled" -gt "$bar_size" ]; then filled="$bar_size"; fi

empty=$((bar_size - filled))
bar=""
for ((i=0; i<filled; i++)); do bar+="█"; done
for ((i=0; i<empty; i++)); do bar+="░"; done

case "$state" in
    "WORKING")
        icon="🍅"
        desc="Foco (Trabalhando)"
        ;;
    "RESTING")
        icon="☕"
        desc="Descanso"
        ;;
    "FINISHED")
        icon="🏁"
        desc="Finalizado"
        ;;
    *)
        icon="⏸️"
        desc="Parado / Pausado"
        ;;
esac

# Build rich tooltip (changing <min> to [min] to prevent Pango Markup errors)
tooltip="⏱️  Hyprmodoro\n\n"
tooltip+="Estado: $desc\n"
tooltip+="Tempo: $time\n"
tooltip+="Progresso: [$bar] $percent%\n\n"
tooltip+="🖱️ Controles Rápidos:\n"
tooltip+="  • Clique Esquerdo: Pausar / Retomar\n"
tooltip+="  • Clique Direito: Pular Sessão\n\n"
tooltip+="⌨️ Comandos Disponíveis (hyprctl):\n"
tooltip+="  • dispatch hyprmodoro:start          - Iniciar timer\n"
tooltip+="  • dispatch hyprmodoro:stop           - Parar timer\n"
tooltip+="  • dispatch hyprmodoro:pause          - Pausar/Despausar\n"
tooltip+="  • dispatch hyprmodoro:skip           - Pular sessão\n"
tooltip+="  • dispatch hyprmodoro:set [min]      - Def. tempo de foco\n"
tooltip+="  • dispatch hyprmodoro:setRest [min]  - Def. tempo de descanso"

# Print valid JSON for Waybar
printf '{"text": "%s %s", "tooltip": "%s"}\n' "$icon" "$time" "$tooltip"
