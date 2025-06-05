import os
import json
from datetime import datetime
import re
def extract_title_from_markdown(content):
    # Try to get title from H1 header
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1)
    return None

def get_blog_posts():
    blog_dir = "blog"
    posts = []
    
    # Ensure blog directory exists
    if not os.path.exists(blog_dir):
        print(f"Warning: {blog_dir} directory not found")
        return posts
    
    # Get all markdown files
    for filename in os.listdir(blog_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(blog_dir, filename)
            
            # Get file modification time as fallback date
            mod_time = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from content or use filename
            title = extract_title_from_markdown(content)
            if not title:
                title = filename.replace('.md', '').replace('-', ' ').title()
            
            posts.append({
                'filename': filename,
                'title': title,
                'date': date
            })
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def generate_metadata():
    posts = get_blog_posts()
    metadata = {'posts': posts}
    
    # Write to blog-posts.json
    with open('blog-posts.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"Generated metadata for {len(posts)} blog posts")

if __name__ == "__main__":
    generate_metadata()
