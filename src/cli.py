import click
import os
from src.instagram_business_discovery import InstagramBusinessDiscovery

@click.group()
def cli():
    pass

@cli.command()
def summary():
    """Print account summary."""
    target_username = os.getenv("TARGET_USERNAME")
    if not target_username:
        raise click.UsageError("TARGET_USERNAME must be set in .env")
    
    api = InstagramBusinessDiscovery()
    api.print_summary(target_username)

@cli.command()
@click.option('--output', default=None, help='Output JSON filename')
def fetch(output):
    """Fetch and save full account data."""
    target_username = os.getenv("TARGET_USERNAME")
    if not target_username:
        raise click.UsageError("TARGET_USERNAME must be set in .env")
    
    api = InstagramBusinessDiscovery()
    data = api.get_account_info(target_username)
    if data:
        filename = output or f"{target_username}_data.json"
        api.save_to_json(data, filename)

@cli.command()
@click.option('--output', default=None, help='Output JSON filename')
def all_posts(output):
    """Fetch and save all posts."""
    target_username = os.getenv("TARGET_USERNAME")
    if not target_username:
        raise click.UsageError("TARGET_USERNAME must be set in .env")
    
    api = InstagramBusinessDiscovery()
    print("\nFetching all posts...")
    posts = api.get_all_posts(target_username)
    print(f"Fetched {len(posts)} posts")
    
    if posts:
        filename = output or f"{target_username}_all_posts.json"
        api.save_to_json({"posts": posts, "total": len(posts)}, filename)

def main():
    cli()

if __name__ == "__main__":
    main()