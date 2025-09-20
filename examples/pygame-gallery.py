
import sys
import io
import os
from typing import List

import pygame

# Add parent directory to path to import material_icons
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from material_icons import MaterialIcons


class IconGallery:
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Material Icons Gallery (Rounded)")

        self.font = pygame.font.Font(None, 16)
        self.title_font = pygame.font.Font(None, 24)

        self.icons = MaterialIcons()
        self.icon_list = self._get_all_icons()

        # Grid settings
        self.icon_size = 32
        self.cell_width = 120
        self.cell_height = 60
        self.cols = (width - 40) // self.cell_width
        self.rows = (height - 80) // self.cell_height
        self.items_per_page = self.cols * self.rows

        self.current_page = 0
        self.max_pages = (len(self.icon_list) + self.items_per_page - 1) // self.items_per_page

        # Colors
        self.bg_color = (240, 240, 240)
        self.text_color = (50, 50, 50)
        self.header_color = (30, 30, 30)

        self.clock = pygame.time.Clock()

    def _get_all_icons(self) -> List[str]:
        """Get list of all available icons from the outlined directory."""
        outlined_dir = os.path.join(self.icons.icon_dir, "outlined")
        if not os.path.exists(outlined_dir):
            print(f"Icons directory not found: {outlined_dir}")
            return []

        icons = []
        for filename in os.listdir(outlined_dir):
            if filename.endswith('.svg'):
                icon_name = filename[:-4]  # Remove .svg extension
                icons.append(icon_name)

        return sorted(icons)

    def _load_icon_surface(self, name: str) -> "pygame.Surface":
        """Load an icon and convert to pygame surface."""
        try:
            png_bytes = self.icons.get(name, size=self.icon_size)
            return pygame.image.load(io.BytesIO(png_bytes))
        except Exception as e:
            print(f"Failed to load icon '{name}': {e}")
            # Return a placeholder surface
            surface = pygame.Surface((self.icon_size, self.icon_size))
            surface.fill((200, 200, 200))
            pygame.draw.rect(surface, (150, 150, 150), surface.get_rect(), 2)
            return surface

    def _draw_header(self):
        """Draw the header with page info and controls."""
        header_text = f"Material Icons Gallery - Page {self.current_page + 1} of {self.max_pages}"
        header_surface = self.title_font.render(header_text, True, self.header_color)
        self.screen.blit(header_surface, (20, 10))

        controls_text = "Arrow Keys to navigate | ESC to quit"
        controls_surface = self.font.render(controls_text, True, self.text_color)
        self.screen.blit(controls_surface, (20, 35))

        total_icons_text = f"Total icons: {len(self.icon_list)}"
        total_surface = self.font.render(total_icons_text, True, self.text_color)
        self.screen.blit(total_surface, (self.width - 150, 35))

    def _draw_icons(self):
        """Draw the current page of icons."""
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.icon_list))

        y_offset = 70

        for i, icon_name in enumerate(self.icon_list[start_idx:end_idx]):
            row = i // self.cols
            col = i % self.cols

            x = 20 + col * self.cell_width
            y = y_offset + row * self.cell_height

            # Load and draw icon
            icon_surface = self._load_icon_surface(icon_name)
            icon_x = x + (self.cell_width - self.icon_size) // 2
            icon_y = y + 5
            self.screen.blit(icon_surface, (icon_x, icon_y))

            # Draw icon name (truncated if too long)
            display_name = icon_name
            if len(display_name) > 15:
                display_name = display_name[:12] + "..."

            text_surface = self.font.render(display_name, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_x = x + (self.cell_width - text_rect.width) // 2
            text_y = y + self.icon_size + 10
            self.screen.blit(text_surface, (text_x, text_y))

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_LEFT:
                    self.current_page = max(0, self.current_page - 1)
                elif event.key == pygame.K_RIGHT:
                    self.current_page = min(self.max_pages - 1, self.current_page + 1)
        return True

    def run(self):
        """Main game loop."""
        if not self.icon_list:
            print("No icons found! Make sure icons are downloaded first.")
            return

        running = True
        while running:
            running = self.handle_events()

            # Clear screen
            self.screen.fill(self.bg_color)

            # Draw everything
            self._draw_header()
            self._draw_icons()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


def main():
    gallery = IconGallery()
    gallery.run()


if __name__ == "__main__":
    main()
