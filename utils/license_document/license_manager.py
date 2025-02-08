from PIL import Image, ImageFont, ImageDraw
import asyncio
from typing import Tuple, Optional
import os


class CertificateGenerator:
    def __init__(self, template_path: str, font_path1: str, font_path2: str):
        self.template_path = template_path
        self.font_path1 = font_path1
        self.font_path2 = font_path2
        self.BLUE_COLOR = (0, 51, 102)  # RGB for dark blue
        self.BLACK_COLOR = (0, 0, 0)  # RGB for dark blue

        # Maximum widths for text elements (in pixels)
        self.MAX_NAME_WIDTH = 1800  # Maximum width for name
        self.MAX_DIRECTION_WIDTH = 1600  # Maximum width for direction

    async def load_image(self) -> Tuple[Image.Image, ImageDraw.ImageDraw]:
        return await asyncio.to_thread(Image.open, self.template_path)

    def get_adaptive_font_size(self, text: str, max_width: int, initial_size: int, min_size: int = 36) -> int:
        """Binary search to find the optimal font size"""
        left = min_size
        right = initial_size
        optimal_size = min_size

        while left <= right:
            mid = (left + right) // 2
            font = ImageFont.truetype(self.font_path1, mid)
            bbox = font.getbbox(text)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                optimal_size = mid
                left = mid + 1
            else:
                right = mid - 1

        return optimal_size

    def get_adaptive_font(self, text: str, is_name: bool = True) -> ImageFont.FreeTypeFont:
        """Get font with adaptive size based on text length"""
        initial_size = 130 if is_name else 83
        max_width = self.MAX_NAME_WIDTH if is_name else self.MAX_DIRECTION_WIDTH

        # Get adaptive font size
        font_size = self.get_adaptive_font_size(text, max_width, initial_size)
        return ImageFont.truetype(self.font_path1, font_size)

    async def generate_certificate(
            self,
            full_name: str,
            direction: str,
            academic_year_first: str,
            academic_year_last: str,
            date_year: str,
            date_month: str,
            order_number: str,
            output_path: str
    ) -> Optional[dict]:
        try:
            img = await self.load_image()
            draw = ImageDraw.Draw(img)

            # Get adaptive fonts
            name_font = self.get_adaptive_font(full_name, is_name=True)
            direction_font = self.get_adaptive_font(f'"{direction}"', is_name=False)
            regular_font = ImageFont.truetype(self.font_path2, 55)
            regular_font1 = ImageFont.truetype(self.font_path2, 60)

            # Calculate positions
            center_x = img.width // 2

            # Draw name with adaptive font
            name_bbox = name_font.getbbox(full_name)
            name_height = name_bbox[3] - name_bbox[1]
            draw.text(
                (center_x, 1920),
                full_name,
                font=name_font,
                fill=self.BLUE_COLOR,
                anchor="mm"
            )

            # Draw direction with adaptive font
            direction_text = f'“{direction}”'
            direction_bbox = direction_font.getbbox(direction_text)
            direction_height = direction_bbox[3] - direction_bbox[1]
            draw.text(
                (center_x, 2090),
                direction_text,
                font=direction_font,
                fill=self.BLUE_COLOR,
                anchor="mm"
            )

            # Bottom information
            bottom_start_y = 2930

            # Academic year
            draw.text(
                (center_x + 165, bottom_start_y),
                f"{academic_year_first}",
                font=regular_font,
                fill=self.BLACK_COLOR,
                anchor="ra"
            )

            draw.text(
                (center_x + 320, bottom_start_y),
                f"{academic_year_last}",
                font=regular_font,
                fill=self.BLACK_COLOR,
                anchor="ra"
            )

            # Date
            draw.text(
                (center_x + 320, bottom_start_y + 88),
                f"{date_year}",
                font=regular_font,
                fill=self.BLACK_COLOR,
                anchor="ra"
            )

            draw.text(
                (center_x + 765, bottom_start_y + 84),
                f"{date_month}",
                font=regular_font1,
                fill=self.BLACK_COLOR,
                anchor="ra"
            )

            # Order number
            draw.text(
                (center_x + 320, bottom_start_y + 176),
                f"{order_number}",
                font=regular_font,
                fill=self.BLACK_COLOR,
                anchor="ra"
            )

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save asynchronously
            await asyncio.to_thread(img.save, output_path, "JPEG", quality=95)
            return {'data': output_path, 'ok': True}

        except Exception as e:
            return {'error': str(e), 'ok': False}
