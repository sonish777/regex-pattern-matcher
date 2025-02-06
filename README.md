# RegXFindAndMatch
Identify patterns in text columns using natural language input, and replace the matched patterns. It also provides the option to perform various data transformations like normalizing emails, capitalizing text fields, and formatting currency.

This project is built with the following technologies:
- **Backend**: Django, Django Rest Framework, Redis (for caching)
- **Frontend**: React, Material UI (MUI), Axios for API requests
- **AI Integration**: Hugging Face API for generating regular expressions (LLM)
  
## Pre-requisites
Before setting up the project, ensure you have the following:
- Python 3.x & pipenv
- Node.js and npm (or yarn)
- Redis
- A HuggingFace API key (for LLM integration)

## Instructions
After cloning the repository,
### 1. Install python dependencies using pipenv
```bash
pipenv install
```
### 2. In backend directory, create a .env file and copy contents of .env.example and update the variables according to your system and configuration

### 3. From the backend directory, run the following command to start the server
```bash
pipenv run python manage.py runserver
```
Once the server is running, you can access the API documentation at:
http://localhost:8000/api/docs
Server health API:
http://localhost:8000/api/health

### 4. To setup the frontend, go to frontend directory and install the dependencies
```bash
yarn install # or npm install
```

### 5. Start the frontend development server
```bash
yarn start # or npm start
```
The frontend will be served at http://localhost:3000


