from rag_pipeline import RAGPipeline

def main():
    # Test video ID (a short educational video)
    video_id = "15_pppse4fY"  # "Me at the zoo" - First YouTube video
    
    try:
        # Initialize and run pipeline
        print("Initializing RAG Pipeline...")
        pipeline = RAGPipeline(video_id)
        pipeline.run_pipeline()
        
        print("\nQ&A System Ready!")
        print("-------------------")
        print("Type your questions and press Enter. Type 'exit' to quit.")
        
        while True:
            question = input("\nEnter your question: ").strip()
            
            if question.lower() == 'exit':
                print("Thank you for using the Q&A system!")
                break
                
            if not question:
                print("Please enter a valid question.")
                continue
                
            print(f"\nQ: {question}")
            result = pipeline.query_system(question)
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"A: {result['answer']}")
                print("\nSources:")
                for chunk in result["retrieved_chunks"]:
                    print(f"- [{chunk['start_time']} --> {chunk['end_time']}] (distance: {chunk['distance']:.4f})")
                    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
