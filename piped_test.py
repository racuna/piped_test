import requests
from bs4 import BeautifulSoup
import subprocess

# Función personalizada para obtener un valor de clasificación que maneja "N/A"
def custom_sort_key(item):
    if item[2] == "N/A":
        return float("inf")  # Asignar un valor infinito para "N/A"
    else:
        return float(item[2])  # Convertir el tiempo de ping a un valor numérico

# URL de la página wiki
wiki_url = "https://github.com/TeamPiped/Piped/wiki/Instances"

# Realizar una solicitud GET a la página wiki
response = requests.get(wiki_url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la tabla en la página (ajusta el selector según sea necesario)
    table = soup.find('table')

    # Crear una lista para almacenar los resultados del ping
    ping_results = []

    print(f"Testing every link in the Piped wiki:")

    # Iterar a través de las filas de la tabla (ignorando la primera fila de encabezados)
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) >= 2:
            name = columns[0].text.strip()
            link = columns[1].find('a')['href']

            # Eliminar "https://" de la URL
            link = link.replace("https://", "")

            # Realizar un ping al sitio web usando la utilidad de línea de comandos ping
            ping_response = subprocess.run(["ping", "-c", "4", link], capture_output=True, text=True)

            # Extraer el tiempo promedio de ping del resultado
            ping_time = "N/A"
            if ping_response.returncode == 0:
                lines = ping_response.stdout.splitlines()
                for line in lines:
                    if "avg" in line:
                        parts = line.split("/")
                        ping_time = parts[4]
            # Imprimir el resultado en pantalla
            print(f"Name: {name}, API Link: https://{link}, Ping: {ping_time} ms")

            # Agregar el resultado del ping a la lista
            ping_results.append((name, link, ping_time))
    
    # Ordenar la lista por tiempo de ping (menor a mayor)
    # ping_results.sort(key=lambda x: x[2])
    ping_results.sort(key=custom_sort_key)

    print(f"")
    print(f"Now the sorted list:")

    # Imprimir la lista ordenada
    for result in ping_results:
        name, link, ping_time = result
        print(f"Name: {name}, API Link: https://{link}, Ping: {ping_time} ms")
else:
    print(f"Error al obtener la página: {response.status_code}")

