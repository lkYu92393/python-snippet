from data import ColumnItem
from generator import CVGenerator

contact = {
    "name": "NAME HERE",
    "email": "YOUR@EMAIL.XYZ",
    "phone": "12345678",
    "github": "github.com/link",
    "current_salary": 100000,
    "expected_salary": 200000,
    "available_date": "DD MMM YYYY"
}

jobs = [
    {
        "position": "Job 1",
        "company": "Company 1",
        "date": "Aug 2024 – Mar 2026",
        "projects": [
            {
                "name": "Project 1",
                "tech_stack": "C#, python, HTML5, JavaScript, MySQL",
                "description": "GOOD THING",
                "bullets": [
                    "Use of low code framework",
                    "Participated in designing implementation of features",
                    "Experience in dealing with users"
                ]
            }
        ]
    },
    {
        "position": "Job 2",
        "company": "Company 2",
        "date": "Jan 2022 – Aug 2024",
        "projects": [
            {
                "name": "Good Project",
                "tech_stack": "C#, HTML5, Javascript, SQLServer",
                "description": "Some more good things",
                "bullets": [
                    "Good people",
                    "Spearhead several features design and implementations"
                ]
            },
            {
                "name": "Good Project 2",
                "tech_stack": "ReactJS, NodeJS, Python",
                "description": "Something is done",
                "bullets": [
                    "NICE"
                ]
            }
        ]
    },
    {
        "position": "Job 3",
        "company": "Eternal Technology Consultant",
        "date": "Aug 2021 – Dec 2021",
        "projects": [
            {
                "name": "Another Project",
                "tech_stack": "C#, SQL Server",
                "description": "Good thing.",
                "bullets": []
            },
            {
                "name": "More Project",
                "tech_stack": "C#",
                "description": "More Good thing.",
                "bullets": []
            }
        ]
    }
]

# Education
education = [
    {
        "institution": "Some School",
        "degree": "More degree",
        "date": "Sep 2021 – Dec 2023"
    },
    {
        "institution": "Another School",
        "degree": "Bachelor degree",
        "date": "Sep 2012 – Aug 2015"
    }
]

# Languages
languages = [
    ColumnItem(title="English", text="Good"),
    ColumnItem(title="Cantonese", text="Native speaker"),
]

# Skills
skills = [
    ColumnItem(title="Slacking", text="Epic"),
    ColumnItem(title="Making bad decision", text="Legendary"),
]

cv = CVGenerator()
output = cv.generate(
    contact_info=contact,
    jobs=jobs,
    education=education,
    languages=languages,
    skills=skills,
    mode='nested',
    output_filename='some_CV.pdf'
)

print("\n🎉 Done! Check your folder for the PDFs.")