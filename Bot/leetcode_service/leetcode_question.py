from leetcode_service.leetcode_constants import Constants

class LeetcodeQuestion:

    def __init__(self, title, slug, difficulty):
        self.title = title
        self.slug = slug
        self.difficulty = difficulty
        self.url = self._build_url(slug)
    
    def _build_url(self, slug):
        return f"{Constants.PROBLEMS_PATH}/{slug}/"
