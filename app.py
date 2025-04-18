from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from datetime import datetime
from sqlalchemy import func, extract
import os
from dotenv import load_dotenv

# environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Post model
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Text, unique=True, nullable=False)
    region = db.Column(db.Text)
    title = db.Column(db.Text)
    cover_photo = db.Column(db.Text)
    ai_dynamic_cover_photo = db.Column(db.Text)
    duration = db.Column(db.Integer)
    video_link = db.Column(db.Text)
    size = db.Column(db.Integer)
    play_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    share_count = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    download_count = db.Column(db.Integer)
    is_live = db.Column(db.Boolean, default=False)
    is_ad = db.Column(db.Boolean, default=False)
    is_shareable = db.Column(db.Boolean, default=False)
    engagement_rate = db.Column(db.Float, default=0.0)
    mentioned_users_ids = db.Column(db.JSON)
    user_id = db.Column(db.Text)
    user_unique_id = db.Column(db.Text)
    user_nickname = db.Column(db.Text)
    user_avatar = db.Column(db.Text)
    keyword = db.Column(db.Text)

    def __repr__(self):
        return f"<Post {self.video_id}>"

with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

@app.route('/')
def home():
    return render_template('index.html')

# Scrape API to fetch TikTok video posts from TikTok.
@app.route('/api/scrap-tiktok-data', methods=['GET'])
def scrap_data():
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    search_keyword = request.args.get('keyword', '')
    limit = request.args.get('limit', 30, type=int)
    max_posts = request.args.get('max_posts', 200, type=int)
    is_save_to_db = request.args.get('is_save_to_db', False, type=bool)

    publish_time = 0
    sort = 0
    has_more_posts = True
    cursor = 0
    all_posts = []
    skipped_videos = []

    while has_more_posts and len(all_posts) < max_posts:
        response = requests.get(
            f'https://tiktok-video-no-watermark2.p.rapidapi.com/feed/search'
            f'?keywords={search_keyword}&count={limit}&cursor={cursor}&publish_time={publish_time}&sort_type={sort}',
            headers=headers
        )

        try:
            post_data = response.json()
        except Exception as e:
            print(f"Error in thr parsing API: {e}")
            return jsonify({"error": "Failed to parse API response"}), 500

        videos = post_data.get('data', {}).get('videos', [])
        if not videos:
            print(" No videos found, for pagination")
            break

        for video in videos:
            try:
                # Calculate if post is shareable based on engagement metrics
                play_count = video.get('play_count', 0)
                comment_count = video.get('comment_count', 0)
                share_count = video.get('share_count', 0)
                
                # Prevent division by zero
                engagement_rate = 0
                if play_count > 0:
                    engagement_rate = (comment_count + share_count) / play_count
                
                # A post is considered shareable if:
                # 1. It has high engagement rate (>0.5%) OR
                # 2. It has very high view count (>100000)
                is_shareable = (engagement_rate > 0.005) or (play_count > 100000)
                
                all_posts.append({
                    "video_id": video.get('video_id'),
                    "region": video.get('region'),
                    "title": video.get('title'),
                    "cover_photo": video.get('cover'),
                    "ai_dynamic_cover_photo": video.get('ai_dynamic_cover'),
                    "duration": video.get('duration', 0),
                    "video_link": video.get('video_link'),
                    "size": video.get('size', 0),
                    "play_count": play_count,
                    "comment_count": comment_count,
                    "share_count": share_count,
                    "create_time": datetime.utcfromtimestamp(video.get('create_time', 0)) if video.get('create_time') else None,
                    "download_count": video.get('download_count', 0),
                    "is_live": video.get('is_live', False),
                    "is_ad": video.get('is_ad', False),
                    "is_shareable": is_shareable,
                    "engagement_rate": round(engagement_rate * 100, 2),  # Store as percentage with 2 decimal places
                    "mentioned_users_ids": video.get('mentioned_users_ids', []),
                    "user_id": video.get('author', {}).get('id'),
                    "user_unique_id": video.get('author', {}).get('unique_id'),
                    "user_nickname": video.get('author', {}).get('nickname'),
                    "user_avatar": video.get('author', {}).get('avatar'),
                    "keyword": search_keyword
                })
            except KeyError as e:
                print(f"⚠️ Skipping video due to missing key: {e}")

        print(f'Fetched {len(videos)} videos, Total Collected: {len(all_posts)}')
        cursor += 1 
        has_more_posts = post_data.get('data', {}).get('hasMore', False)

    saved_count = 0
    if is_save_to_db:
        batch_size = 10 

        for i, video in enumerate(all_posts):
            try:
                existing_post = Post.query.filter_by(video_id=video['video_id']).first()
                if not existing_post:
                    new_post = Post(**video)
                    db.session.add(new_post)
                    saved_count += 1

                    if saved_count % batch_size == 0:
                        db.session.commit()
                else:
                    skipped_videos.append(video['video_id']) 
            except Exception as e:
                print(f"Error saving video {video['video_id']}: {e}")
                print(f" Full Data: {video}")

        db.session.commit() 
        print(f"Total saved to DB: {saved_count}")
        print(f"Total skipped (already exists): {len(skipped_videos)}")
        print(f" Skipped Video IDs: {skipped_videos}")

    return jsonify({
        'results': all_posts,
        'saved_posts': saved_count if is_save_to_db else 0,
        'skipped_posts': len(skipped_videos),
        'skipped_video_ids': skipped_videos, 
    })

@app.route('/api/posts', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Get total count for pagination
    total_posts = Post.query.count()
    
    # Get paginated posts
    posts = Post.query.order_by(Post.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    results = []
    for post in posts.items:
        results.append({
            "video_id": post.video_id,
            "title": post.title,
            "user_nickname": post.user_nickname,
            "play_count": post.play_count,
            "comment_count": post.comment_count,
            "share_count": post.share_count,
            "create_time": post.create_time.strftime('%Y-%m-%d') if post.create_time else None,
            "keyword": post.keyword,
            "is_shareable": post.is_shareable,
            "engagement_rate": post.engagement_rate,
            "is_shareable": post.is_shareable
        })
    
    # Return pagination metadata along with results
    return jsonify({
        'results': results,
        'pagination': {
            'total': total_posts,
            'pages': posts.pages,
            'page': page,
            'per_page': per_page,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }
    })

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    # Get distinct keywords from the database
    keywords = db.session.query(Post.keyword).distinct().filter(Post.keyword.isnot(None)).all()
    keyword_list = []
    for k in keywords:
        keyword = k[0]
        # Only add non-empty keywords
        if keyword and keyword.strip():
            keyword_list.append(keyword)
    
    # Sort keywords alphabetically
    keyword_list.sort()

    return jsonify(keyword_list)

@app.route('/api/monthly-stats', methods=['GET'])
def get_monthly_stats():
    keyword = request.args.get('keyword', None)
    
    # Base query
    query = db.session.query(
        extract('year', Post.create_time).label('year'),
        extract('month', Post.create_time).label('month'),
        func.count(Post.id).label('count')
    ).filter(Post.create_time.isnot(None))
    
    # keyword filter if provided
    if keyword and keyword != 'all':
        query = query.filter(Post.keyword == keyword)
    
    monthly_counts = query.group_by('year', 'month').order_by('year', 'month').all()
    
    result = []
    for year, month, count in monthly_counts:
        result.append({
            "date": f"{int(year)}-{int(month):02d}",
            "count": count
        })
    
    print('result==>', result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
