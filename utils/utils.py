def generate_rasi(request):
    return "Hello, World!"
try:
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_MAPS_API_KEY'))
    print("Google Maps API Key:", os.environ.get('GOOGLE_MAPS_API_KEY'))
except ValueError:
    print("Warning: Google Maps API Key not found. Some features may not work.")
    gmaps = None


def read_and_tokenize_csv():
    # Initialize an empty list to store tokenized texts
    tokenized_texts = []
    
    # Read the CSV file
    with open('BEPINS.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Skip the header row
        next(csvreader)
        
        for row in csvreader:
            bhava = row[0]
            rasi = row[1]
            graha = row[2]
            lagna = row[3]
            graha_in_sign_in_house = row[4]
            bepins_text = row[5]
            ownership_of_graha = row[6]
            sign_in_house = row[7]
            graha_in_house = row[8]
            graha_in_sign = row[9]
            ascendant_of_chart = row[10]
            line = row[11]
            
            # Tokenize Bepin's text
            tokens = nltk.sent_tokenize(bepins_text)
            
            # Attach metadata to tokens
            for token in tokens:
                token_with_metadata = {
                    'token': token,
                    'bhava': bhava,
                    'rasi': rasi,
                    'graha': graha,
                    'lagna': lagna,
                    'graha_in_sign_in_house': graha_in_sign_in_house,
                    'ownership_of_graha': ownership_of_graha,
                    'sign_in_house': sign_in_house,
                    'graha_in_house': graha_in_house,
                    'graha_in_sign': graha_in_sign,
                    'ascendant_of_chart': ascendant_of_chart,
                    'line': line
                }
                tokenized_texts.append(token_with_metadata)
    
    return tokenized_texts

# Now, tokenized_texts contains all the tokenized sentences along with their metadata
tokenized_texts = read_and_tokenize_csv()



# Assuming tokenized_texts is a global variable or passed as an argument
# tokenized_texts = read_and_tokenize_csv()  # Uncomment this if you haven't already read the CSV

def get_tokenized_entry(planet, house, tokenized_texts):
    # This function will look up the tokenized entry for a given planet and house.
    # Loop through tokenized_texts to find relevant entries
    relevant_entries = [entry['token'] for entry in tokenized_texts if entry['graha'] == planet and entry['bhava'] == house]
    
    # Combine relevant entries into a single string
    return " ".join(relevant_entries)

def generate_astro_analysis(chart_details, tokenized_texts):
    # Step 1: Extract chart details
    planets_in_houses = chart_details.get('planets_in_houses', {})
    
    # Step 2: Query tokenized entries and general meanings
    analysis_parts = []
    for planet, house in planets_in_houses.items():
        tokenized_entry = get_tokenized_entry(planet, house, tokenized_texts)
        analysis_parts.append(tokenized_entry)
    
    # Step 3: Generate comprehensive analysis
    complete_analysis = " ".join(analysis_parts)
    
    return complete_analysis

def get_time_zone(latitude, longitude):
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=latitude, lng=longitude)
    return result

def get_coordinates(api_key, city_name):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    complete_url = f"{base_url}address={city_name}&key={api_key}"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if data['status'] == "OK":
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None, None

# Replace YOUR_API_KEY with the actual API key
api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
city_name = "New York"

latitude, longitude = get_coordinates(api_key, city_name)
if latitude and longitude:
    print(f"The coordinates for {city_name} are {latitude}, {longitude}.")
else:
    print(f"Could not get the coordinates for {city_name}.")

def convert_to_iso8601(local_date, local_time, time_zone):
    # Combine date and time into a single string
    local_datetime_str = f"{local_date} {local_time}"
    
    # Convert the string to a datetime object
    local_datetime_obj = datetime.strptime(local_datetime_str, '%Y-%m-%d %H:%M:%S')
    
    # Localize the datetime object to the given time zone
    local_tz = pytz.timezone(time_zone)
    local_datetime_obj = local_tz.localize(local_datetime_obj)
    
    # Convert to ISO 8601 format
    iso8601_datetime = local_datetime_obj.isoformat()
    
    return iso8601_datetime


