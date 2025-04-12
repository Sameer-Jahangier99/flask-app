import unittest
from unittest.mock import patch
import json
from datetime import datetime
from app import app

class TestTikTokScraper(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
    
    @patch('requests.get')
    def test_all_posts_append(self, mock_get):
        sample_response = {
            "data": {
                "videos": [
                    {
                        "video_id": "123456789",
                        "region": "US",
                        "title": "Test TikTok Video",
                        "cover": "https://example.com/cover.jpg",
                        "ai_dynamic_cover": "https://example.com/dynamic.jpg",
                        "duration": 30,
                        "video_link": "https://example.com/video.mp4",
                        "size": 1024,
                        "play_count": 1000,
                        "comment_count": 50,
                        "share_count": 25,
                        "create_time": 1654321098,  # Unix timestamp
                        "download_count": 10,
                        "is_live": False,
                        "is_ad": False,
                        "mentioned_users_ids": ["user1", "user2"],
                        "author": {
                            "id": "user123",
                            "unique_id": "testuser",
                            "nickname": "Test User",
                            "avatar": "https://example.com/avatar.jpg"
                        }
                    }
                ],
                "hasMore": False
            }
        }
        
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = sample_response
        mock_get.return_value = mock_response
        
        response = self.app.get('/api/scrap-tiktok-data?keyword=test&limit=1&max_posts=1&is_save_to_db=false')
        
        data = json.loads(response.data)
        self.assertTrue(len(data['results']) > 0)
        

        post = data['results'][0]
        self.assertEqual(post['video_id'], "123456789")
        self.assertEqual(post['title'], "Test TikTok Video")
        self.assertEqual(post['user_nickname'], "Test User")
        self.assertEqual(post['play_count'], 1000)
        self.assertEqual(post['keyword'], "test")
        
       
        print("Test passed! The all_posts.append function works correctly!")

if __name__ == '__main__':
    unittest.main() 