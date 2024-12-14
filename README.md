# ShelterDonationManagement

## Setup project
- Need python > 3.10
- Create python venv if needed  
   - Run `python -m venv venv`
   - Run `source venv/bin/activate` to activate the env
- Run `pip install -r requirements.txt` at the root folder to install deps

- Need Node > 20
   - Go to Frontend folder and install deps: `cd Frontend && npm i`

## Running locally
- Backend
  - Setup database: run `python Backend/Banco/create_tables.py`
  - Start server: run `python Backend/Rotas/routes.py`. Will launch at **localhost:5000**
  - API uses Cors to enable Front-end to fetch data

- Frontend
  - Start app: run `python Frontend/server.py`. Will launch at **localhost:3000**
  - The `home.html` file is served by default.
  - To acesses other `.html`, set the url to that file name. Ex.: `localhost:3000/index.html`

## Formating code
- Backend: On root folder, run `black Backend`. For lines that are too long, add `  # noqa: E501` at the EOL
- Frontend: On Frontend folder, run `npm i && npm run lint-fix`

## Testing project & code format
> [!NOTE]
> Once you open a PR, a CI workflow will perform tests and validate code format
> If the requirements are not met, you will not be able to merge into `main`
> You can run those validations locally to avoid multiple commits to fix those issues
- Option 1: Will need docker installed (better)
   - At the root folder, simply
      - Run `docker build -t code-format-check .` to build local test image. The build process may take a while
      - Run `docker run --rm code-format-check` to execute the image with Docker

- Option 2: No docker required
   - To run api tests: On the root folder, run: `python Backend/**/*tests.py`
   - To run api code format: On the root folder, run: `flake8 Backend`
   - To run frontend code format: On the Frontend folder, run: `npm run lint`

If you choose to run with docker, if all tests pass you will se a screen like below


<img width="563" alt="tests" src="https://github.com/user-attachments/assets/5c6ac8f2-877f-46f0-a7c6-51f0d438922d" />
