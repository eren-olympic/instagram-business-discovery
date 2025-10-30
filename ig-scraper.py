import requests
import json
from typing import Dict, List, Optional


class InstagramBusinessDiscovery:
    """
    Instagram Business Discovery API 工具
    用來查詢其他 Business/Creator 帳號的公開資訊
    """
    
    def __init__(self, access_token: str, your_business_account_id: str):
        """
        初始化
        
        Args:
            access_token: 你的 Facebook/Instagram Access Token
            your_business_account_id: 你自己的 Instagram Business Account ID
        """
        self.access_token = access_token
        self.business_account_id = your_business_account_id
        self.base_url = "https://graph.facebook.com/v21.0"
    
    def get_account_info(self, username: str) -> Optional[Dict]:
        """
        取得指定帳號的基本資訊和所有貼文
        
        Args:
            username: 目標 Instagram 帳號的用戶名稱（不含 @）
            
        Returns:
            包含帳號資訊和貼文的字典
        """
        # 定義要取得的欄位
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
            "  media.limit(100){",  # 一次最多取 100 筆
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
            print(f"API 請求錯誤: {e}")
            if response.text:
                print(f"錯誤詳情: {response.text}")
            return None
    
    def get_all_posts(self, username: str) -> List[Dict]:
        """
        取得所有貼文（處理分頁）
        
        Args:
            username: 目標 Instagram 帳號的用戶名稱
            
        Returns:
            所有貼文的列表
        """
        all_posts = []
        data = self.get_account_info(username)
        
        if not data or "business_discovery" not in data:
            return all_posts
        
        discovery = data["business_discovery"]
        
        if "media" in discovery and "data" in discovery["media"]:
            all_posts.extend(discovery["media"]["data"])
            
            # 處理分頁（如果有 next）
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
                    print(f"取得分頁資料時發生錯誤: {e}")
                    break
        
        return all_posts
    
    def save_to_json(self, data: Dict, filename: str = "instagram_data.json"):
        """
        將資料儲存為 JSON 檔案
        
        Args:
            data: 要儲存的資料
            filename: 檔案名稱
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"資料已儲存至 {filename}")
    
    def print_summary(self, username: str):
        """
        印出帳號摘要資訊
        
        Args:
            username: 目標 Instagram 帳號的用戶名稱
        """
        data = self.get_account_info(username)
        
        if not data or "business_discovery" not in data:
            print("無法取得帳號資訊")
            return
        
        discovery = data["business_discovery"]
        
        print(f"\n{'='*50}")
        print(f"帳號: @{discovery.get('username', 'N/A')}")
        print(f"名稱: {discovery.get('name', 'N/A')}")
        print(f"粉絲數: {discovery.get('followers_count', 0):,}")
        print(f"追蹤數: {discovery.get('follows_count', 0):,}")
        print(f"貼文數: {discovery.get('media_count', 0):,}")
        print(f"{'='*50}\n")
        
        if "media" in discovery and "data" in discovery["media"]:
            posts = discovery["media"]["data"]
            print(f"已取得 {len(posts)} 筆貼文\n")
            
            for i, post in enumerate(posts[:5], 1):  # 只顯示前 5 筆
                print(f"貼文 {i}:")
                print(f"  按讚數: {post.get('like_count', 0):,}")
                print(f"  留言數: {post.get('comments_count', 0):,}")
                print(f"  類型: {post.get('media_type', 'N/A')}")
                caption = post.get('caption', '')
                if caption:
                    preview = caption[:50] + "..." if len(caption) > 50 else caption
                    print(f"  說明: {preview}")
                print()


def main():
    """
    主程式
    """
    # ============================================
    # 請在這裡填入你的資訊
    # ============================================
    ACCESS_TOKEN = "EAAfQiJIxYcIBP2ZAMKv4mjeUwcm9r2ZBocTqpm0PP7ueK6eKh3VMifujK49iyINNPhiIjA3ENG25a92t6or9NtZAXanWfF5XK88IvSeHO6kNyXdnCQKZARierHAyY9XKKTMBkyXnHHVsePyVrHpcgOF8IMwP4b1FBWhER3moj8oqRbkgCfpCbQY96DZCg"
    YOUR_BUSINESS_ACCOUNT_ID = "17841468771515418"
    TARGET_USERNAME = "sungaiwatch"  # 例如: "instagram" 或 "nike"
    # ============================================
    
    # 檢查是否已填入必要資訊
    if ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE" or YOUR_BUSINESS_ACCOUNT_ID == "YOUR_BUSINESS_ACCOUNT_ID_HERE":
        print("錯誤: 請先填入你的 ACCESS_TOKEN 和 BUSINESS_ACCOUNT_ID")
        print("\n如何取得這些資訊:")
        print("1. 前往 https://developers.facebook.com/apps/")
        print("2. 建立或選擇你的應用程式")
        print("3. 在 Graph API Explorer 中取得 Access Token")
        print("4. 使用以下 API 取得你的 Business Account ID:")
        print("   GET https://graph.facebook.com/v21.0/me/accounts")
        print("   然後用 Page ID 查詢: GET https://graph.facebook.com/v21.0/{PAGE_ID}?fields=instagram_business_account")
        return
    
    # 建立 API 實例
    api = InstagramBusinessDiscovery(ACCESS_TOKEN, YOUR_BUSINESS_ACCOUNT_ID)
    
    # 印出摘要
    api.print_summary(TARGET_USERNAME)
    
    # 取得完整資料
    full_data = api.get_account_info(TARGET_USERNAME)
    if full_data:
        api.save_to_json(full_data, f"{TARGET_USERNAME}_data.json")
    
    # 取得所有貼文（包含分頁）
    print("\n開始取得所有貼文...")
    all_posts = api.get_all_posts(TARGET_USERNAME)
    print(f"總共取得 {len(all_posts)} 篇貼文")
    
    # 儲存所有貼文
    if all_posts:
        api.save_to_json({"posts": all_posts, "total": len(all_posts)}, f"{TARGET_USERNAME}_all_posts.json")


if __name__ == "__main__":
    main()