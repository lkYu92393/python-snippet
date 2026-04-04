from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos
from io import BytesIO
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
    image_source: Optional[Union[str, BytesIO]] = None  # Can be path OR BytesIO

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
        
        # ✅ Image with Auto-Fit (handles tall images)
        if entry.image_source is not None:
            try:
                # Handle different image source types
                if isinstance(entry.image_source, str):
                    if not os.path.exists(entry.image_source):
                        raise FileNotFoundError(f"Image not found: {entry.image_source}")
                    image_source = entry.image_source
                    source_type = "file"
                elif isinstance(entry.image_source, BytesIO):
                    image_source = entry.image_source
                    source_type = "BytesIO"
                elif isinstance(entry.image_source, bytes):
                    image_source = BytesIO(entry.image_source)
                    source_type = "bytes"
                else:
                    raise TypeError(f"Unsupported image source type: {type(entry.image_source)}")
                
                # Calculate available width
                available_width = self.w - self.l_margin - self.r_margin
                
                # ✅ Get image dimensions to calculate aspect ratio
                try:
                    from PIL import Image
                    if isinstance(image_source, str):
                        img = Image.open(image_source)
                    else:
                        # For BytesIO or bytes, seek to beginning
                        if hasattr(image_source, 'seek'):
                            image_source.seek(0)
                        img = Image.open(image_source)
                    
                    img_width, img_height = img.size
                    aspect_ratio = img_height / img_width
                    
                    print(f"Image dimensions: {img_width}x{img_height}, aspect ratio: {aspect_ratio:.2f}")
                    
                except ImportError:
                    print("⚠️  Pillow not installed. Cannot calculate image dimensions.")
                    aspect_ratio = 1.0  # Default assumption
                except Exception as e:
                    print(f"⚠️  Could not get image dimensions: {e}")
                    aspect_ratio = 1.0
                
                # ✅ Calculate available height on current page
                current_y = self.get_y()
                available_height = self.h - self.t_margin - self.b_margin - current_y
                
                # Calculate image height if we use full width
                calculated_height = available_width * aspect_ratio
                
                print(f"Available space: width={available_width:.1f}mm, height={available_height:.1f}mm")
                print(f"Calculated image height: {calculated_height:.1f}mm")
                
                # ✅ Check if image needs page break or scaling
                if calculated_height > available_height:
                    print(f"⚠️  Image too tall ({calculated_height:.1f}mm > {available_height:.1f}mm available)")
                    
                    # Option 1: Add page break before image
                    self.add_page()
                    self.set_x(cfg.margins['left'])
                    current_y = self.get_y()
                    available_height = self.h - self.t_margin - self.b_margin - current_y
                    print(f"Added page break. New available height: {available_height:.1f}mm")
                    
                    # Option 2: Scale down to fit (uncomment if preferred)
                    # calculated_height = available_height - 10  # Leave some margin
                    # available_width = calculated_height / aspect_ratio
                    # print(f"Scaled image to: {available_width:.1f}mm x {calculated_height:.1f}mm")
                
                # Position at left margin
                self.set_x(cfg.margins['left'])
                
                # Insert image with calculated width (height auto-scales)
                self.image(
                    image_source, 
                    x=self.get_x(),
                    y=None, 
                    w=available_width
                    # h=calculated_height  # Uncomment to force specific height
                )
                
                # Move cursor down past the image
                self.ln(cfg.spacing['medium'])
                
                print(f"✓ Image added ({source_type}): {entry.title}")
                
            except Exception as e:
                self.set_text_color(255, 0, 0)
                self.cell(0, 10, f"Error loading image: {e}", align='C')
                self.set_text_color(*cfg.colors.secondary)
                self.ln(cfg.spacing['medium'])
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
            self.ln(cfg.spacing['medium'])

    def generate_document(self, entries: List[Entry], output_path: str):
        self.add_toc_page(entries)
        for entry in entries:
            self.add_detail_page(entry)
        self.output(output_path)
        print(f"✓ Document saved to: {output_path}")
