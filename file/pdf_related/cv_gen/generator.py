"""CV Generator class with all render methods"""

import os
from fpdf import FPDF
from config import CONFIG, SECTION_STYLES, LINE_STYLE, SECTION_TITLES, SECTION_ORDER, FONT_FILES
from styles import StyleResolver


class CVGenerator(FPDF):
    """PDF Generator for CV with all render methods"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_fonts()
        self.resolver = StyleResolver(CONFIG, SECTION_STYLES)
        self.layout = self.resolver.get_computed_layout()
    
    def _load_fonts(self):
        """Load required fonts"""
        for style, filename in FONT_FILES.items():
            if os.path.exists(filename):
                self.add_font('DejaVu', 'B' if style == 'bold' else '', filename, uni=True)
    
    def header(self):
        """No header - we create custom header"""
        pass
    
    def footer(self):
        """No footer"""
        pass
    
    # ============================================
    # RENDER METHODS
    # ============================================
    
    def render_header(self, contact):
        """Render header section (name, contact, salary)"""
        style = self.resolver.get_section_style('header')
        
        # Name
        self.set_font('DejaVu', 'B', self.resolver.get_font_size(style['name']['font_size']))
        self.set_text_color(*self.resolver.get_color(style['name']['color']))
        self.cell(0, style['name']['height'], contact['name'], ln=True, align='C')
        
        # Contact
        self.set_font('DejaVu', '', self.resolver.get_font_size(style['contact']['font_size']))
        self.set_text_color(*self.resolver.get_color(style['contact']['color']))
        contact_line = " | ".join(contact.get("contacts", []))
        # contact_line = f"{contact['email']}  |  {contact['phone']}  |  {contact['github']}"
        self.cell(0, style['contact']['height'], contact_line, ln=True, align='C')
        
        # Salary
        self.set_font('DejaVu', '', self.resolver.get_font_size(style['salary']['font_size']))
        self.set_text_color(*self.resolver.get_color(style['salary']['color']))
        summary_line = " | ".join(contact.get("summaries", []))
        self.cell(0, style['salary']['height'], summary_line, ln=True, align='C')
        
        self.ln(self.resolver.get_spacing(style['spacing_after']))
    
    def render_section_title(self, title):
        """Render section title with underline"""
        style = self.resolver.get_section_style('work_experience')['title']
        
        self.ln(self.resolver.get_spacing('large'))
        self.set_font('DejaVu', 'B', self.resolver.get_font_size(style['font_size']))
        self.set_text_color(*self.resolver.get_color(style['color']))
        self.cell(0, style['height'], title, ln=True)
        
        # Draw line
        x = self.get_x()
        y = self.get_y()
        self.set_line_width(LINE_STYLE['width'])
        self.set_draw_color(*self.resolver.get_color('line'))
        self.line(x, y + LINE_STYLE['offset_y'], x + self.layout['line_length'], y + LINE_STYLE['offset_y'])
        self.ln(self.resolver.get_spacing('medium'))
    
    def render_work_experience(self, jobs, include_projects=True):
        """Render work experience (optionally with projects)"""
        style = self.resolver.get_section_style('work_experience')
        
        for job in jobs:
            if not job.get('position', '').strip():
                continue
            
            # Job title and company
            job_title_text = f"{job['position']} - {job['company']}"
            self.set_font('DejaVu', 'B', self.resolver.get_font_size(style['job_title']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['job_title']['color']))
            self.cell(self.layout['name_cell_width'], style['job_title']['height'], job_title_text, ln=False)
            
            # Date
            self.set_font('DejaVu', '', self.resolver.get_font_size(style['date']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['date']['color']))
            self.cell(self.layout['date_cell_width'], style['date']['height'], job['date'], ln=True, align='R')
            
            # Projects (only in nested mode)
            if include_projects and job.get('projects'):
                self._render_projects_nested(job['projects'], style)
            
            self.ln(self.resolver.get_spacing(style['spacing_after_job']))
    
    def _render_projects_nested(self, projects, parent_style):
        """Render projects nested within a job"""
        for project in projects:
            if not project.get('name', '').strip():
                continue
            
            self.ln(self.resolver.get_spacing(parent_style['spacing_after_project']))
            
            # Project title
            self.set_font('DejaVu', '', self.resolver.get_font_size(parent_style['project_title']['font_size']))
            self.set_text_color(*self.resolver.get_color(parent_style['project_title']['color']))
            self.cell(0, parent_style['project_title']['height'], project['name'], ln=True)
            
            # Tech stack + description
            self.set_font('DejaVu', '', self.resolver.get_font_size(parent_style['description']['font_size']))
            self.set_text_color(*self.resolver.get_color(parent_style['description']['color']))
            
            if project.get('tech_stack'):
                full_text = f"Tech stack: {project['tech_stack']} {project['description']}"
            else:
                full_text = project['description']
            self.multi_cell(0, parent_style['description']['height'], full_text)
            
            # Bullets
            if project.get('bullets'):
                self.ln(self.resolver.get_spacing(parent_style['spacing_before_bullets']))
                for bullet in project['bullets']:
                    if bullet.strip():
                        self.set_font('DejaVu', '', self.resolver.get_font_size(parent_style['bullet']['font_size']))
                        self.set_text_color(*self.resolver.get_color(parent_style['bullet']['color']))
                        self.set_x(self.layout['bullet_indent'])
                        self.multi_cell(0, parent_style['bullet']['height'], f"•  {bullet}")
    
    def render_projects(self, projects):
        """Render projects as separate section"""
        style = self.resolver.get_section_style('projects')
        
        for project in projects:
            if not project.get('name', '').strip():
                continue
            
            # Project title
            self.set_font('DejaVu', 'B', self.resolver.get_font_size(style['project_title']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['project_title']['color']))
            self.cell(self.layout['name_cell_width'], style['project_title']['height'], project['name'], ln=False)
            
            # Date
            self.set_font('DejaVu', '', self.resolver.get_font_size(style['date']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['date']['color']))
            self.cell(self.layout['date_cell_width'], style['date']['height'], project.get('date', ''), ln=True, align='R')
            
            # Tech stack + description
            self.set_font('DejaVu', '', self.resolver.get_font_size(style['description']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['description']['color']))
            
            if project.get('tech_stack'):
                full_text = f"Tech stack: {project['tech_stack']} {project['description']}"
            else:
                full_text = project['description']
            self.multi_cell(0, style['description']['height'], full_text)
            
            # Bullets
            if project.get('bullets'):
                self.ln(self.resolver.get_spacing(style['spacing_before_bullets']))
                for bullet in project['bullets']:
                    if bullet.strip():
                        self.set_font('DejaVu', '', self.resolver.get_font_size(style['bullet']['font_size']))
                        self.set_text_color(*self.resolver.get_color(style['bullet']['color']))
                        self.set_x(self.layout['bullet_indent'])
                        self.multi_cell(0, style['bullet']['height'], f"•  {bullet}")
            
            self.ln(self.resolver.get_spacing(style['spacing_after_project']))
    
    def render_education(self, education):
        """Render education section"""
        style = self.resolver.get_section_style('education')
        
        for edu in education:
            if not edu.get('institution', '').strip():
                continue
            
            self.set_font('DejaVu', 'B', self.resolver.get_font_size(style['institution']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['institution']['color']))
            self.cell(self.layout['name_cell_width'], style['institution']['height'], edu['institution'], ln=False)
            
            self.set_font('DejaVu', '', self.resolver.get_font_size(style['date']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['date']['color']))
            self.cell(self.layout['date_cell_width'], style['date']['height'], edu['date'], ln=True, align='R')
            
            self.set_font('DejaVu', '', self.resolver.get_font_size(style['degree']['font_size']))
            self.set_text_color(*self.resolver.get_color(style['degree']['color']))
            self.cell(0, style['degree']['height'], edu['degree'], ln=True)
            
            self.ln(self.resolver.get_spacing(style['spacing_after']))


    def render_columns(self, items, section_name):
        """Render column-based sections (languages, skills) - UNIFIED METHOD"""
        style = self.resolver.get_section_style(section_name)
        col_layout = self.resolver.get_column_layout(section_name)
        
        col_count = 0
        start_x = self.get_x()
        start_y = self.get_y()
        
        for item in items:
            # Support both dataclass and dict
            if hasattr(item, 'title'):
                title = item.title
                text = item.text
            else:
                title = item.get('title', item.get('language', item.get('category', '')))
                text = item.get('text', item.get('proficiency', item.get('skills', '')))
            
            if not str(title).strip():
                continue
            
            x_pos = start_x + (col_count * col_layout['column_width'])
            self.set_xy(x_pos, start_y)
            
            # Title (bold)
            self.set_font('DejaVu', 'B', self.resolver.get_font_size(style['language']['font_size']))
            self.set_text_color(*self.resolver.get_color('primary'))
            self.cell(col_layout['column_cell_width'], style['language']['height'], str(title), ln=False)
            
            # Text (regular)
            self.set_xy(x_pos, start_y + style['language']['height'])
            self.set_font('DejaVu', '', self.resolver.get_font_size(style['proficiency']['font_size']))
            self.set_text_color(*self.resolver.get_color('primary'))
            self.cell(col_layout['column_cell_width'], style['proficiency']['height'], str(text), ln=False)
            
            col_count += 1
            if col_count >= col_layout['column_count']:
                col_count = 0
                start_y += col_layout['row_spacing']
        
        self.ln(self.resolver.get_spacing(style['spacing_after']))

    # Update render_languages and render_skills to call the unified method
    def render_languages(self, languages):
        """Render languages in columns"""
        self.render_columns(languages, 'languages')

    def render_skills(self, skills):
        """Render skills in columns"""
        self.render_columns(skills, 'skills')

    # ============================================
    # MAIN GENERATE METHOD
    # ============================================
    
    def generate(self, contact_info, jobs, education=None, languages=None, 
                 skills=None, mode='nested', section_order=None, output_filename=None):
        """
        Generate complete CV PDF
        
        Args:
            contact_info (dict): Personal info
            jobs (list): Work experience with nested projects
            education (list): Education items
            languages (list): Language items
            skills (list): Skills items
            mode (str): 'nested' or 'separate'
            section_order (list): Custom section order
            output_filename (str): Output filename
        
        Returns:
            str: Path to generated PDF
        """
        # Defaults
        education = education or []
        languages = languages or []
        skills = skills or []
        
        # Set mode
        CONFIG['mode'] = mode.lower()
        
        # Get section order
        if section_order is None:
            section_order = SECTION_ORDER.get(CONFIG['mode'], SECTION_ORDER['nested'])
        
        # Prepare data based on mode
        if CONFIG['mode'] == 'nested':
            jobs_to_render = jobs
            projects_to_render = []
        else:
            jobs_to_render = self._strip_projects_from_jobs(jobs)
            projects_to_render = self._extract_all_projects(jobs)
        
        # Setup PDF
        self.add_page()
        self.set_auto_page_break(auto=True, margin=CONFIG['margins']['bottom'])
        self.set_margins(
            left=CONFIG['margins']['left'],
            top=CONFIG['margins']['top'],
            right=CONFIG['margins']['right']
        )
        
        # Render header
        self.render_header(contact_info)
        
        # Define renderers
        renderers = {
            'work_experience': lambda: self.render_work_experience(
                jobs_to_render, include_projects=(CONFIG['mode'] == 'nested')
            ),
            'projects': lambda: self.render_projects(projects_to_render),
            'education': lambda: self.render_education(education),
            'languages': lambda: self.render_languages(languages),
            'skills': lambda: self.render_skills(skills),
        }
        
        # Render sections in order
        for section_type in section_order:
            if section_type in renderers:
                title = SECTION_TITLES.get(section_type, section_type.upper())
                self.render_section_title(title)
                renderers[section_type]()
        
        # Set metadata
        self.set_title(f"{contact_info['name']} - CV")
        self.set_author(contact_info['name'])
        self.set_subject('Curriculum Vitae')
        
        # Generate filename
        if output_filename is None:
            safe_name = contact_info['name'].replace(', ', '_').replace(' ', '_')
            output_filename = f"{safe_name}_CV.pdf"
        
        # Save
        self.output(output_filename)
        
        return output_filename
    
    # ============================================
    # HELPER METHODS
    # ============================================
    
    @staticmethod
    def _extract_all_projects(jobs):
        """Extract all projects from jobs into a flat list"""
        all_projects = []
        for job in jobs:
            if job.get('projects'):
                for project in job['projects']:
                    project_with_context = project.copy()
                    project_with_context['job_position'] = job.get('position', '')
                    project_with_context['job_company'] = job.get('company', '')
                    if not project_with_context.get('date'):
                        project_with_context['date'] = job.get('date', '')
                    all_projects.append(project_with_context)
        return all_projects
    
    @staticmethod
    def _strip_projects_from_jobs(jobs):
        """Return jobs without projects"""
        jobs_without_projects = []
        for job in jobs:
            job_copy = job.copy()
            job_copy.pop('projects', None)
            jobs_without_projects.append(job_copy)
        return jobs_without_projects