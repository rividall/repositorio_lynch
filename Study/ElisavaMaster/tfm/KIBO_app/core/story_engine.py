# core/story_engine.py - Story loading and navigation logic

import json
from typing import Optional, Dict, Any, List
import os

def list_available_stories(stories_dir: str = "stories") -> list:
    """
    List all available story JSON files in the given directory, returning their filenames and titles.
    Uses absolute paths for robustness.

    Usage:
        - To list all stories in the top-level 'stories' directory:
            list_available_stories("stories")
        - To list all stories in a subdirectory (e.g., 'stories/math'):
            list_available_stories("stories/math")

    :param stories_dir: Directory containing story JSON files.
    :return: List of dicts with 'filename' and 'title' keys.
    """
    stories = []
    # Make stories_dir absolute
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_stories_dir = os.path.normpath(os.path.join(current_dir, "..", stories_dir))
    if not os.path.isdir(abs_stories_dir):
        return stories
    for fname in os.listdir(abs_stories_dir):
        if fname.endswith(".json"):
            path = os.path.join(abs_stories_dir, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                title = data.get("title", fname)
                stories.append({"filename": fname, "title": title})
            except Exception:
                # Skip files that can't be loaded
                continue
    return stories

class StoryEngine:
    """
    Backend-only class for loading and navigating interactive stories.
    Each story is a JSON file with a title and a list of pages.
    Each page contains text, image, and optionally a mini_game dict.
    """

    def __init__(self, story_path: str):
        """
        Initialize the StoryEngine by loading a story from a JSON file.

        :param story_path: Path to the story JSON file.
        """
        # Make story_path absolute
        current_dir = os.path.dirname(os.path.abspath(__file__))
        abs_story_path = story_path
        if not os.path.isabs(story_path):
            abs_story_path = os.path.normpath(os.path.join(current_dir, "..", story_path))
        with open(abs_story_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.title: str = data.get("title", "")
        self.pages: List[Dict[str, Any]] = data.get("pages", [])
        self.current_index: int = 0

    def get_page(self, index: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Get the page at the given index, or the current page if index is None.

        :param index: Page index (optional).
        :return: Page dict or None if out of bounds.
        """
        idx = self.current_index if index is None else index
        if 0 <= idx < len(self.pages):
            return self.pages[idx]
        return None

    def next_page(self) -> Optional[Dict[str, Any]]:
        """
        Move to the next page and return it.

        :return: The next page dict, or None if at the end.
        """
        if self.has_next():
            self.current_index += 1
            return self.get_page()
        return None

    def previous_page(self) -> Optional[Dict[str, Any]]:
        """
        Move to the previous page and return it.

        :return: The previous page dict, or None if at the beginning.
        """
        if self.has_previous():
            self.current_index -= 1
            return self.get_page()
        return None

    def has_next(self) -> bool:
        """
        Check if there is a next page.

        :return: True if next page exists, False otherwise.
        """
        return self.current_index < len(self.pages) - 1

    def has_previous(self) -> bool:
        """
        Check if there is a previous page.

        :return: True if previous page exists, False otherwise.
        """
        return self.current_index > 0

    def get_mini_game(self) -> Optional[Dict[str, Any]]:
        """
        Get the mini_game dict for the current page, if present.

        :return: mini_game dict or None.
        """
        page = self.get_page()
        if page and "mini_game" in page:
            return page["mini_game"]
        return None

    def reset(self):
        """
        Reset the story to the first page.
        """
        self.current_index = 0
