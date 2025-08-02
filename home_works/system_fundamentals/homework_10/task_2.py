"""Module for text analysis and visualization of top words from web content."""

import re
import string
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns
from concurrent.futures import ThreadPoolExecutor

import requests


class TopWordsGetter:
    """Class for extracting and analyzing top words from web content."""
    
    def __init__(self, url: str) -> None:
        """
        Initialize TopWordsGetter with URL.
        
        Args:
            url: URL to fetch text content from
        """
        self.url = url

    def get_text(self) -> str:
        """
        Fetch text content from the URL.
        
        Returns:
            Raw text content from the URL
        """
        with requests.get(self.url, timeout=30) as response:
            return response.text

    def remove_punctuation(self, text: str) -> str:
        """
        Remove punctuation from text.
        
        Args:
            text: Input text
            
        Returns:
            Text with punctuation removed
        """
        return text.translate(str.maketrans("", "", string.punctuation))

    def remove_tags(self, text: str) -> str:
        """
        Remove HTML tags and cleanup text.
        
        Args:
            text: HTML text content
            
        Returns:
            Clean text without HTML tags
        """
        # Remove CSS styles
        text = re.sub(
            r"<style[^>]*>.*?</style>", "", text, 
            flags=re.DOTALL | re.IGNORECASE
        )

        # Remove JavaScript
        text = re.sub(
            r"<script[^>]*>.*?</script>", "", text,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Remove HTML comments
        text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

        # Remove all HTML tags (improved regex)
        text = re.sub(r"<[^<>]*>", "", text)
        
        # Additional step: remove remaining tag parts
        text = re.sub(r"<[^>]*", "", text)  # Unclosed tags
        text = re.sub(r"[^<]*>", "", text)  # Closing tag parts

        # Remove CSS rules that might remain
        text = re.sub(r"\{[^}]*\}", "", text, flags=re.DOTALL)

        # Remove CSS selectors (words with colons)
        text = re.sub(r"\b\w+\s*:\s*[^;]+;?", "", text)

        # Remove single letters from tags (P, A, DIV etc.)
        text = re.sub(r"\b[A-Z]{1,3}\b", "", text)
        
        # Remove HTML entities
        text = re.sub(r"&[a-zA-Z0-9#]+;", "", text)
        
        # Remove numeric references
        text = re.sub(r"\b\d+\b", "", text)

        # Clean extra whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def map_function(self, word: str) -> Tuple[str, int]:
        """
        Map function for MapReduce - converts word to uppercase with count 1.
        
        Args:
            word: Input word
            
        Returns:
            Tuple of (uppercase_word, 1)
        """
        return word.upper(), 1

    def shuffle_function(
        self, mapped_values: List[Tuple[str, int]]
    ) -> List[Tuple[str, List[int]]]:
        """
        Shuffle function for MapReduce - groups values by key.
        
        Args:
            mapped_values: List of (key, value) tuples
            
        Returns:
            List of (key, list_of_values) tuples
        """
        shuffled: defaultdict[str, List[int]] = defaultdict(list)
        for key, value in mapped_values:
            shuffled[key].append(value)
        return list(shuffled.items())

    def reduce_function(self, key_values: Tuple[str, List[int]]) -> Tuple[str, int]:
        """
        Reduce function for MapReduce - sums values for each key.
        
        Args:
            key_values: Tuple of (key, list_of_values)
            
        Returns:
            Tuple of (key, sum_of_values)
        """
        key, values = key_values
        return key, sum(values)

    def map_reduce(self, search_words: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Execute MapReduce algorithm to count word frequencies.
        
        Args:
            search_words: Optional list of specific words to search for
            
        Returns:
            Dictionary of word frequencies sorted by frequency (descending)
        """
        text = self.get_text()
        # Remove punctuation and tags
        text = self.remove_punctuation(text)
        text = self.remove_tags(text)
        words = text.split()

        # Filter words if search list is provided
        if search_words:
            words = [word for word in words if word in search_words]

        # Parallel mapping
        with ThreadPoolExecutor() as executor:
            mapped_values = list(executor.map(self.map_function, words))

        # Shuffle step
        shuffled_values = self.shuffle_function(mapped_values)

        # Parallel reduction
        with ThreadPoolExecutor() as executor:
            reduced_values = list(executor.map(self.reduce_function, shuffled_values))

        result_dict = dict(reduced_values)
        return {
            k: result_dict[k] 
            for k in sorted(result_dict, key=result_dict.get, reverse=True)
        }

    def get_top_words(self, search_words: Optional[List[str]] = None) -> Dict[str, int]:
        """
        Get top 10 most frequent words.
        
        Args:
            search_words: Optional list of specific words to search for
            
        Returns:
            Dictionary of top 10 word frequencies
        """
        all_words = self.map_reduce(search_words)
        return dict(list(all_words.items())[:10])


def top_words_barchart(top_words: Dict[str, int], title: str = "Top 10 words") -> None:
    """
    Create horizontal bar chart for top words.
    
    Args:
        top_words: Dictionary of word frequencies
        title: Chart title
    """
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 8))

    # Create horizontal bar plot
    words = list(top_words.keys())
    frequencies = list(top_words.values())
    
    # Create horizontal bars
    bars = plt.barh(words, frequencies)
    
    # Add value labels on the bars
    max_freq = max(frequencies) if frequencies else 1
    for bar, freq in zip(bars, frequencies):
        plt.text(
            bar.get_width() + max_freq * 0.01, 
            bar.get_y() + bar.get_height() / 2, 
            str(freq), 
            ha='left', va='center', fontsize=10
        )

    # Customize the plot
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Words", fontsize=12)
    
    # Reverse the order to show highest values at the top
    plt.gca().invert_yaxis()
    
    # Adjust margins to ensure all text is visible
    plt.subplots_adjust(left=0.2, right=0.95, top=0.95, bottom=0.1)
    
    plt.show()


def main() -> None:
    """Main function to demonstrate word frequency analysis."""
    url = "https://www.gutenberg.org/files/1580/1580-h/1580-h.htm#link2H_4_0005"
    top_words_getter = TopWordsGetter(url)
    top_words = top_words_getter.get_top_words()
    top_words_barchart(top_words)


if __name__ == "__main__":
    main()