# TikTok Data Explorer

This app collects TikTok video info. You can find and explore videos in two ways:
1. Through code (API)
2. With our simple website
You can browse videos and look at basic stats like views and comments.

## Requirements

Install these libraries with the command:
pip install -r requirements.txt

Libraries:
- Flask - version(3.1.0)
- Flask-SQLAlchemy - version(3.1.1)
- Flask-Migrate -  version(4.1.0)
- Flask-CORS - version(5.0.1) 
- requests -  version(2.32.3) 
- python-dotenv - version(1.0.1)
- psycopg2-binary -  version(2.9.10) 
- gunicorn -  version(21.2.0)

## Setup

Make a file named .env in your main folder. Put this in it:

```
DB_URL=your_db_url
RAPIDAPI_KEY=your_apid_api_key

```

##  Files
app.py - The main program that runs everything
.env - Secret Variables
requirements.txt - List of needed programs
templates/index.html - Layout of the website.



## All Requests.

### 1. Scrape TikTok Videos
- **Endpoint**: `/api/scrap-tiktok-data`
-  **Method**: GET
- **Parameters**:
  - `keyword`       - Words to search for
  - `limit`         - How many videos per request (starts at 30)
  - `max_posts`     - Total videos to collect (starts at 200)
  - `is_save_to_db` - Should we save to database? (starts at no)

### 2. Retrieve Saved Posts
- **Endpoint**: `/api/posts`
- **Method**: GET
- **Parameters**:
  - `page` - Page number for pagination (default: 1)
  - `per_page` - Number of posts per page (default: 10)

### 3. List Available Keywords
- **Endpoint**: `/api/keywords`
- **Method**: GET
- **Description**: Returns a list of distinct keywords used in the database

### 4. Monthly Statistics
- **Endpoint**: `/api/monthly-stats`
- **Method**: GET
- **Parameters**:
  - `keyword` - Optional filter for specific keyword (default: all)

## Web Interface

The application includes a web dashboard at the root URL (`/`) with two main sections:

### Posts Data Tab
- Displays a paginated table of TikTok posts
- Shows video ID, title, creator, views, comments, shares, creation date, and search keyword
- Includes pagination controls (previous/next page, items per page selector)
- Displays total post count and current page information

### Monthly Trends Tab
- Visualizes video post trends over time
- Uses Chart.js to display a bar chart of monthly video counts
- Includes keyword filter to view trends for specific search terms
- Responsive design that adapts to window size

## Running the Application
1. Install dependencies: `pip install -r requirements.txt`
2. Set up your `.env` file with necessary credentials
3. Activate the virtual environment: `source venv/bin/activate`
4. Start the application: `python app.py`
5. Access the dashboard at: `http://localhost:5000`

## Database Schema

The `Post` model schema includes the following key fields:

### Primary Keys and Identifiers
- `id`: Integer, primary key for the post record
- `video_id`: Text, unique identifier for the TikTok video (non-nullable)

### Video Metadata
- `title`: Text, title or caption of the video
- `region`: Text, geographic region where the video was created
- `duration`: Integer, length of the video in seconds
- `size`: Integer, file size of the video
- `video_link`: Text, URL to the video content
- `create_time`: DateTime, when the video was created
- `is_live`: Boolean, indicates if the video is a live stream
- `is_ad`: Boolean, indicates if the video is an advertisement

### Visual Assets
- `cover_photo`: Text, URL to the video's thumbnail
- `ai_dynamic_cover_photo`: Text, URL to AI-generated dynamic cover

### Engagement Metrics
- `play_count`: Integer, number of video views
- `comment_count`: Integer, number of comments
- `share_count`: Integer, number of shares
- `download_count`: Integer, number of downloads

### Creator Information
- `user_id`: Text, TikTok user ID of the creator
- `user_unique_id`: Text, unique username of the creator
- `user_nickname`: Text, display name of the creator
- `user_avatar`: Text, URL to the creator's profile picture

### Additional Data
- `mentioned_users_ids`: JSON, array of user IDs mentioned in the video
- `keyword`: Text, search term used to find this video

## Technical Details

### Data Collection Process
The application uses the TikTok Video No Watermark API via RapidAPI to fetch video data. The API supports pagination through cursor-based navigation, allowing the application to collect large datasets. Videos are collected based on search keywords and can be filtered by publish time and sort type.

### Database Integration
- The application uses SQLAlchemy ORM to interact with a PostgreSQL database
- Database tables are automatically created at application startup if they don't exist
- Batch processing is implemented when saving videos to improve performance (batches of 10)
- Duplicate detection prevents saving the same video multiple times

### Data Visualization
The web interface uses Chart.js for creating interactive data visualizations. The monthly statistics chart provides insights into content trends over time, with the ability to filter by specific keywords.

## Deployment

### Local Development
For local development, run the application using:

```
source venv/bin/activate
python app.py
```

### Production Deployment
The application is deployed on Render with PostgreSQL as the database service. For production deployment:

1. Set `DB_URL` to your production PostgreSQL connection string
2. Configure environment variables in Render dashboard
3. Deploy with Gunicorn as the WSGI server:
   ```
   gunicorn app:app
   ```

## Future Work
- Will Add more advanced analytics and insights
- Implement user authentication for data access control
- Add export functionality for data in various formats
- Develop more detailed creator and keyword analytics
- Add automated data collection scheduling
- Implement natural language processing for content analysis

## References and Acknowledgements

### Development Assistance
The HTML templates and frontend Html, CSS, JavaScript logic were developed with assistance from AI tools GPT.

### Learning Resources
  Chart.js -  ["Chart.js: Step-by-step guide"](https://www.chartjs.org/docs/latest/getting-started/usage.html)
  Medium - ["Python Flask: A Comprehensive Guide from Basic to Advanced"](https://medium.com/@moraneus/python-flask-a-comprehensive-guide-from-basic-to-advanced-fbc6ec9aa5f7) by Ran Moran on Medium

### APIs and Services
- TikTok data is collected using the TikTok Video No Watermark API via RapidAPI
- The application is deployed on Render with PostgreSQL database services

# Understanding the Test App

The test_app.py file is a special program that checks if our TikTok Data Explorer works correctly. Let's see how it works!

## Testing Documentation for Grade 8 Students

When programmers build apps, they need to make sure everything works properly. That's where testing comes in! The `test_app.py` file is like a teacher checking a student's work - it makes sure our TikTok app does what it's supposed to do.

### What Does This Test Do?

This test checks if our app can:
1. Pretend to search TikTok for videos (without actually connecting to TikTok)
2. Return the correct information about videos
3. Format the data in the right way

### How It Works

1. The test creates a "fake" TikTok video response with all the information a real video would have
2. It tells the app to use this fake data instead of connecting to the real TikTok
3. It asks the app to search for videos with the keyword "test"
4. It checks if the app returned the correct video information

If everything works right, the test prints: "Test passed! The all_posts.append function works correctly!"

### Live Links:
Website: https://flask-app-jsl7.onrender.com/
Presentation URL: https://docs.google.com/presentation/d/17KeCPIES9Zf3lQfr63Sgv73-eoyVNdI5A7HXzOanA0k/edit?usp=sharing