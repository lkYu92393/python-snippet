"""Configuration settings for CV Generator"""

# ============================================
# MAIN CONFIGURATION
# ============================================
CONFIG = {
    'page': {'width': 210, 'height': 297},
    'margins': {'left': 15, 'right': 15, 'top': 15, 'bottom': 15},
    'layout': {
        'column_count': 2,
        'name_width_ratio': 0.65,
        'date_width_ratio': 0.35,
        'bullet_indent': 15,
    },
    'colors': {
        'primary': (0, 0, 0),
        'secondary': (60, 60, 60),
        'muted': (80, 80, 80),
        'light': (140, 140, 140),
        'line': (180, 180, 180),
    },
    'fonts': {
        'name': 28,
        'section_title': 12,
        'job_title': 11,
        'default': 9,
    },
    'spacing': {
        'tight': 2,
        'small': 4,
        'medium': 6,
        'large': 8,
    },
    'mode': 'nested',
}

# ============================================
# SECTION STYLES
# ============================================
SECTION_STYLES = {
    'header': {
        'name': {'font_size': 'name', 'color': 'primary', 'height': 14, 'bold': True},
        'contact': {'font_size': 'default', 'color': 'muted', 'height': 5},
        'salary': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'spacing_after': 'tight',
    },
    'work_experience': {
        'title': {'font_size': 'section_title', 'color': 'primary', 'height': 7, 'bold': True},
        'job_title': {'font_size': 'job_title', 'color': 'primary', 'height': 6, 'bold': True},
        'project_title': {'font_size': 'default', 'color': 'secondary', 'height': 5},
        'date': {'font_size': 'default', 'color': 'light', 'height': 6},
        'description': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'bullet': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'spacing_after_job': 'small',
        'spacing_after_project': 'tight',
        'spacing_before_bullets': 'tight',
    },
    'projects': {
        'title': {'font_size': 'section_title', 'color': 'primary', 'height': 7, 'bold': True},
        'project_title': {'font_size': 'job_title', 'color': 'primary', 'height': 6, 'bold': True},
        'date': {'font_size': 'default', 'color': 'light', 'height': 6},
        'description': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'bullet': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'spacing_after_project': 'small',
        'spacing_before_bullets': 'tight',
    },
    'education': {
        'title': {'font_size': 'section_title', 'color': 'primary', 'height': 7, 'bold': True},
        'institution': {'font_size': 'job_title', 'color': 'primary', 'height': 6, 'bold': True},
        'degree': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'date': {'font_size': 'default', 'color': 'light', 'height': 6},
        'spacing_after': 'small',
    },
    'languages': {
        'title': {'font_size': 'section_title', 'color': 'primary', 'height': 7, 'bold': True},
        'language': {'font_size': 'default', 'color': 'primary', 'height': 5, 'bold': True},
        'proficiency': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'spacing_after': 'medium',
        'row_spacing': 12,
        'column_count': 2,  # ← ADD THIS
    },
    
    'skills': {
        'title': {'font_size': 'section_title', 'color': 'primary', 'height': 7, 'bold': True},
        'category': {'font_size': 'default', 'color': 'primary', 'height': 5, 'bold': True},
        'skills': {'font_size': 'default', 'color': 'primary', 'height': 5},
        'spacing_after': 'medium',
        'row_spacing': 12,
        'column_count': 3,  # ← ADD THIS
    },
}

# ============================================
# LINE STYLES
# ============================================
LINE_STYLE = {'width': 0.25, 'offset_y': 1}

# ============================================
# SECTION ORDER & TITLES
# ============================================
SECTION_ORDER = {
    'nested': ['work_experience', 'education', 'skills', 'languages'],
    'separate': ['work_experience', 'projects', 'education', 'skills', 'languages'],
}

SECTION_TITLES = {
    'work_experience': 'WORK EXPERIENCE',
    'projects': 'PROJECTS',
    'education': 'EDUCATION',
    'languages': 'LANGUAGES',
    'skills': 'SKILLS',
}

# ============================================
# FONT FILES
# ============================================
FONT_FILES = {
    'regular': 'DejaVuSans.ttf',
    'bold': 'DejaVuSans-Bold.ttf',
}