# Instagram Business Discovery Tool

This tool uses the Instagram Business Discovery API to fetch public information from other Business/Creator accounts, including account details and posts.

## Features
- Fetch basic account info (username, bio, followers, etc.).
- Retrieve posts with configurable limits per request and total (handles pagination).
- Save data to JSON files in a dedicated `results/` folder with date-time stamped filenames.
- Print summary of account and recent posts.
- Configurable via environment variables.

## Requirements
- Python 3.12+
- A Facebook/Instagram Access Token with necessary permissions.
- Your own Instagram Business Account ID.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/eren-olympic/instagram-business-discovery.git
   cd instagram-business-discovery
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Copy `.env.example` to `.env` and fill in your details:
   ```
   cp .env.example .env
   ```
   Edit `.env`:
   ```
   ACCESS_TOKEN=your_access_token_here
   YOUR_BUSINESS_ACCOUNT_ID=your_business_account_id_here
   TARGET_USERNAME=target_username_here  # Without @
   ```

4. How to obtain credentials:
   - Go to https://developers.facebook.com/apps/.
   - Create or select your app.
   - Use Graph API Explorer to get an Access Token with `instagram_basic` and `pages_show_list` permissions.
   - To get your Business Account ID:
     - GET https://graph.facebook.com/v21.0/me/accounts (for Page ID).
     - Then GET https://graph.facebook.com/v21.0/{PAGE_ID}?fields=instagram_business_account.

## Usage

Run the CLI:
```
poetry run instagram-discovery --help
```

Commands:
- `summary`: Print account summary (with optional limits).
  ```
  poetry run instagram-discovery summary --media-limit 50 --max-posts 100
  ```
- `fetch`: Fetch and save full data to JSON (first page only, with limit).
  ```
  poetry run instagram-discovery fetch --media-limit 25 --output base_filename  # Output: results/base_filename_YYYYMMDD_HHMMSS.json
  ```
- `all-posts`: Fetch and save all posts with pagination (with optional total limit).
  ```
  poetry run instagram-discovery all-posts --media-limit 50 --max-posts 200 --output base_filename
  ```

Outputs are saved in the `results/` folder with timestamps to avoid overwriting (e.g., `results/target_username_data_20251030_120000.json`).

## Development
- Add dependencies: `poetry add <package>`.
- Run tests (if added): `poetry run pytest`.
- Lint: Add tools like black/flake8 as needed.

## License
MIT License. See LICENSE file (add if needed).