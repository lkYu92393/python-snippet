"""Style resolver for CV Generator"""

from config import CONFIG


class StyleResolver:
    """Resolves style references from CONFIG"""
    
    def __init__(self, config, section_styles):
        self.config = config
        self.section_styles = section_styles
    
    def get_font_size(self, size_key):
        """Resolve font size from config"""
        if isinstance(size_key, int):
            return size_key
        return self.config['fonts'].get(size_key, self.config['fonts']['default'])
    
    def get_color(self, color_key):
        """Resolve color from config"""
        if isinstance(color_key, tuple):
            return color_key
        return self.config['colors'].get(color_key, self.config['colors']['primary'])
    
    def get_spacing(self, spacing_key):
        """Resolve spacing from config"""
        if isinstance(spacing_key, int):
            return spacing_key
        return self.config['spacing'].get(spacing_key, self.config['spacing']['medium'])
    
    def get_section_style(self, section_name):
        """Get complete style for a section"""
        return self.section_styles.get(section_name, {})
    
    def get_computed_layout(self):
        """Calculate derived layout values"""
        available_width = (
            self.config['page']['width'] 
            - self.config['margins']['left'] 
            - self.config['margins']['right']
        )
        
        return {
            'available_width': available_width,
            'name_cell_width': available_width * self.config['layout']['name_width_ratio'],
            'date_cell_width': available_width * self.config['layout']['date_width_ratio'],
            'column_width': available_width / self.config['layout']['column_count'],
            'column_cell_width': (available_width / self.config['layout']['column_count']) - 5,
            'line_length': available_width,
            'bullet_indent': self.config['layout']['bullet_indent'],
        }

    def get_column_layout(self, section_name: str):
        """Get column layout for a specific section"""
        section_style = self.section_styles.get(section_name, {})
        column_count = section_style.get('column_count', self.config['layout']['column_count'])
        
        available_width = (
            self.config['page']['width'] 
            - self.config['margins']['left'] 
            - self.config['margins']['right']
        )
        
        return {
            'column_count': column_count,
            'column_width': available_width / column_count,
            'column_cell_width': (available_width / column_count) - 5,
            'row_spacing': section_style.get('row_spacing', 12),
        }