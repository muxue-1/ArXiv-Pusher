import os
import requests
from datetime import datetime, timedelta
from arxiv import Client, Search, SortCriterion, SortOrder
from PyPDF2 import PdfReader
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from config import CONFIG

def fetch_papers():
    search_query = "(cat:cs.LG OR cat:cs.DC)"
    client = Client()
    search = Search(
        query=search_query,
        sort_by=SortCriterion.SubmittedDate,
        sort_order=SortOrder.Descending,
        max_results=5
    )
    
    papers = []
    cutoff_date = datetime.now() - timedelta(days=CONFIG["days_lookback"])
    
    for result in client.results(search):
        if result.published.replace(tzinfo=None) > cutoff_date:
            papers.append({
                "title": result.title,
                "url": result.entry_id,
                "pdf_url": result.pdf_url,
                "abstract": result.summary,
                "authors": [a.name for a in result.authors],
                "published": result.published
            })
    print(f"Found {len(papers)} papers.")
    return papers

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def ask(prompt: str, model: str = "deepseek-v3-250324") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    # print(f"API Key set: {'Yes' if api_key else 'No'}")
    # print(f"Base URL set: {'Yes' if base_url else 'No'}")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    if not base_url:
        raise ValueError("OPENAI_BASE_URL environment variable is not set")

    response = requests.post(
        url = base_url,
        json = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "stream": False,
        },
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def gpt_summarize(text):
    prompt = f"""请用中文总结以下学术论文内容：

1. 用三句话概括论文摘要
2. 列出三个主要创新点
3. 保持简洁专业

论文内容：{text}"""

    print(f"Requesting GPT to summarize: {text[:100]}...")
    print(f"Request length: {len(text)}")
    summary = ask(prompt, model=CONFIG["model"])
    print(f"Response: {summary[:100]}...")
    print(f"Response length: {len(summary)}")
    return summary

def daily_job():
    report = []
    papers = fetch_papers()
    
    for paper in papers:
        try:
            # 下载并处理PDF
            pdf_path = f"temp/{paper['pdf_url'][paper['pdf_url'].rfind('/')+1:]}.pdf"
            download_pdf(paper['pdf_url'], pdf_path)
            text = extract_text_from_pdf(pdf_path)

            # GPT总结
            summary = gpt_summarize(text)
            # os.remove(pdf_path)  # 清理临时文件

            # 构建报告
            report.append(f"""
论文标题: {paper['title']}
作者: {', '.join(paper['authors'])}
发表日期: {paper['published'].strftime('%Y-%m-%d %H:%M:%S')}
链接: {paper['url']}

{summary}
{'='*60}
""")
        except Exception as e:
            print(f"处理论文失败: {paper['title']}，错误: {str(e)}")
    
    if report:
        # send_email('\n'.join(report))
        with open('report.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        print("Reports sent.")

if __name__ == "__main__":
    daily_job()