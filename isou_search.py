import requests 
import json
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

class SearchModeError(Exception):
    """Exception raised for invalid search modes."""
    pass

class SearchCategoryError(Exception):
    """Exception raised for invalid search categories."""
    pass

class NetworkError(Exception):
    """Exception raised for network-related issues."""
    pass

class ResponseParsingError(Exception):
    """Exception raised when parsing the response fails."""
    pass

class SearchMode(Enum):
    """Enumeration of available search modes."""
    SIMPLE = "simple"
    DEEP = "deep"

class SearchCategory(Enum):
    """Enumeration of available search categories."""
    GENERAL = "general"
    SCIENCE = "science"

@dataclass
class ImageResult:
    """Dataclass to represent image search results."""
    id: str = ''
    name: str = ''
    source: str = ''
    url: str = ''
    img: str = ''
    thumbnail: str = ''
    snippet: str = ''
    engine: str = ''

@dataclass
class SearchResult:
    """Dataclass to represent complete search results."""
    images: List[ImageResult] = field(default_factory=list)
    answer: str = ''
    related: str = ''

class BaseSearchProvider(ABC):
    """Abstract base class for search providers."""
    
    @abstractmethod
    def search(self, query: str) -> SearchResult:
        """Abstract method to perform a search."""
        pass

class IsouAISearchProvider(BaseSearchProvider):
    """Concrete implementation of IsouAI search provider."""
    
    DEFAULT_TIMEOUT = 10
    BASE_URL = "https://isou.chat/api/search"
    
    def __init__(self, 
                 mode: SearchMode = SearchMode.SIMPLE, 
                 category: SearchCategory = SearchCategory.SCIENCE,
                 timeout: int = DEFAULT_TIMEOUT,
                 stream: bool = True):
        """
        Initialize the IsouAI search provider.
        
        Args:
            mode: Search mode (simple or deep)
            category: Search category
            timeout: Request timeout in seconds
            stream: Whether to stream the response
        """
        self._mode = mode
        self._category = category
        self._timeout = timeout
        self._stream = stream
        self._headers = self._generate_headers()
    
    def _generate_headers(self) -> Dict[str, str]:
        """Generate headers for the HTTP request."""
        return {
            'Accept': 'text/event-stream',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://isou.chat',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
    
    def _prepare_request_payload(self, query: str) -> Dict[str, Any]:
        """Prepare the JSON payload for the request."""
        return {
            'stream': True,
            'model': 'yi-lightning',
            'provider': 'ollama',
            'mode': self._mode.value,
            'language': 'all',
            'categories': [self._category.value],
            'engine': 'SEARXNG',
            'locally': False,
            'reload': False,
        }
    
    def search(self, query: str) -> SearchResult:
        """
        Perform a search using IsouAI.
        
        Args:
            query: Search query string
        
        Returns:
            SearchResult containing images, answer, and related information
        
        Raises:
            NetworkError: If there's an issue with the network request
            ResponseParsingError: If parsing the response fails
        """
        try:
            response = requests.post(
                self.BASE_URL, 
                params={'q': query}, 
                headers=self._headers, 
                json=self._prepare_request_payload(query), 
                stream=True, 
                timeout=self._timeout
            )
            
            # Process response
            images = []
            answer = ""
            related = ""
            
            for value in response.iter_lines(decode_unicode=True, chunk_size=1000):
                if value and value.startswith("data:"):
                    try:
                        # Safely parse the JSON data
                        json_str = value[5:]
                        parsed_json = json.loads(json_str)
                        data_str = parsed_json.get('data', '{}')
                        
                        # Ensure data is a dictionary
                        data = json.loads(data_str) if isinstance(data_str, str) else data_str
                        
                        # Process images
                        if 'image' in data:
                            # Ensure image is a dictionary and has required fields
                            image_data = data['image']
                            if isinstance(image_data, dict):
                                images.append(ImageResult(**{k: str(v or '') for k, v in image_data.items()}))
                        
                        # Process text responses
                        if data.get('answer') is not None:
                            answer += str(data['answer'])
                            
                        if self._stream and 'answer' in data:
                            if data['answer'] is not None:
                                print(data['answer'], end="", flush=True)
                        
                        if data.get('related'):
                            related += str(data['related'])
                    
                    except:
                        continue
            
            return SearchResult(images=images, answer=answer, related=related)
        
        except requests.RequestException as e:
            raise NetworkError(f"Network error occurred: {e}")
        except Exception as e:
            raise ResponseParsingError(f"Unexpected error: {e}")

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