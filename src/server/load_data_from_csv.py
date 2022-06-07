import requests

file_url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,sy_snum,sy_pnum,disc_year,discoverymethod,disc_facility,pl_orbper,pl_rade,pl_bmasse+from+ps&format=csv"

response = requests.get(file_url, stream=True)
# TODO: Replace later with populating mongo database

csv = open("data.csv", "wb")

for chunk in response.iter_content(chunk_size=1024):
    csv.write(chunk)

csv.close()
