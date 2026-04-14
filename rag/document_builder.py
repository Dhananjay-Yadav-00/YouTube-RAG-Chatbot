from langchain_core.documents import Document

def build_documents(videos, label):
    docs = []
    for v in videos:
        text = f"""
        Type: {label}
        Title: {v['title']}
        URL: {v.get('url', 'N/A')}
        Description: {v['description']}
        Views: {v['views']}
        Likes: {v['likes']}
        Comments: {v['comments']}
        Published: {v['published']}
        Tags: {', '.join(v['tags'])}
        """
        docs.append(Document(page_content=text, metadata={"type": label, "url": v.get('url', '')}))
    return docs
