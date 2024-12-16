# IsouAI Search Provider

## Overview

This Python library provides a flexible and extensible search solution using the IsouAI search API. It supports customizable search modes, categories, and robust error handling for retrieving web search results and images.

## Features

- 🔍 Flexible Search Modes
  - Simple search
  - Deep search

- 📑 Multiple Search Categories
  - General search
  - Science-focused search

- 🖼️ Image Search Capabilities
  - Retrieve image results with metadata
  - Extract image details like source, URL, and description

- 🛡️ Comprehensive Error Handling
  - Specific exceptions for different error scenarios
  - Network error handling
  - Response parsing error management

## Installation

```bash
pip install requests
```

Note: This library depends on the `requests` library for making HTTP requests.

## Usage Example

```python
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

```

## Configuration Options

### Search Modes
- `SearchMode.SIMPLE`: Standard search mode
- `SearchMode.DEEP`: Comprehensive search mode

### Search Categories
- `SearchCategory.GENERAL`: Broad, general-purpose search
- `SearchCategory.SCIENCE`: Specialized scientific search

## Advanced Configuration

```python
search_provider = IsouAISearchProvider(
    mode=SearchMode.DEEP,            # Search mode
    category=SearchCategory.SCIENCE,  # Search category
    timeout=15,                       # Custom timeout (default: 10 seconds)
    stream=True                       # Enable streaming results
)
```

## Error Handling

The library provides specific exceptions for different error scenarios:

- `SearchModeError`: Invalid search mode
- `SearchCategoryError`: Invalid search category
- `NetworkError`: Network-related issues
- `ResponseParsingError`: Issues parsing API response

```python
try:
    result = search_provider.search("your query")
except NetworkError as e:
    print(f"Network problem: {e}")
except ResponseParsingError as e:
    print(f"Response parsing failed: {e}")
```

## Return Object Structure

The `SearchResult` object contains:
- `images`: List of `ImageResult` objects
- `answer`: Textual search result
- `related`: Related information

Each `ImageResult` includes:
- `id`
- `name`
- `source`
- `url`
- `img`
- `thumbnail`
- `snippet`
- `engine`

## Requirements

- Python 3.7+
- `requests` library
- `dataclasses`

## Disclaimer ⚠️

**IMPORTANT: EDUCATIONAL PURPOSE ONLY**

This library interfaces with the IsouAI search API for educational purposes only. It is not intended to harm or exploit the https://isou.chat/ website in any way.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.
