#!/usr/bin/env python3
import datetime
import calendar
import json
import sys
import re

MONTHS_PT = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

MONTHS_SHORT_PT = ["", "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                   "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

WEEKDAYS_PT = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

# Gold color for holidays and red/brown color for today
GOLD_COLOR = "#e5c07b"
TODAY_COLOR = "#a55555"

def strip_tags(text):
    return re.sub(r'<[^>]*>', '', text)

def get_easter(year):
    # Anonymous Gregorian Algorithm
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

def get_brazilian_holidays(year):
    easter = get_easter(year)
    carnaval = easter - datetime.timedelta(days=47)
    good_friday = easter - datetime.timedelta(days=2)
    corpus_christi = easter + datetime.timedelta(days=60)
    
    holidays = {
        datetime.date(year, 1, 1): "Confraternização Universal (Ano Novo)",
        carnaval: "Carnaval",
        good_friday: "Sexta-feira Santa",
        easter: "Páscoa",
        datetime.date(year, 4, 21): "Tiradentes",
        datetime.date(year, 5, 1): "Dia do Trabalhador",
        corpus_christi: "Corpus Christi",
        datetime.date(year, 9, 7): "Independência do Brasil",
        datetime.date(year, 10, 12): "Nossa Senhora Aparecida",
        datetime.date(year, 11, 2): "Finados",
        datetime.date(year, 11, 15): "Proclamação da República",
        datetime.date(year, 11, 20): "Dia da Consciência Negra",
        datetime.date(year, 12, 25): "Natal",
    }
    return holidays

def main():
    now = datetime.datetime.now()
    today_date = now.date()
    year, month = now.year, now.month
    
    # Get holidays
    holidays = get_brazilian_holidays(year)
    holidays.update(get_brazilian_holidays(year + 1))
    
    today_holiday = holidays.get(today_date)
    
    # Generate list of holidays for the current month
    month_holidays_lines = []
    raw_lines_for_width = [
        "📅  Calendário e Feriados",
        f"✨  Feriados de {MONTHS_PT[month]} (BR):"
    ]
    if today_holiday:
        raw_lines_for_width.append(f"🎉  Hoje é Feriado: {today_holiday}")
        
    for date, name in sorted(holidays.items()):
        if date.year == year and date.month == month:
            day_str = f"{date.day:02d}"
            if date == today_date:
                line = f"  • <b><span color='{GOLD_COLOR}'>{day_str}</span></b>: <b><span color='{TODAY_COLOR}'>{name} (Hoje)</span></b>"
                raw_line = f"  • {day_str}: {name} (Hoje)"
            else:
                line = f"  • <b><span color='{GOLD_COLOR}'>{day_str}</span></b>: {name}"
                raw_line = f"  • {day_str}: {name}"
            month_holidays_lines.append(line)
            raw_lines_for_width.append(raw_line)
            
    # Calculate maximum line length to dynamically center the calendar
    max_len = max(len(strip_tags(l)) for l in raw_lines_for_width)
    if max_len < 24:
        max_len = 24
        
    # The calendar width is exactly 20 characters
    calendar_width = 20
    padding_size = max(0, (max_len - calendar_width) // 2)
    pad = " " * padding_size
    
    # Generate calendar
    cal = calendar.TextCalendar(firstweekday=6)
    month_weeks = cal.monthdayscalendar(year, month)
    
    header = f"{MONTHS_PT[month]} {year}"
    w_days = "Do Se Te Qa Qi Se Sá"
    
    calendar_lines = [
        f"{pad}<b>{header.center(calendar_width)}</b>",
        f"{pad}<b>{w_days}</b>"
    ]
    
    for week in month_weeks:
        week_str = []
        for day in week:
            if day == 0:
                week_str.append("  ")
            else:
                day_date = datetime.date(year, month, day)
                is_holiday = day_date in holidays
                
                if day == now.day:
                    if is_holiday:
                        # Today is also a holiday: bold gold with underline
                        week_str.append(f"<span color='{GOLD_COLOR}'><b><u>{day:2d}</u></b></span>")
                    else:
                        # Today only: bold theme color
                        week_str.append(f"<span color='{TODAY_COLOR}'><b>{day:2d}</b></span>")
                elif is_holiday:
                    # Holiday: gold color
                    week_str.append(f"<span color='{GOLD_COLOR}'><b>{day:2d}</b></span>")
                else:
                    week_str.append(f"{day:2d}")
        calendar_lines.append(f"{pad}{' '.join(week_str)}")
        
    calendar_markup = "<tt>" + "\n".join(calendar_lines) + "</tt>"
    
    # Assemble the final tooltip
    tooltip = "📅  Calendário e Feriados\n\n"
    tooltip += calendar_markup
    tooltip += "\n\n"
    
    if today_holiday:
        tooltip += f"🎉  <b>Hoje é Feriado: <span color='{GOLD_COLOR}'>{today_holiday}</span></b>\n\n"
        
    tooltip += f"✨  <b>Feriados de {MONTHS_PT[month]} (BR):</b>\n"
    if month_holidays_lines:
        tooltip += "\n".join(month_holidays_lines)
    else:
        tooltip += "  • Nenhum feriado nacional este mês."
        
    # Main clock text
    weekday_str = WEEKDAYS_PT[now.weekday()]
    month_str = MONTHS_SHORT_PT[month]
    time_str = f"{weekday_str}, {now.day:02d} {month_str} {now.strftime('%H:%M')}"
    
    display_text = time_str
    if today_holiday:
        display_text = f"🎉 {time_str}"
        
    output = {
        "text": display_text,
        "tooltip": tooltip
    }
    
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
