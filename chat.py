import logging
import os

from core.load_settings import load_settings
from retrieval.retriever import retrieve
from llm.generator import generate_answer

settings = load_settings()
logger = logging.getLogger("chat")

MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "512"))

def chat(question: str) -> str:
    if not question:
        logger.warning("Received empty question")
        return "Câu hỏi không được để trống"
    
    if len(question) > MAX_QUERY_LENGTH:
        logger.warning("Question length exceeds maxium limit")
        return f"Câu hỏi quá dài (hơn {MAX_QUERY_LENGTH} ký tự). Vui lòng rút gọn câu hỏi."
    
    logger.info(f"Starting retrieval for th question : {question}")

    try:
        documents = retrieve(question)

        if not documents:
            logger.info("No relevant document found")
            return "Tôi không tìm thấy thông tin phù hợp trong tài liệu"

        context = "\n\n".join(
            f"[Document {i+1}]\n{doc.text}\n(Nguồn: {doc.metadata})"
            for i, doc in enumerate(documents)
        )
        answer = generate_answer(context, question)

        logger.info("Answer generation completed successfully.")
        return answer

    except Exception as e:
        logger.error(f"Error during chat process: {e}")
        return "Đã xảy ra lỗi trong quá trình xử lý câu hỏi. Vui lòng thử lại."

def main():
    while True:
        question = input("Bạn: ")
        if question.lower() in {"exit", "quit"}:
            print("Kết thúc trò chuyện")
            break
        answer = chat(question)
        print("Bot: ", answer)
if __name__ == "__main__":
    main()