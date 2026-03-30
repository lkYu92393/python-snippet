from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos
import os

# ==========================================
# 2. CONFIGURATION
# ==========================================
@dataclass
class FontConfig:
    name: int = 28
    section_title: int = 14
    default: int = 10

@dataclass
class ColorConfig:
    primary: tuple = (0, 0, 0)
    secondary: tuple = (60, 60, 60)
    light: tuple = (140, 140, 140)
    line: tuple = (180, 180, 180)

@dataclass
class LayoutConfig:
    column_count: int = 4
    cell_height: int = 15
    image_padding: int = 10  # Padding around image

@dataclass
class PDFConfig:
    DEFAULT_MARGINS = {'left': 15, 'right': 15, 'top': 15, 'bottom': 15}
    DEFAULT_SPACING = {'small': 4, 'medium': 6}

    page_width: int = 210
    page_height: int = 297
    margins: Dict[str, int] = field(default_factory=dict)
    spacing: Dict[str, int] = field(default_factory=dict)
    layout: LayoutConfig = field(default_factory=LayoutConfig)
    colors: ColorConfig = field(default_factory=ColorConfig)
    fonts: FontConfig = field(default_factory=FontConfig)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'PDFConfig':
        layout = LayoutConfig(**config_dict.get('layout', {}))
        colors = ColorConfig(**config_dict.get('colors', {}))
        fonts = FontConfig(**config_dict.get('fonts', {}))

        return cls(
            page_width=config_dict.get('page', {}).get('width', 210),
            page_height=config_dict.get('page', {}).get('height', 297),
            margins=config_dict.get('margins', cls.DEFAULT_MARGINS),
            spacing=config_dict.get('spacing', cls.DEFAULT_SPACING),
            layout=layout,
            colors=colors,
            fonts=fonts,
        )

# ==========================================
# 3. DATA MODELS
# ==========================================
@dataclass
class Entry:
    id: str
    title: str
    summary: str
    image_path: Optional[str] = None

# ==========================================
# 4. PDF GENERATOR CLASS
# ==========================================
class GridPDF(FPDF):
    def __init__(self, config: PDFConfig):
        super().__init__(
            orientation="P",
            unit="mm",
            format=(config.page_width, config.page_height)
        )
        self.config = config
        self.set_margins(
            left=config.margins['left'],
            right=config.margins['right'],
            top=config.margins['top']
        )
        self.set_auto_page_break(auto=True, margin=config.margins['bottom'])
        self._link_ids: Dict[str, int] = {}

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(*self.config.colors.light)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_toc_page(self, entries: List[Entry]):
        self.add_page()
        cfg = self.config

        self.set_font('Helvetica', 'B', cfg.fonts.section_title)
        self.set_text_color(*cfg.colors.primary)
        self.cell(0, 10, "Table of Contents", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(cfg.spacing['medium'])

        start_x = self.get_x()
        start_y = self.get_y()
        cols = cfg.layout.column_count

        usable_width = self.w - cfg.margins['left'] - cfg.margins['right']
        cell_width = usable_width / cols
        cell_height = cfg.layout.cell_height

        entries_on_page = 0

        for i, entry in enumerate(entries):
            row = entries_on_page // cols
            col = entries_on_page % cols

            x = start_x + (col * cell_width)
            y = start_y + (row * cell_height)

            if y > (cfg.page_height - 40):
                self.add_page()
                start_y = self.get_y() + 10
                entries_on_page = 0
                row = 0
                col = 0
                y = start_y
                x = start_x

            self.set_xy(x, y)
            self.set_font('Helvetica', 'B', cfg.fonts.default)
            self.set_draw_color(*cfg.colors.line)

            display_title = entry.title[:10]
            link_id = self.add_link()
            self._link_ids[entry.id] = link_id

            self.cell(cell_width, cell_height, display_title, border=1, align='C', link=link_id)

            entries_on_page += 1

    def add_detail_page(self, entry: Entry):
        self.add_page()
        cfg = self.config

        if entry.id in self._link_ids:
            link_id = self._link_ids[entry.id]
            self.set_link(link_id, page=self.page_no(), y=0)

        # Header
        self.set_font('Helvetica', 'B', cfg.fonts.name)
        self.set_text_color(*cfg.colors.primary)
        self.cell(0, 15, entry.title, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(cfg.spacing['small'])

        # Summary
        self.set_font('Helvetica', '', cfg.fonts.default)
        self.set_text_color(*cfg.colors.secondary)
        self.multi_cell(0, 10, entry.summary)
        self.ln(cfg.spacing['medium'])

        # ✅ Image with Full Width
        if entry.image_path and os.path.exists(entry.image_path):
            try:
                # Calculate available width - use full page width minus margins
                available_width = self.w - self.l_margin - self.r_margin

                # Alternative calculation if the above doesn't work:
                # available_width = cfg.page_width - cfg.margins['left'] - cfg.margins['right']

                # print(f"DEBUG: Page width={self.w}mm, Left margin={self.l_margin}mm, Right margin={self.r_margin}mm")
                # print(f"DEBUG: Available width for image={available_width}mm")

                # Save current position
                x_start = self.get_x()

                # Move to left margin
                self.set_x(cfg.margins['left'])

                # Insert image with full available width
                self.image(
                    entry.image_path,
                    x=self.get_x(),  # Explicit x position at left margin
                    y=None,
                    w=available_width  # Full width
                )

                # Move cursor down past the image
                self.set_y(self.get_y() + cfg.spacing['medium'])

                # print(f"✓ Image added: {entry.image_path} (width: {available_width}mm)")
            except Exception as e:
                self.set_text_color(255, 0, 0)
                self.cell(0, 10, f"Error loading image: {e}", align='C')
                self.set_text_color(*cfg.colors.secondary)
        else:
            # Placeholder if no image
            available_width = self.w - self.l_margin - self.r_margin
            self.set_fill_color(*cfg.colors.light)
            self.rect(
                self.l_margin,
                self.get_y(),
                available_width,
                50,
                style='F'
            )
            self.set_xy(self.l_margin, self.get_y() + 20)
            self.set_font('Helvetica', 'I', 10)
            self.set_text_color(*cfg.colors.secondary)
            self.cell(available_width, 10, "No Image Available", align='C')

    def generate_document(self, entries: List[Entry], output_path: str):
        self.add_toc_page(entries)
        for entry in entries:
            self.add_detail_page(entry)
        self.output(output_path)
        print(f"✓ Document saved to: {output_path}")
