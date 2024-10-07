## SkillSync Interviewer API

### Project notes:  
 - `main.py` and `RunTests.py` set the working directory to their directory  
 - calling RunTests uses up some ElevenLabs tokens  

### Quickstart:  
 - Create and activate conda environment with `environment.yml`  
 - Install ffmpeg on your system so the ElevenLabs python package can run  
 - Create a `.env` in `api/.env` with the following:
~~~
ELEVEN_LABS_API_KEY=<api key here>
~~~
 - Run `python api/main.py` or `python api/RunTests.py`

### Testing:  
Since we have endpoints that cost a few cents per query, run `python api/RunTests.py -f` to only run free tests. Run `python RunTests.py -a` to run all tests, including the ones that incur costs.