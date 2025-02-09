import os
import requests
from datetime import datetime, timedelta
from arxiv import Client, Search, SortCriterion, SortOrder
from PyPDF2 import PdfReader
import openai

from config import CONFIG

def fetch_papers():
    search_query = "(all:\"machine learning systems\" OR all:MLSys OR all:\"distributed machine learning\" OR all:\"model serving\") AND (cat:cs.LG OR cat:cs.DC)"
    client = Client()  # 创建客户端实例
    search = Search(
        query=search_query,
        sort_by=SortCriterion.SubmittedDate,
        sort_order=SortOrder.Descending,
        max_results=100
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

def gpt_summarize(text):
    prompt = f"""请用中文总结以下学术论文内容：

1. 用三句话概括论文摘要
2. 列出三个主要创新点
3. 保持简洁专业

论文内容：{text}"""

    client = openai.OpenAI(
        base_url=CONFIG["base_url"],
        api_key=CONFIG["api_key"]
    )

    print(f"Requesting GPT to summarize: {text[:100]}...")
    print(f"Request length: {len(text)}")
    response = client.chat.completions.create(
        model=CONFIG["model"],
        messages=[{
            "role": "user",
            "content": prompt
        }],
    )
    print(f"Response: {response.choices[0].message.content[:100]}...")
    print(f"Response length: {len(response.choices[0].message.content)}")
    return response.choices[0].message.content

def daily_job():
    report = []
    papers = fetch_papers()
    
    for paper in papers:
        try:
            # 下载并处理PDF
            pdf_path = f"temp/{paper['title']}.pdf"
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