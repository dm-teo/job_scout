from fpdf import FPDF
from fpdf.enums import XPos, YPos
from matcher import get_matches
from PIL import Image
import sys
import os

def build_cv(target_link):
    skills, projects, profile_data = get_matches(target_link)

    generate_cv(profile_data, skills, projects)
    if skills is None:
        print("Skipping PDF generation for this link")
        return


def generate_cv(profile_data, skills_list, projects_list):
    original_photo = "profile_photo.jpg"
    cropped_photo = "profile_photo_processed.jpg"

    if os.path.exists(original_photo):
        img = Image.open(original_photo)
        width, height = img.size
        img_cropped = img.crop((0, 0, width, int(height * 0.75)))
        img_cropped.save(cropped_photo)

    pdf = FPDF()
    pdf.add_page()

    # --- GLOBAL SETTINGS ---
    navy = (0, 51, 102)
    black = (0, 0, 0)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)

    # --- HEADER & PHOTO ---
    if os.path.exists(cropped_photo):
        pdf.image(cropped_photo, x=155, y=12, w=40)

    pdf.set_y(15)
    pdf.set_font('Times', 'B', 26)
    pdf.set_text_color(*navy)
    pdf.cell(130, 12, profile_data['contact']['name'].upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font('Times', 'I', 13)
    pdf.cell(130, 8, "BSc Informatics Student", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Contact Info
    pdf.set_font('Times', '', 9)
    pdf.set_text_color(*black)
    c = profile_data['contact']
    pdf.cell(130, 5, f"{c['location']}  |  {c['phone']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(130, 5, f"{c['email']}  |  github.com/dm-teo", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    # --- 3. PROFESSIONAL SUMMARY ---
    pdf.set_font('Times', 'B', 12)
    pdf.set_text_color(*navy)
    pdf.cell(0, 8, "PROFESSIONAL SUMMARY", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(2)

    pdf.set_text_color(*black)
    pdf.set_font('Times', 'I', 10.5)
    pdf.multi_cell(130, 5, profile_data['introduction'], align='J')
    pdf.ln(5)

    # --- 4. TECHNICAL SKILLS (THREE COLUMNS - REFINED SPACING) ---
    pdf.set_font('Times', 'B', 12)
    pdf.set_text_color(*navy)
    pdf.cell(0, 8, "TECHNICAL SKILLS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)

    y_start_skills = pdf.get_y()
    max_y = y_start_skills

    # We define the X positions for 3 equal columns
    # Total available width is 180mm. 180 / 3 = 60mm per column.
    col_width = 60
    col_x_positions = [15, 15 + col_width, 15 + (col_width * 2)]

    for i, family in enumerate(skills_list):
        # Stop if we have more than 3 families (to keep it in one row)
        if i > 2: break

        col_x = col_x_positions[i]
        pdf.set_xy(col_x, y_start_skills)

        # Category Title
        pdf.set_font('Times', 'B', 10.5)
        pdf.set_text_color(*navy)
        pdf.cell(col_width, 6, family['category_name'], new_x=XPos.LEFT, new_y=YPos.NEXT)

        # Bullet Points
        pdf.set_font('Times', '', 10)
        pdf.set_text_color(*black)

        # We use a height of 5.5 to give the text more "air" (less crowded)
        for skill in family['skills_to_show']:
            pdf.set_x(col_x + 2)  # Tiny indent for bullets
            pdf.cell(col_width, 5.5, f"- {skill}", new_x=XPos.LEFT, new_y=YPos.NEXT)

        # Track which column is the longest to start the next section correctly
        if pdf.get_y() > max_y:
            max_y = pdf.get_y()

    # Move pen safely below the longest skill list
    pdf.set_y(max_y + 4)

    # --- 5. PROJECTS & SYSTEMS ---
    pdf.set_font('Times', 'B', 12)
    pdf.set_text_color(*navy)
    pdf.cell(0, 8, "PROJECTS & SYSTEMS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(5)

    for project in projects_list:
        pdf.set_font('Times', 'B', 11)
        pdf.set_text_color(*black)
        pdf.cell(0, 6, f"- {project['name']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font('Times', '', 10)
        for bullet in project['desc']:
            pdf.set_x(22)
            pdf.multi_cell(0, 4.2, f"> {bullet['text']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    # --- 6. EDUCATION & LANGUAGES ---
    pdf.ln(5)
    y_footer_sec = pdf.get_y()

    # Education (Left)
    pdf.set_xy(15, y_footer_sec)
    pdf.set_font('Times', 'B', 11)
    pdf.set_text_color(*navy)
    pdf.cell(90, 8, "EDUCATION", new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.line(15, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(1)
    pdf.set_text_color(*black)
    pdf.set_font('Times', 'B', 10)
    edu = profile_data['education']
    pdf.cell(85, 5, f"{edu['degree']}", new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.set_font('Times', '', 10)
    pdf.cell(85, 5, edu['university'], new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.set_font('Times', 'I', 9)
    pdf.cell(85, 5, f"Expected Graduation: {edu['status']}", new_x=XPos.LEFT, new_y=YPos.NEXT)

    # Languages (Right)
    pdf.set_xy(110, y_footer_sec)
    pdf.set_font('Times', 'B', 11)
    pdf.set_text_color(*navy)
    pdf.cell(85, 8, "LANGUAGES", new_x=XPos.LEFT, new_y=YPos.NEXT)
    pdf.line(110, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(1)
    pdf.set_text_color(*black)
    pdf.set_font('Times', '', 10)
    for lang, level in profile_data['languages'].items():
        pdf.set_x(110)
        pdf.cell(85, 5, f"{lang}: {level}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(f"CV_{profile_data['contact']['name'].replace(' ', '_')}.pdf")

for link in sys.argv[1:]:
    build_cv(link)