import requests
import time
import csv
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

MARKET_SLUG = "cricipl-del-che-2026-05-05"
API_URL = f"https://gamma-api.polymarket.com/markets/slug/{MARKET_SLUG}"

last_dc = None
last_csk = None

def get_prices():
    try:
        response = requests.get(API_URL, timeout=15)
        data = response.json()
        
        # 🔥 Sabse Strong Parsing
        price_str = data.get('outcomePrices', '[]')
        
        # Clean aur parse karo
        if isinstance(price_str, str):
            # Agar '[' se start hota hai toh JSON load karo
            price_str = price_str.replace("'", '"')   # safety
            prices = json.loads(price_str)
        else:
            prices = price_str
        
        dc_raw = prices[0]
        csk_raw = prices[1]
        
        dc_price = round(float(dc_raw) * 100, 1)
        csk_price = round(float(csk_raw) * 100, 1)
        
        total = dc_price + csk_price
        volume = float(data.get('volume', 0))
        
        return dc_price, csk_price, total, volume
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print(f"[yellow]Raw Data: {data.get('outcomePrices') if 'data' in locals() else 'N/A'}[/yellow]")
        return None, None, None, None


print("🚀 DC vs CSK Polymarket Live Tracker Started...\n")

with Live(console=console, refresh_per_second=1) as live:
    while True:
        result = get_prices()
        if result[0] is None:
            time.sleep(30)
            continue
            
        dc, csk, total, volume = result
        
        current_time = datetime.now().strftime("%H:%M:%S")
        
        dc_change = f"{dc - last_dc:+.1f}¢" if last_dc is not None else "—"
        csk_change = f"{csk - last_csk:+.1f}¢" if last_csk is not None else "—"
        
        # CSV Save
        with open("prices_history.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([current_time, dc, csk, total, dc_change, csk_change])
        
        table = Table(title="🔴 DC vs 🟠 CSK | Live Tracker", title_style="bold cyan")
        table.add_column("Time", style="dim")
        table.add_column("Delhi Capitals", style="blue", justify="right")
        table.add_column("Chennai Super Kings", style="yellow", justify="right")
        table.add_column("Sum", style="green", justify="right")
        table.add_column("DC 1m", justify="right")
        table.add_column("CSK 1m", justify="right")
        table.add_column("Volume", justify="right")
        
        table.add_row(
            current_time,
            f"{dc}¢",
            f"{csk}¢",
            f"{total}¢",
            dc_change,
            csk_change,
            f"{volume:,.0f}"
        )
        
        live.update(table)
        
        last_dc = dc
        last_csk = csk
        
        time.sleep(60)
