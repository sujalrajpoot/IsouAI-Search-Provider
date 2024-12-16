from isou_search import IsouAISearchProvider, SearchMode, SearchCategory, SearchModeError, SearchCategoryError, NetworkError, ResponseParsingError

def main():
    """Example usage of the IsouAI search provider."""
    try:
        # Create a search provider with custom settings
        search_provider = IsouAISearchProvider(
            mode=SearchMode.SIMPLE, 
            category=SearchCategory.SCIENCE
        )
        
        # Perform search
        result = search_provider.search("what is the current AQI in Delhi?")
        
        # Print image results
        for image in result.images:
            print(
                f"\n{'='*80}"
                f"\nID:          {image.id}"
                f"\nTitle:       {image.name}"
                f"\nSource:      {image.source}"
                f"\nURL:         {image.url}"
                f"\nImage URL:   {image.img}"
                f"\nThumbnail:   {image.thumbnail}"
                f"\nDescription: {image.snippet}"
                f"\nEngine:      {image.engine}"
                f"\n{'='*80}\n"
            )
        
        # Print text results
        print(f"Answer: {result.answer}")
        print(f"\nRelated: {result.related}")
    
    except (SearchModeError, SearchCategoryError, NetworkError, ResponseParsingError) as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
