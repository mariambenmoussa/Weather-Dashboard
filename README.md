# OpenWeather Dashboard  - Devops Challenge
## Project Overview 
This project consisys in using OpenWeather API and AWS to generate and visualize a Weather Dashboard. 
 - OpenWeather API
 - AWS S3
 - Infrastructure as Code
 - Python
 - Version Control (Git) 
 - HTML CSS

## Features 
- Fetches real-time Weather data for multiple cities.
- Displays multiple data about weather conditions.
- Stores Weather data in an AWS S3 bucket.
- Import json API data to an HTML page to visualize the weather dashboard.

## Project Structure 

Weather-Dashboard/  
  src/  
  __init__.py  
  weather_dashboard.py  
.env  
.gitignore  
requirements.txt  

## Run the project 
In a bash environment: 
1. Clone the repository:  
git clone 

3. Install dependencies:  
pip install -r requirements.txt

4. Configure environment variables (.env):  
OPENWEATHER_API_KEY=your_api_key  
AWS_BUCKET_NAME=your_bucket_name  
AWS_ACCESS_KEY_ID=your_aws_access_key_id  
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key  

(either add your AWS credentials in .env file or use the command 'aws configure' to add it directly to ~/.aws/credentials )

5. Run the application:  
python3 src/weather_dashboard.py

## Results 
HTML file generated will be pushed to your S3 bucket and you can visualize it by opening the file on your browser.   
![image](https://github.com/user-attachments/assets/326b8335-8e0a-4a6d-89b5-269250684466)


