import click
import os
from src.instagram_business_discovery import InstagramBusinessDiscovery

@click.group()
def cli():
    pass

@cli.command()
@click.option('--media-limit', type=int, default=100, help='Media items per API request (max 100)')
@click.option('--max-posts', type=int, default=None, help='Maximum total posts for summary')
def summary(media_limit, max_posts):
    """Print account summary."""
    target_username = os.getenv("TARGET_USERNAME")
    if not target_username:
        raise click.UsageError("TARGET_USERNAME must be set in .env")
    
    api = InstagramBusinessDiscovery()
    api.print_summary(target_username, media_limit=media_limit, max_posts=max_posts)

@cli.command()
@click.option('--output', default=None, help='Base filename for output (defaults to target_username_data)')
@click.option('--media-limit', type=int, default=100, help='Media items per API request (max 100)')
def fetch(output, media_limit):
    """Fetch and save full account data (first page only)."""
    target_username = os.getenv("TARGET_USERNAME")
    if not target_username:
        raise click.UsageError("TARGET_USERNAME must be set in .env")
    
    api = InstagramBusinessDiscovery()
    data = api.get_account_info(target_username, media_limit)
    if data:
        base_filename = output or f"{target_username}_data"
        api.save_to_json(data, base_filename)

@cli.command()
@click.option('--output', default=None, help='Base filename for output (defaults to target_username_all_posts)')
@click.option('--media-limit', type=int, default=100, help='Media items per API request (max 100)')
@click.option('--max-posts', type=int, default=None, help='Maximum total posts to fetch')
def all_posts(output, media_limit, max_posts):
    """Fetch and save all posts."""
    target_username = os.getenv("TARGET_USERNAME")
    if not target_username:
        raise click.UsageError("TARGET_USERNAME must be set in .env")
    
    api = InstagramBusinessDiscovery()
    print("\nFetching all posts...")
    posts = api.get_all_posts(target_username, media_limit=media_limit, max_posts=max_posts)
    print(f"Fetched {len(posts)} posts")
    
    if posts:
        base_filename = output or f"{target_username}_all_posts"
        api.save_to_json({"posts": posts, "total": len(posts)}, base_filename)

def main():
    cli()

if __name__ == "__main__":
    main()