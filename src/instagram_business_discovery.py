import requests
import json
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class InstagramBusinessDiscovery:
    """
    Instagram Business Discovery API Tool
    Used to query public information from other Business/Creator accounts.
    """
    
    def __init__(self, access_token: Optional[str] = None, business_account_id: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            access_token: Your Facebook/Instagram Access Token (defaults to env var ACCESS_TOKEN)
            business_account_id: Your own Instagram Business Account ID (defaults to env var YOUR_BUSINESS_ACCOUNT_ID)
        """
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        self.business_account_id = business_account_id or os.getenv("YOUR_BUSINESS_ACCOUNT_ID")
        self.base_url = "https://graph.facebook.com/v21.0"
        
        if not self.access_token or not self.business_account_id:
            raise ValueError("ACCESS_TOKEN and YOUR_BUSINESS_ACCOUNT_ID must be provided via init args or .env file.")
    
    def get_account_info(self, username: str, media_limit: int = 100) -> Optional[Dict]:
        """
        Get basic account info and posts for the specified account.
        
        Args:
            username: Target Instagram username (without @)
            media_limit: Number of media items to fetch per request (max 100)
            
        Returns:
            Dictionary containing account info and posts
        """
        # Define fields to fetch
        fields = [
            "business_discovery.username({username}){",
            "  id,",
            "  username,",
            "  name,",
            "  biography,",
            "  followers_count,",
            "  follows_count,",
            "  media_count,",
            "  profile_picture_url,",
            f"  media.limit({media_limit}){{",  # Configurable limit
            "    id,",
            "    caption,",
            "    like_count,",
            "    comments_count,",
            "    media_type,",
            "    media_url,",
            "    permalink,",
            "    timestamp",
            "  }",
            "}"
        ]
        
        fields_str = "".join(fields).replace("{username}", username)
        
        url = f"{self.base_url}/{self.business_account_id}"
        params = {
            "fields": fields_str,
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            if response.text:
                print(f"Error details: {response.text}")
            return None
    
    def get_all_posts(self, username: str, media_limit: int = 100) -> List[Dict]:
        """
        Get all posts (handles pagination).
        
        Args:
            username: Target Instagram username
            media_limit: Number of media items per request
            
        Returns:
            List of all posts
        """
        all_posts = []
        data = self.get_account_info(username, media_limit)
        
        if not data or "business_discovery" not in data:
            return all_posts
        
        discovery = data["business_discovery"]
        
        if "media" in discovery and "data" in discovery["media"]:
            all_posts.extend(discovery["media"]["data"])
            
            # Handle pagination
            while "paging" in discovery["media"] and "next" in discovery["media"]["paging"]:
                next_url = discovery["media"]["paging"]["next"]
                try:
                    response = requests.get(next_url)
                    response.raise_for_status()
                    page_data = response.json()
                    
                    if "data" in page_data:
                        all_posts.extend(page_data["data"])
                    
                    if "paging" not in page_data or "next" not in page_data["paging"]:
                        break
                    
                    discovery["media"] = page_data
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching paginated data: {e}")
                    break
        
        return all_posts
    
    def save_to_json(self, data: Dict, filename: str = "instagram_data.json"):
        """
        Save data to a JSON file.
        
        Args:
            data: Data to save
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")
    
    def print_summary(self, username: str, media_limit: int = 100):
        """
        Print account summary.
        
        Args:
            username: Target Instagram username
            media_limit: Number of media items to fetch
        """
        data = self.get_account_info(username, media_limit)
        
        if not data or "business_discovery" not in data:
            print("Unable to fetch account info")
            return
        
        discovery = data["business_discovery"]
        
        print(f"\n{'='*50}")
        print(f"Account: @{discovery.get('username', 'N/A')}")
        print(f"Name: {discovery.get('name', 'N/A')}")
        print(f"Followers: {discovery.get('followers_count', 0):,}")
        print(f"Following: {discovery.get('follows_count', 0):,}")
        print(f"Media Count: {discovery.get('media_count', 0):,}")
        print(f"{'='*50}\n")
        
        if "media" in discovery and "data" in discovery["media"]:
            posts = discovery["media"]["data"]
            print(f"Fetched {len(posts)} posts\n")
            
            for i, post in enumerate(posts[:5], 1):  # Show first 5 posts
                print(f"Post {i}:")
                print(f"  Likes: {post.get('like_count', 0):,}")
                print(f"  Comments: {post.get('comments_count', 0):,}")
                print(f"  Type: {post.get('media_type', 'N/A')}")
                caption = post.get('caption', '')
                if caption:
                    preview = caption[:50] + "..." if len(caption) > 50 else caption
                    print(f"  Caption: {preview}")
                print()