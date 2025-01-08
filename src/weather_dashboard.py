import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            # Simpler creation for us-east-1
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # "units": "imperial" for Fahrenheit
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
            weather_data['city'] = city  # Add city name to the data
            print(f"Fetched data for {city}: {weather_data}")  # Debugging: print weather data
            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        
    def save_to_s3(self, weather_data, city):
        """Save weather data to S3 bucket"""
        if not weather_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"
        
        try:
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

    def generate_html(self, weather_data):
            """Generate an HTML file to visualize weather data"""
            html_content = """
            <html>
            <head>
                <title>Weather Dashboard</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f4f4f4; }
                </style>
            </head>
            <body>
                <h1>Weather Dashboard</h1>
                <table>
                    <tr>
                        <th>City</th>
                        <th>Temperature (°C)</th>
                        <th>Feels Like (°C)</th>
                        <th>Conditions</th>
                        <th>Humidity (%)</th>
                        <th>Wind Speed (m/s)</th>
                        <th>Timestamp</th>
                    </tr>
            """
            for data in weather_data:
                html_content += f"""
                    <tr>
                        <td>{data['name']}</td>
                        <td>{data['main']['temp']}</td>
                        <td>{data['main']['feels_like']}</td>
                        <td>{data['weather'][0]['description']}</td>
                        <td>{data['main']['humidity']}</td>
                        <td>{data['wind']['speed']}</td>
                        <td>{data['timestamp']}</td>
                    </tr>
                """
            html_content += """
                </table>
            </body>
            </html>
            """
            
            html_file_path = "weather_dashboard.html"
            with open("weather_dashboard.html", "w") as file:
                file.write(html_content)
            print("HTML file generated: weather_dashboard.html")
            return html_file_path
    
    def save_html_to_s3(self, html_file_path):
        """Save the HTML file to the S3 bucket"""
        file_name = "weather-dashboard.html"
        try:
            with open(html_file_path, "rb") as file:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=file_name,
                    Body=file,
                    ContentType='text/html'
                )
            print(f"HTML file successfully uploaded to S3: {file_name}")
        except Exception as e:
            print(f"Error uploading HTML to S3: {e}")



def main():
    dashboard = WeatherDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = ["Rabat", "Ottawa", "Tokyo"]
    weather_data_list = [ ]
    
    for city in cities:
        print(f"\nFetching weather for {city}...")
        weather_data = dashboard.fetch_weather(city)
        if weather_data:
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            print(f"Temperature: {temp}°C")
            print(f"Feels like: {feels_like}°C")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            
            # Save to S3
            success = dashboard.save_to_s3(weather_data, city)
            if success:
                print(f"Weather data for {city} saved to S3!")
                weather_data['city'] = city  # Add city name for visualization
                weather_data_list.append(weather_data)
        else:
            print(f"Failed to fetch weather data for {city}")
    
    # Generate HTML file
    html_file_path = dashboard.generate_html(weather_data_list)
    # Save HTML to S3
    dashboard.save_html_to_s3(html_file_path) 


if __name__ == "__main__":
    main()