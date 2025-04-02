# TikTok Data Explorer

This Flask application scrapes TikTok video data and provides an interface to explore and analyze the data. It includes a RESTful API and a web interface for data visualization.

## Requirements

To run this application, you need to have the following Python packages installed. You can install them using the `requirements.txt` file:


### Key Dependencies:
- Flask (3.1.0) - Web framework
- Flask-SQLAlchemy (3.1.1) - ORM for database interactions
- Flask-Migrate (4.1.0) - Database migration tool
- Flask-CORS (5.0.1) - Cross-Origin Resource Sharing
- requests (2.32.3) - HTTP library for API requests
- python-dotenv (1.0.1) - Environment variable management
- psycopg2-binary (2.9.10) - PostgreSQL adapter
- gunicorn (21.2.0) - WSGI HTTP Server

## Environment Setup

Create a `.env` file in the root directory with the following variables:

```
DB_URL=
RAPIDAPI_KEY=
```

## Folder Structure

├── app.py # Main application file with Flask routes and DB models
├── .env # Environment variables (API keys, DB connection)
├── requirements.txt # Project dependencies
├── templates/ # HTML templates
│ └── index.html # Main dashboard interface



## API Functions

### 1. Scrape TikTok Data
- **Endpoint**: `/api/scrap-tiktok-data`
- **Method**: GET
- **Parameters**:
  - `keyword` - Search term for TikTok videos
  - `limit` - Number of videos per request (default: 30)
  - `max_posts` - Maximum videos to fetch (default: 200)
  - `is_save_to_db` - Whether to save results to database (default: false)
- **Response**: JSON with video details and save statistics

### 2. Retrieve Saved Posts
- **Endpoint**: `/api/posts`
- **Method**: GET
- **Description**: Returns the latest 100 TikTok posts from the database
- **Response**: JSON array of post objects including video ID, title, creator, engagement metrics, 

### 3. Monthly Statistics
- **Endpoint**: `/api/monthly-stats`
- **Method**: GET
- **Description**: Provides aggregated monthly video statistics
- **Response**: JSON array with video counts by month

## Web Interface

The application includes a web dashboard at the root URL (`/`) with two main sections:

### Posts Data Tab
- Displays a table of the latest 100 TikTok posts
- Shows video ID, title, creator, views, comments, shares, creation date, and search keyword
- Data loads automatically when the page opens

### Monthly Trends Tab
- Visualizes video post trends over time
- Uses Chart.js to display a bar chart of monthly video counts
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
- Batch processing is implemented when saving videos to improve performance
- Duplicate detection prevents saving the same video multiple times

### Data Visualization
The web interface uses Chart.js for creating interactive data visualizations. The monthly statistics chart provides insights into content trends over time. The data is dynamically fetched from the API endpoint when the chart tab is selected.

## Deployment

### Local Development
For local development, run the application using:

```
source venv/bin/activate
python app.py
```

### Deployment
Deployed on Render.
Postgres is used as the database in Render.
Flask is used as the web framework.


## Future Work
- Add more features to the web interface
- Add more analytics and insights
- Add more data visualization options
- Add more data collection options
- Add more data processing options
- Add more data storage options


## References and Acknowledgements

### Development Assistance
- **Frontend Development**: The HTML templates and frontend JavaScript logic were developed with assistance from AI tools including GPT and Claude.

### Learning Resources
- **Backend Logic**: The Flask backend implementation was informed by various web resources and the following article:
  - ["Python Flask: A Comprehensive Guide from Basic to Advanced"](https://medium.com/@moraneus/python-flask-a-comprehensive-guide-from-basic-to-advanced-fbc6ec9aa5f7) by Ran Moran on Medium

### APIs and Services
- TikTok data is collected using the TikTok Video No Watermark API via RapidAPI
- The application is deployed on Render with PostgreSQL database services

