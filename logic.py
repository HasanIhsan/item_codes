# logic.py
import os
import random
import re
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "assets"


class QuizLogic:
    """
    Stores items and codes, chooses quiz options, returns associated image.
    """

    def __init__(self):
        # Example dataset — add more items here.
        self.items = {
            "banana": 4011,
            "onion red": 4082,
            "parsley curly": 4900,
            "celery stalks": 4070,
            "apple granny smith": 4017,
            "tomato vine": 4664,
            "cucumber field": 4062,
            "lemon": 4053,
            "asparagus": 4080,
            "avocado": 4046,
            "brocoli binch": 4060,
            "brocoli crown":3082,
            "cantelope": 4050,
            "Cauliflower":4572,
            "Celantro": 4889,
            "celery root": 4585,
            "corn": 4590,
            "cucumber english": 4593,
            "Garlic":4610,
            "ginger root":4612,
            "lemons": 4053,
            "limes": 4048,
            "Onion sweet":4159,
            "onion yellow":4658,
            "onion green": 4068,
            "parsley Itealina": 4901,
            "pepper green": 4065,
            "pepper orange":3121,
            "pepper red": 4688,
            "pepper yellow": 4689,
            "pinapple": 4430,
            "pomegranete":3127,
            "potato white": 4083,
            "potato red": 4073,
            "potato yellow": 4727,
            "tomato roma": 4087,
            "tomato vine ripe": 4664,
            "zucchini green": 4067,
            "zucchini yellow": 4086,
            "Dounuts": 2736,
            "pc case water": 7541,
            "Bags": 18951
            
        }

    def _normalize_key_to_filename(self, key: str) -> str:
        """Normalize a key to a safe filename (lowercase, spaces -> underscores)."""
        key = key.lower()
        key = re.sub(r"[^\w\s-]", "", key)  # remove punctuation
        key = re.sub(r"\s+", "_", key.strip())
        return key

    def get_image(self, key: str, size: Tuple[int, int] = (300, 220)) -> Image.Image:
        """
        Returns a PIL.Image for the given key.
        Looks for common extensions in the assets directory. If not found, returns a placeholder image.
        """
        filename_base = self._normalize_key_to_filename(key)
        possible_exts = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]
        for ext in possible_exts:
            path = os.path.join(ASSETS_DIR, filename_base + ext)
            if os.path.isfile(path):
                try:
                    img = Image.open(path).convert("RGBA")
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                    return img
                except Exception:
                    break  # fall through to placeholder

        # Placeholder image
        img = Image.new("RGBA", size, (230, 230, 230, 255))
        draw = ImageDraw.Draw(img)
        # Try to get a basic font; fallback to default.
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except Exception:
            font = ImageFont.load_default()
        text = key.title()
       
        w = draw.textlength(text, font=font)
        h = 12
        draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=(40, 40, 40), font=font)
        return img

    def randomize_quiz(self) -> Tuple[str, str, List[Tuple[str, str]], Image.Image]:
        """
        Chooses a correct key/value pair and three other unique values.
        Returns:
          - correct_key (str),
          - correct_value (str),
          - options (List of tuples (value_str, key)) shuffled,
          - image (PIL.Image for the correct_key)
        """
        if len(self.items) < 4:
            raise ValueError("Need at least 4 items in the dataset to make a quiz.")

        keys = list(self.items.keys())
        correct_key = random.choice(keys)
        correct_value = str(self.items[correct_key])

        # Prepare other (value, key) pairs excluding the correct one
        other_pairs = [(str(v), k) for k, v in self.items.items() if k != correct_key]
        wrong_choices = random.sample(other_pairs, k=3)

        options = wrong_choices + [(correct_value, correct_key)]
        random.shuffle(options)

        img = self.get_image(correct_key)
        return correct_key, correct_value, options, img

    def is_correct(self, correct_value: str, selected_value: str) -> bool:
        """Return True if the selected value matches the correct one."""
        return str(correct_value) == str(selected_value)
