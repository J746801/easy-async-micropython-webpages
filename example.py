import uasyncio as asyncio
from webpages import *

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig('<YOUR_OPTIONAL_IPCONFIG>')# Recommended to set a static ip
wlan.connect('<YOUR_SSID>', '<YOUR_PASSWORD>')
# Wait for connect or fail
wait = 30
while wait > 0 and wlan.status() != 3 and wlan.isconnected() == False:
    wait -= 1
    print('waiting for connection...', wlan.status())
    time.sleep(0.5)

temp_html = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Temperature: 72 Degrees</h1>
    </body>
    </html>
    """

hum_html = f"""
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Humidity: 35%</h1>
    </body>
    </html>
    """

page = Webpage(temp_html, '192.168.4.219', '/temperature') # IP address and extention. The http would be http://192.168.4.219/temperature (page.http)
html = Webpage(hum_html, '192.168.4.219', '/humidity')
# Run the event loop
async def other_task():
    while True:
        paths = tuple(Webpage.https.keys()) # A Webpage.https is a dictonary of all pages hosted
        print(f'Webpages: http://192.168.4.219{paths[0]} and http://192.168.4.219{paths[1]}')
        await asyncio.sleep_ms(1000)

try:
    async def ALL():
        t1 = asyncio.create_task(Webpage.start())
        t2 = asyncio.create_task(other_task())
        await asyncio.gather(t1, t2)
    asyncio.run(ALL())
except KeyboardInterrupt:
    print("Server stopped")
