#!/usr/bin/env python3
"""
PDF Generator for creating custom clinical and insurance documents for testing the RAG system.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

def create_clinical_document_pdf(filename: str = "sample_clinical_document.pdf"):
    """Create a sample clinical document PDF for testing."""

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("CLINICAL MEDICAL RECORD", title_style))
    story.append(Spacer(1, 12))

    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", styles['Heading2']))
    patient_data = [
        ["Patient ID:", "MRN-2024-001"],
        ["Name:", "Sarah Johnson"],
        ["Date of Birth:", "March 15, 1985"],
        ["Gender:", "Female"],
        ["Address:", "123 Health Street, Medical City, MC 12345"],
        ["Phone:", "(555) 123-4567"],
        ["Insurance Provider:", "MediCare Plus"],
        ["Policy Number:", "MCP-789012345"]
    ]

    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 20))

    # Medical History
    story.append(Paragraph("MEDICAL HISTORY", styles['Heading2']))

    medical_content = """
    <b>Chief Complaint:</b> Patient presents with persistent hypertension and occasional chest pain.

    <b>History of Present Illness:</b> The patient reports having high blood pressure for the past 5 years.
    She has been taking antihypertensive medication but reports inconsistent compliance due to side effects.
    Recent episodes of chest pain have been mild and resolve with rest. No associated symptoms such as
    shortness of breath, nausea, or diaphoresis.

    <b>Past Medical History:</b>
    • Hypertension (diagnosed 2019)
    • Type 2 Diabetes Mellitus (diagnosed 2020)
    • Hyperlipidemia
    • No history of cardiovascular events

    <b>Medications:</b>
    • Lisinopril 10mg daily
    • Metformin 500mg twice daily
    • Atorvastatin 20mg daily
    • Aspirin 81mg daily

    <b>Allergies:</b> No known drug allergies. Environmental allergies to pollen.

    <b>Social History:</b> Non-smoker, occasional alcohol consumption (1-2 drinks/week).
    Works as a teacher. Exercises 3 times per week. Married with two children.

    <b>Family History:</b> Father had myocardial infarction at age 65. Mother has hypertension.
    No family history of diabetes or cancer.
    """

    story.append(Paragraph(medical_content, styles['Normal']))
    story.append(Spacer(1, 20))

    # Vital Signs
    story.append(Paragraph("VITAL SIGNS", styles['Heading2']))
    vital_data = [
        ["Date/Time", "BP", "HR", "Temp", "Weight", "BMI"],
        ["2024-01-15 09:00", "148/92", "78", "98.6°F", "165 lbs", "27.2"],
        ["2024-01-10 14:30", "152/94", "82", "98.4°F", "166 lbs", "27.4"],
        ["2023-12-20 11:15", "145/88", "75", "98.8°F", "164 lbs", "27.0"]
    ]

    vital_table = Table(vital_data, colWidths=[1.5*inch, 1*inch, 0.8*inch, 1*inch, 1*inch, 0.8*inch])
    vital_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(vital_table)
    story.append(Spacer(1, 20))

    # Assessment and Plan
    story.append(Paragraph("ASSESSMENT AND PLAN", styles['Heading2']))

    assessment_content = """
    <b>Assessment:</b>
    1. Hypertension, poorly controlled - Blood pressure readings consistently above target goals.
    2. Type 2 Diabetes Mellitus, well controlled - Recent A1c of 6.8%.
    3. Hyperlipidemia - LDL cholesterol elevated despite statin therapy.
    4. Chest pain, atypical - Likely musculoskeletal in origin, but cardiac workup recommended.

    <b>Plan:</b>
    1. Adjust antihypertensive regimen: Increase Lisinopril to 20mg daily, add Amlodipine 5mg daily.
    2. Continue current diabetes management with lifestyle modifications and metformin.
    3. Increase Atorvastatin to 40mg daily for better lipid control.
    4. Order cardiac workup: EKG, echocardiogram, and stress test.
    5. Lifestyle counseling: Weight management, increased physical activity, DASH diet.
    6. Follow-up appointment in 2 weeks to review test results and medication adjustments.
    7. Daily home blood pressure monitoring.

    <b>Patient Education:</b> Discussed importance of medication compliance, lifestyle modifications,
    and warning signs of cardiovascular events. Provided educational materials on hypertension management.
    """

    story.append(Paragraph(assessment_content, styles['Normal']))
    story.append(Spacer(1, 20))

    # Provider Information
    story.append(Paragraph("PROVIDER INFORMATION", styles['Heading2']))
    provider_data = [
        ["Provider:", "Dr. Michael Chen, MD"],
        ["Specialty:", "Internal Medicine"],
        ["License:", "MD123456"],
        ["Date:", "January 15, 2024"],
        ["Next Appointment:", "January 29, 2024"]
    ]

    provider_table = Table(provider_data, colWidths=[2*inch, 4*inch])
    provider_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(provider_table)

    doc.build(story)
    print(f"Clinical document PDF created: {filename}")

def create_insurance_document_pdf(filename: str = "sample_insurance_document.pdf"):
    """Create a sample insurance document PDF for testing."""

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("INSURANCE CLAIM DOCUMENT", title_style))
    story.append(Spacer(1, 12))

    # Claim Information
    story.append(Paragraph("CLAIM INFORMATION", styles['Heading2']))
    claim_data = [
        ["Claim Number:", "CLM-2024-789012"],
        ["Policy Number:", "POL-2023-456789"],
        ["Claimant Name:", "Sarah Johnson"],
        ["Date of Service:", "January 10, 2024"],
        ["Date Filed:", "January 12, 2024"],
        ["Claim Type:", "Medical Expense"],
        ["Total Claimed Amount:", "$2,450.00"],
        ["Insurance Provider:", "MediCare Plus"]
    ]

    claim_table = Table(claim_data, colWidths=[2.5*inch, 3.5*inch])
    claim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(claim_table)
    story.append(Spacer(1, 20))

    # Service Details
    story.append(Paragraph("SERVICE DETAILS", styles['Heading2']))

    service_content = """
    <b>Provider Information:</b>
    Medical Center Hospital
    456 Healthcare Avenue
    Medical City, MC 12345
    Provider ID: PROV-001234

    <b>Services Rendered:</b>

    1. <b>Office Visit - Internal Medicine</b>
       • CPT Code: 99214
       • Diagnosis: I10 (Hypertension)
       • Charge: $180.00
       • Allowed: $145.00

    2. <b>Comprehensive Metabolic Panel</b>
       • CPT Code: 80053
       • Diagnosis: I10, E11.9 (Type 2 Diabetes)
       • Charge: $125.00
       • Allowed: $98.00

    3. <b>Lipid Panel</b>
       • CPT Code: 80061
       • Diagnosis: E78.5 (Hyperlipidemia)
       • Charge: $95.00
       • Allowed: $76.00

    4. <b>Hemoglobin A1c</b>
       • CPT Code: 83036
       • Diagnosis: E11.9 (Type 2 Diabetes)
       • Charge: $85.00
       • Allowed: $68.00

    5. <b>Electrocardiogram (EKG)</b>
       • CPT Code: 93000
       • Diagnosis: R07.9 (Chest pain)
       • Charge: $150.00
       • Allowed: $120.00

    6. <b>Echocardiogram</b>
       • CPT Code: 93306
       • Diagnosis: R07.9 (Chest pain)
       • Charge: $850.00
       • Allowed: $680.00

    7. <b>Cardiac Stress Test</b>
       • CPT Code: 93015
       • Diagnosis: R07.9 (Chest pain)
       • Charge: $985.00
       • Allowed: $788.00
    """

    story.append(Paragraph(service_content, styles['Normal']))
    story.append(Spacer(1, 20))

    # Claim Summary
    story.append(Paragraph("CLAIM SUMMARY", styles['Heading2']))
    summary_data = [
        ["Total Billed Amount:", "$2,470.00"],
        ["Contractual Adjustments:", "-$197.60"],
        ["Patient Responsibility:", "-$150.00"],
        ["Insurance Approved Amount:", "$2,122.40"],
        ["Amount Paid:", "$2,122.40"],
        ["Patient Balance:", "$0.00"],
        ["Claim Status:", "APPROVED"]
    ]

    summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # Explanation of Benefits
    story.append(Paragraph("EXPLANATION OF BENEFITS", styles['Heading2']))

    eob_content = """
    This claim has been processed according to the terms of your MediCare Plus health insurance policy.
    All services were determined to be medically necessary and covered under your policy benefits.

    <b>Coverage Details:</b>
    • Preventive care services: 100% covered
    • Diagnostic tests: 80% covered after deductible
    • Specialist visits: 70% covered after deductible

    <b>Important Notes:</b>
    • Your deductible for 2024 has been met.
    • No pre-authorization was required for these services.
    • All providers are in-network with preferred rates applied.
    • If you have questions about this claim, please contact customer service at 1-800-MEDI-PLUS.

    <b>Appeal Rights:</b> If you disagree with this determination, you have the right to appeal this decision
    within 180 days of the date on this notice. Contact your insurance provider for appeal procedures.
    """

    story.append(Paragraph(eob_content, styles['Normal']))
    story.append(Spacer(1, 20))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=1
    )
    story.append(Paragraph("This is an electronically generated document for demonstration purposes.", footer_style))

    doc.build(story)
    print(f"Insurance document PDF created: {filename}")

if __name__ == "__main__":
    # Create both sample documents
    create_clinical_document_pdf()
    create_insurance_document_pdf()
    print("Both sample PDFs created successfully!")