# Bio-Internships

Tool for biology internship searches. 

Make sure to have at least python3/pip for the backend and node/npm for the frontend.

## Setup

### Create a `.env` file

```bash
cp .env.demo .env
```

### Install backend dependencies

**optional** unix users may want to create a venv first:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install all python dependencies:

```bash
pip install -r requirements.txt
```

## Run App

### Reset the database (required the first time):

```bash
python scripts/db_reset.py
```
**note** This will also start the database

### Start/Stop the app in developpement mode:

```bash
python scripts/dev_start.py
```

- Backend URL: http://127.0.0.1:8000/  
- Frontend URL: http://localhost:5173/

Both the backend and frontend will have auto-reload enabled.

Use `CTRL-C` to stop the dev mode (backend, frontend, and databases).

### Start/Stop the app in production mode:

Make sure to remove `DEBUG=1` for real production…

```bash
python scripts/prod_start.py
```

- Backend URL: http://127.0.0.1:8000/  
- Frontend URL: http://localhost:8080/

To stop the production app:

```bash
python scripts/prod_stop.py
```

### Start/Stop the database:

```bash
python scripts/db_start.py
```

```bash
python scripts/db_stop.py
```


## About the use of Qwen

If you want to use Qwen for PDF processing:

Run `pip install -r requirements-qwen.txt` and set `QWEN_ENABLED=1` in the .env file. Then start dev or prod server. Qwen Chat API will be available at `http://localhost:8888`.

We compared various language models to meet our automation needs when a user uploads a job offer PDF:
- Extracting its title
- Extracting its summary
- Extracting its scientific disciplines
- Extracting its start/end dates

We also believe it's better to use a **multilingual model**, as some researchers may still want to post apprenticeship offers in their native languages.

Our test machine was:
- **i3 8100**
- **GTX 980 4GB**
- **16 GB DDR4** 

We tried the following:

- **Summarization-only models**, like Google's mT5_multilingual_XLSum and Pegasus-XSum, but the lack of flexibility in such models made it impossible to handle all our requirements in a single request (especially for extracting scientific disciplines). Additionally, it was very slow—about 30 seconds on a CPU—and impractical on our small GPU.

- **deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B**, but it was still running on the CPU, exceeded our 4GB VRAM limit, and took too long for our needs : we didn't need its thinking ability as the problems listed above are simple. However, it was incredibly good considering its size in terms of results.

- **Qwen2.5-0.5B-Instruct**, this model fits within our GPU’s capabilities. It passed some of our tests and was able to handle direct JSON formatting, but we preferred to manage the formatting ourselves to let the model focus on its task. However, keywords and dates extraction were not working as expected.

- **Qwen2.5-3B-Instruct** with **4b quantization**, which performed better for keyword extraction and date extraction. For these tasks, we used direct JSON string output from the LLM when outputing lists like keywords and dates to ensure more predictable behavior.

We took **Qwen2.5-3B-Instruct** with **4b quantization**. A PDF processing took around **10 seconds** in our benchmarks. nvtop reported low CPU/RAM usage and around **3.5 GB of VRAM** used while processing PDF.

It would be interesting to integrate **European Skills, Competences, Qualifications, and Occupations (ESCO)** data to enhance the accuracy and efficiency of automatic processing.

## About the use of Biobert

Biobert is used to perform smart searches on all pdf.


Run `pip install -r requirements-biobert.txt` and set `BIOBERT_ENABLED=1` in the .env file. Then start dev or prod server. Biobert API will be available at `http://localhost:8889`.

## Project Contributors

### Frontend
- El Khedim Ilyes
- Charlotte Ruiz

### Backend
- El Ouarrad Mariam
- Marc Faussurier
- Atamna Miryam
