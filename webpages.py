import uasyncio as asyncio
#import usocket as socket

class Webpage:
    https = {}
    port = None
    _404 = """<!DOCTYPE html>
    <html><body><h1>404</h1><p>Page not found.</p></body></html>"""
    
    def __init__(self, page, ip, name='', port=80):
        if Webpage.port == None:
            Webpage.port = port
        self.page = page
        self.ip = ip
        self.name = name
        self.http = f'http://{self.ip}{self.name}:{Webpage.port}'
        Webpage.https[self.name] = self.page
        print(f"Server running on {self.http}")
        
    def update_page(self, new):
        self.page = new
        Webpage.https[self.name] = self.page
    
    async def __handle_client(reader, writer):
        try:
            request_line = await reader.readline()
            if not request_line:
                await writer.aclose()
                return

            # Read and discard the rest of the HTTP headers
            while True:
                header = await reader.readline()
                if header == b"\r\n" or not header:
                    break
            request_path = request_line.decode('utf-8').split(' ')[1]
            request_path = request_path.split(':')[0]
            if request_path in list(Webpage.https.keys()):
                response = Webpage.https[request_path]
            else:
                response = Webpage._404
            # Send the HTML response
            await writer.awrite(response)
            await writer.aclose()

        except Exception as e:
            print("Client handling error:", e)
            try:
                await writer.aclose()
            except:
                pass
    
    async def start():
        # Create an asyncio server using usocket
        server = await asyncio.start_server(Webpage.__handle_client, "0.0.0.0", Webpage.port)
        await server.wait_closed()