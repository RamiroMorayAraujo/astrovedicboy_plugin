# Project Title

## Description

This project is a Flask-based web application that integrates Jyotish astrology with modern technology. It uses various APIs like Google Maps and Prokerala to generate astrological charts and provides detailed readings based on planetary positions. The application also uses GPT-4 to analyze and answer questions related to astrology.

## Features
- Generate Rasi charts
- Astrological analysis based on planetary positions
- User-friendly question and answer interface

## Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/astrovedicboy_function.git
    ```
2. **Navigate to the Directory**
    ```bash
    cd astrovedicboy_function
    ```
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Environment Variables**
    Create a `.env` file in the root directory and add your API keys and other environment variables.
    ```env
    GOOGLE_MAPS_API_KEY=your_key_here
    PROKERALA_API_KEY=your_key_here
    ```
5. **Run the Application**
    ```bash
    python main.py
    ```

## Usage

### Generate Rasi Chart
To generate a Rasi chart, make a POST request to `/generate_rasi` with the following parameters:

- `birth_date`: The birth date in YYYY-MM-DD format.
- `birth_time`: The birth time in HH:MM:SS format.
- `birth_city`: The city of birth.

Example:
```bash
curl -X POST "http://localhost:5000/generate_rasi" -d "birth_date=2000-01-01&birth_time=12:00:00&birth_city=New York"


## Contributing

Instructions for contributing to your project.

## License

Your project's license.
