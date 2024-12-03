# ShelterDonationManagement

## Setup project
- Need python > 3.10
- Create python venv if needed  
   - Run `python -m venv venv`
   - Run `source venv/bin/activate` to activate the env
- Run `pip install -r requirements.txt` at the root folder to install deps

## Running locally
- Backend
  - Setup database: run `python Backend/Banco/create_tables.py`
  - Start server: run `python Backend/Rotas/routes.py`. Will launch at **localhost:5000**
  - API uses Cors to enable Front-end to fetch data

- Frontend
  - Start app: run `python Frontend/dist_server.py`. Will launch at **localhost:3000**
  - The `index.html` file is served by default. 
  - To acesses other `.html`, set the url to that file name. Ex.: `localhost:3000/register`