def parse_date_time(birth_date, birth_time):
    date_formats = ['%d/%m/%Y', '%B %d, %Y', '%Y-%m-%d']
    time_formats = ['%I:%M %p', '%H:%M']

    for d_format in date_formats:
        try:
            birth_date = datetime.strptime(birth_date, d_format).strftime('%Y-%m-%d')
            break
        except ValueError:
            continue

    for t_format in time_formats:
        try:
            birth_time = datetime.strptime(birth_time, t_format).strftime('%H:%M:%S')
            break
        except ValueError:
            continue

    return birth_date, birth_time

# Function to read CSV and return as a list of dictionaries
def read_csv(filename):
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return [row for row in csv_reader]

# Function to write list of dictionaries to CSV
def write_csv(filename, fieldnames, data):
    with open(filename, mode='w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)



# Function to update a row in the CSV by id
def update_csv_row(filename, fieldnames, text_id, new_data):
    rows = read_csv(filename)
    for row in rows:
        if int(row['id']) == text_id:
            row.update(new_data)
            write_csv(filename, fieldnames, rows)
            return True
    return False

# Function to delete a row in the CSV by id
def delete_csv_row(filename, text_id):
    rows = read_csv(filename)
    for row in rows:
        if int(row['id']) == text_id:
            rows.remove(row)
            write_csv(filename, ['id', 'title', 'content'], rows)
            return True
    return False

def get_access_token():
    token_url = "https://api.prokerala.com/token"
    payload = {
        "client_id": PROKERALA_CLIENT_ID,
        "client_secret": PROKERALA_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "public"
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        json_response = response.json()
        access_token = json_response.get("access_token")
        return access_token
    else:
        return None


def get_rasi_chart(access_token, latitude, longitude, birth_datetime_iso8601, retries = 3):
    try:  # Start of try block
        # Prokerala API endpoint for Rasi chart
        rasi_chart_url = "https://api.prokerala.com/v2/astrology/chart"

        # Prepare headers and payload
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "datetime": birth_datetime_iso8601,
            "ayanamsa": 1,  # or 3 or 5 based on your requirement
            "coordinates": f"{latitude},{longitude}",
            "chart_type": "rasi",  # or any other type from the allowed list
            "chart_style": "north-indian",  # or "south-indian" or "east-indian"
        }

        print(f"Access Token: {access_token}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Birth Datetime: {birth_datetime_iso8601}")

        # Make the API call
        response = requests.get(rasi_chart_url, headers=headers, params=payload)

        print("API Response Text:", response.text)
        print("API Response Status Code:", response.status_code)

        # Check if the request was successful
        if response.status_code == 200:
            # Save SVG to a file
            with open("rasi_chart.svg", "w") as f:
                f.write(response.text)
            return {'success': 'SVG saved to rasi_chart.svg'}
        if response.status_code == 429 and retries > 0:
            print("Rate limit exceeded. Retrying...")
            time.sleep(60)
            return get_rasi_chart(access_token, latitude, longitude, birth_datetime_iso8601, retries-1)
        elif response.status_code == 429:
            print("Rate limit exceeded. Waiting for 60 seconds before retrying.")
            time.sleep(60)
            return get_rasi_chart(access_token, latitude, longitude, birth_datetime_iso8601)  # Recursive call
        
        else:
            return {'error': f'Failed to get Rasi chart from Prokerala API. Status Code: {response.status_code}'}
        
    except Exception as e:
        print(f"An exception occurred: {e}")
        return {'error': 'An exception occurred while fetching the Rasi chart'}



def get_rasi_chart_from_user_input(birth_date, birth_time, birth_city):
    return get_rasi_chart_from_prokerala(birth_date, birth_time, birth_city)


def get_rasi_chart_from_prokerala(birth_date, birth_time, birth_city):
    # Get coordinates for the birth city
    latitude, longitude = get_coordinates(api_key, birth_city)
    if latitude and longitude:
        # Get time zone based on coordinates
        time_zone = get_time_zone(latitude, longitude)
        
        # Convert birth date and time to ISO 8601 format
        birth_datetime_iso8601 = convert_to_iso8601(birth_date, birth_time, time_zone)
        
        # Get access token from Prokerala API
        access_token = get_access_token()
        
        # Fetch Rasi Chart using the coordinates and ISO 8601 datetime
        rasi_chart = get_rasi_chart(access_token, str(latitude), str(longitude), birth_datetime_iso8601)
        
        return rasi_chart
    else:
        return {'error': 'Failed to get coordinates or time zone'}


def ask_question():
    # Get user's birth details and question from the request
    birth_date = request.form.get('birth_date')
    birth_time = request.form.get('birth_time')
    birth_city = request.form.get('birth_city')
    question = request.form.get('question')
    
    # Parse and format the date and time
    birth_date, birth_time = parse_date_time(birth_date, birth_time)

    # Validate the received data (you can add more validations)
    if not all([birth_date, birth_time, birth_city, question]):
        return jsonify({'error': 'All fields are required'}), 400
    
    # Call Prokerala API to get Rasi chart (you'll write this function)
    rasi_chart = get_rasi_chart_from_prokerala(birth_date, birth_time, birth_city)
    
    # Analyze the Rasi chart and search the database for relevant texts (you'll write this function)
    answer = analyze_rasi_and_search_db(rasi_chart, question)
    
    return jsonify({'question': question, 'answer': answer})



def standardize_birth_details(raw_details):
    # Initialize an empty dictionary to store the standardized details
    standardized_details = {}
    
    # Extract date using regular expressions
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', raw_details)
    if date_match:
        standardized_details['date'] = date_match.group(1)
    
    # Extract time using regular expressions
    time_match = re.search(r'(\d{2}:\d{2}:\d{2})', raw_details)
    if time_match:
        standardized_details['time'] = time_match.group(1)
    
    # Extract city name (assuming it's a single word for simplicity)
    city_match = re.search(r'([a-zA-Z]+)', raw_details)
    if city_match:
        standardized_details['city'] = city_match.group(1)
    
    return standardized_details


def extract_birth_details(raw_details):
    # Regular expression pattern to match Month Day, Year, Time, City, Country
    pattern = r"([a-zA-Z]+ \d{1,2}, \d{4}), (\d{1,2}:\d{1,2}), ([a-zA-Z\s]+), ([a-zA-Z\s]+)"
    
    match = re.search(pattern, raw_details)
    
    if match:
        date = match.group(1)
        time = match.group(2)
        city = match.group(3)
        country = match.group(4)
        return date, time, city, country
    else:
        return None

# Test the function
raw_details = "June 30, 1976, 16:00, Buenos Aires, Argentina"
result = extract_birth_details(raw_details)
print(result)



def analyze_rasi_and_search_db(rasi_chart, question):
    # Step 1: Initial Filtering based on Rasi Chart
    # This could be a database query or some other logic to narrow down the texts
    relevant_texts = initial_filtering(rasi_chart)
    
    # Step 2: GPT Analysis on the filtered texts
    # This is where you'd call GPT to read through the relevant_texts and answer the question
    answer = gpt_analysis(relevant_texts, question)
    
    return answer

def initial_filtering(rasi_chart):
    # Your logic to filter texts based on rasi_chart
    relevant_texts = []
    
    # Read from the CSV file
    with open('BEPINS.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        
        # Skip the header row
        next(csvreader)
        
        for row in csvreader:
            title = row[0]  # Assuming the title is in the first column
            content = row[1]  # Assuming the content is in the second column
            
            # Example: Filtering based on Rasi (replace 'Aries' with actual data)
            if 'Aries' in title:  # Replace this condition based on your actual logic
                relevant_texts.append((title, content))
    
    return relevant_texts

def gpt_analysis(relevant_texts, question):
    # Your logic to use GPT for further analysis
    # Make an API call to a GPT service here (you'll need to set this up)
    # For now, let's assume you have a function called `call_gpt_service` that does this
    
    answer = call_gpt_service(relevant_texts, question)
    return answer

def call_gpt_service(relevant_texts, question):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    # Combine relevant texts and question for GPT to analyze
    prompt = f"Based on the following texts: {relevant_texts}, what is the answer to: {question}?"
    
    # Make the API call
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=100
    )
    
    # Extract and return the generated text
    answer = response.choices[0].text.strip()
    return answer