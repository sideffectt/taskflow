from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime


def generate_tasks_pdf(tasks: list, username: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    
    title = Paragraph(f"Tasks Report - {username}", styles["Heading1"])
    elements.append(title)
    
    
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"])
    elements.append(date_text)
    elements.append(Spacer(1, 20))
    
    if not tasks:
        elements.append(Paragraph("No tasks found.", styles["Normal"]))
    else:
        data = [["Title", "Priority", "Completed", "Created"]]
    
        for task in tasks:
            created_at = task.get("created_at", "")
            if hasattr(created_at, "strftime"):
                created_at = created_at.strftime("%Y-%m-%d")
            else:
                created_at = str(created_at)[:10] if created_at else ""
            
            data.append([
                task.get("title", ""),
                str(task.get("priority", "")),
                "Yes" if task.get("completed") else "No",
                created_at
            ])
        
        table = Table(data, colWidths=[200, 60, 70, 80])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer