import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak

# ==========================================
# PAGE NUMBERING & CANVAS CLASS
# ==========================================
class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render running footers with total page count.
    Suppresses headers/footers on the cover page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))

        # Running Header
        self.drawString(54, 750, "Salifort Motors | HR Analytics Executive Summary Report")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)

        # Running Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL - INTERNAL HR & EXECUTIVE USE ONLY")
        self.line(54, 48, 612 - 54, 48)

        self.restoreState()


# ==========================================
# REPORT GENERATOR CLASS
# ==========================================
class HRReportGenerator:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.pdf_path = os.path.join(base_dir, "reports", "executive_summary_report.pdf")
        
        # Ensure directories exist
        os.makedirs(os.path.join(base_dir, "reports"), exist_ok=True)

        # Data & Image Paths
        self.charts_dir = os.path.join(base_dir, "outputs", "charts")
        self.tables_dir = os.path.join(base_dir, "outputs", "tables")

        # Color Palette - Professional Corporate Navy/Slate
        self.c_primary = colors.HexColor("#1A365D")    # Deep Navy
        self.c_secondary = colors.HexColor("#2B6CB0")  # Slate Blue
        self.c_accent = colors.HexColor("#319795")     # Teal Accent
        self.c_dark = colors.HexColor("#2D3748")       # Body Text Dark Charcoal
        self.c_light = colors.HexColor("#F7FAFC")      # Light Off-White Table Background
        self.c_border = colors.HexColor("#E2E8F0")     # Light Grey Border

        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Build custom ParagraphStyle objects for professional typography."""
        self.styles.add(ParagraphStyle(
            'CoverTitle',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=26,
            leading=32,
            textColor=self.c_primary,
            alignment=0,
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            'CoverSubtitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=14,
            leading=18,
            textColor=self.c_secondary,
            alignment=0,
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            'CoverMeta',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=self.c_dark
        ))
        self.styles.add(ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=self.c_primary,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        ))
        self.styles.add(ParagraphStyle(
            'SubSectionHeader',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=self.c_secondary,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        ))
        self.styles.add(ParagraphStyle(
            'BodyCustom',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=self.c_dark,
            spaceAfter=8
        ))
        self.styles.add(ParagraphStyle(
            'BulletCustom',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=self.c_dark,
            leftIndent=15,
            firstLineIndent=-10,
            spaceAfter=4
        ))
        self.styles.add(ParagraphStyle(
            'CalloutText',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9.5,
            leading=13.5,
            textColor=self.c_primary
        ))
        self.styles.add(ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
            alignment=1
        ))
        self.styles.add(ParagraphStyle(
            'TableCell',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10.5,
            textColor=self.c_dark,
            alignment=1
        ))
        self.styles.add(ParagraphStyle(
            'TableCellLeft',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10.5,
            textColor=self.c_dark,
            alignment=0
        ))

    def _get_callout_box(self, text, width=504):
        """Creates an executive callout box with a colored left accent border."""
        p = Paragraph(text, self.styles['CalloutText'])
        t = Table([[p]], colWidths=[width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
            ('LINELEFT', (0,0), (0,0), 4, self.c_secondary),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        return t

    def _csv_to_table(self, csv_filename, col_widths, align_left_cols=[0]):
        """Helper to convert CSV files to styled ReportLab Tables safely."""
        path = os.path.join(self.tables_dir, csv_filename)
        if not os.path.exists(path):
            return Paragraph(f"<i>Table data missing: {csv_filename}</i>", self.styles['BodyCustom'])
        
        df = pd.read_csv(path)
        table_data = []

        # Headers
        headers = [Paragraph(str(c), self.styles['TableHeader']) for c in df.columns]
        table_data.append(headers)

        # Rows
        for _, row in df.iterrows():
            row_cells = []
            for col_idx, val in enumerate(row):
                style = self.styles['TableCellLeft'] if col_idx in align_left_cols else self.styles['TableCell']
                row_cells.append(Paragraph(str(val), style))
            table_data.append(row_cells)

        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), self.c_primary),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, self.c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, self.c_light]),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        return t

    def build_pdf(self):
        doc = SimpleDocTemplate(
            self.pdf_path,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        story = []

        # ==========================================
        # COVER / HEADER BLOCK
        # ==========================================
        story.append(Spacer(1, 10))
        story.append(Paragraph("SALIFORT MOTORS HR ANALYTICS", self.styles['CoverSubtitle']))
        story.append(Paragraph("Executive Summary & Workforce Attrition Report", self.styles['CoverTitle']))
        story.append(Paragraph("<b>Author:</b> Data Analytics & Insights Team | <b>Target:</b> Leadership & HR Steering Committee", self.styles['CoverMeta']))
        story.append(Spacer(1, 10))
        
        # Decorative colored bar
        banner_table = Table([[""]], colWidths=[504], rowHeights=[4])
        banner_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), self.c_secondary),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(banner_table)
        story.append(Spacer(1, 15))

        # ==========================================
        # 1. EXECUTIVE SUMMARY & BUSINESS PROBLEM
        # ==========================================
        story.append(Paragraph("1. Executive Summary & Business Problem", self.styles['SectionHeader']))
        
        callout_msg = (
            "<b>Key Finding:</b> Employee attrition at Salifort Motors is primarily driven by "
            "extreme workload imbalance (overworked high-performers vs. underutilized staff), "
            "a near-total stagnation in promotions, and systemic burnout among mid-tenure employees."
        )
        story.append(self._get_callout_box(callout_msg))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "Salifort Motors' Human Resources department initiated this data analytics project to address "
            "elevated turnover rates. Turnover incurs severe operational costs, including recruitment, onboarding, "
            "lost technical expertise, and disrupted project continuity. The business goal is to answer a central question: "
            "<i>What factors are most strongly associated with an employee's decision to leave?</i>",
            self.styles['BodyCustom']
        ))
        story.append(Paragraph(
            "Through comprehensive Exploratory Data Analysis (EDA) and Predictive Machine Learning Modeling "
            "(Logistic Regression, Decision Trees, and Random Forest), this report provides data-backed "
            "insights to enable proactive, targeted HR interventions.",
            self.styles['BodyCustom']
        ))

        # ==========================================
        # 2. DATA OVERVIEW & CLEANING
        # ==========================================
        story.append(Paragraph("2. Data Overview & Data Hygiene", self.styles['SectionHeader']))
        story.append(Paragraph(
            "The initial dataset comprised <b>14,999 employee records</b> across 10 key features. "
            "A rigorous data hygiene audit revealed <b>3,008 duplicate records (20.05%)</b>. "
            "Given the presence of fine-grained continuous metrics (e.g., exact satisfaction scores and evaluation grades), "
            "identical cross-variable matches were deemed duplicate entries rather than genuine distinct employees.",
            self.styles['BodyCustom']
        ))
        
        clean_metrics = [
            "• <b>Raw Records:</b> 14,999 rows | <b>Cleaned Unique Dataset:</b> 11,991 rows (saved to <code>df_clean.csv</code>).",
            "• <b>Overall Attrition Rate:</b> 16.60% (1,991 left vs. 10,000 retained) in the clean dataset.",
            "• <b>Outlier Handling:</b> Extreme tenure values (6+ years) were identified. Outliers were excluded for linear models (Logistic Regression) to preserve statistical validity, but retained for non-parametric tree models."
        ]
        for m in clean_metrics:
            story.append(Paragraph(m, self.styles['BulletCustom']))
        story.append(PageBreak())

        # ==========================================
        # 3. EXPLORATORY DATA ANALYSIS (EDA)
        # ==========================================
        story.append(Paragraph("3. Key Exploratory Data Analysis Insights", self.styles['SectionHeader']))
        
        # Sub-section: Workload & Overwork
        story.append(Paragraph("3.1 Workload & Project Distribution Imbalance", self.styles['SubSectionHeader']))
        story.append(Paragraph(
            "Analysis demonstrates a stark bimodal distribution in employee turnover driven by project load and monthly hours:",
            self.styles['BodyCustom']
        ))
        
        eda_bullets = [
            "• <b>The Overworked High-Performers:</b> Employees assigned to 6 or 7 projects face a catastrophic attrition rate. 100% of employees assigned to 7 projects left the company, logging an average of ~275+ monthly hours.",
            "• <b>The Underutilized Disengaged:</b> Employees assigned to only 2 projects also exhibited high turnover (~54.17%), logging substantially low hours (~140-160 hours/month) and reporting low evaluation scores.",
            "• <b>The Optimal Zone:</b> Employees working on 3 to 4 projects displayed the lowest turnover rates and highest satisfaction."
        ]
        for b in eda_bullets:
            story.append(Paragraph(b, self.styles['BulletCustom']))
        story.append(Spacer(1, 8))

           # Chart 1: Number of Projects & Hours by Evaluation
        img_proj = os.path.join(self.charts_dir, "number_of_projects.png")
        img_eval = os.path.join(self.charts_dir, "avg_monthly_hrs_by_evaluation_score.png")
        
        if os.path.exists(img_proj):
            story.append(Image(img_proj, width=450, height=200))
            story.append(Spacer(1, 10)) # Space between chart 1 and chart 2
            
        if os.path.exists(img_eval):
            story.append(Image(img_eval, width=450, height=200))
            story.append(Spacer(1, 10)) # Space after chart 2
            story.append(PageBreak())

        # Attrition Table
        story.append(Paragraph("<b>Table 1: Attrition Summary by Project Load</b>", self.styles['BodyCustom']))
        story.append(self._csv_to_table("attrition_per_project.csv", col_widths=[80, 100, 100, 100, 124], align_left_cols=[0]))
        story.append(PageBreak())

        # Sub-section: Tenure & Career Progression
        story.append(Paragraph("3.2 Tenure, Stagnation & Promotion Deficit", self.styles['SubSectionHeader']))
        story.append(Paragraph(
            "Career progression metrics highlight a severe bottleneck in talent retention at the 4-to-5 year tenure mark:",
            self.styles['BodyCustom']
        ))
        
        prog_bullets = [
            "• <b>The 4-5 Year Career Cliff:</b> Employee satisfaction drops sharply at 4 years of tenure. Peak turnover occurs between years 4 and 5, driven by lack of promotion and unrewarded high performance.",
            "• <b>Promotion Stagnation:</b> Overall, only <b>2.1%</b> of employees received a promotion in the last 5 years. Among employees who left, virtually zero had received a promotion.",
            "• <b>Salary Dynamics:</b> Low and medium salary tiers account for over 90% of all turnover. High-salary employees exhibit high retention regardless of department."
        ]
        for b in prog_bullets:
            story.append(Paragraph(b, self.styles['BulletCustom']))
        story.append(Spacer(1, 8))

        # Chart 2: Tenure & Promotion
        img_tenure = os.path.join(self.charts_dir, "satisfaction_by_tenure.png")
        img_promo = os.path.join(self.charts_dir, "avg_monthly_hrs_by_promotion.png")
        
        if os.path.exists(img_tenure):
            story.append(Image(img_tenure, width=450, height=200))
            story.append(Spacer(1, 10))  # Space between tenure chart and promo chart

        if os.path.exists(img_promo):
            story.append(Image(img_promo, width=450, height=200))
            story.append(Spacer(1, 10))  # Space after promo chart

        story.append(PageBreak()) # Clean transition to Modeling & Strategic Recommendations

        # ==========================================
        # 4. PREDICTIVE MODELING & PERFORMANCE
        # ==========================================
        story.append(Paragraph("4. Predictive Analytics & Model Comparison", self.styles['SectionHeader']))
        story.append(Paragraph(
            "Multiple machine learning models were trained, tuned, and evaluated to forecast attrition risk, with tree-based models significantly outperforming the linear baseline. Cross-validation and hyperparameter tuning were applied to prevent overfitting.",
            self.styles['BodyCustom']
        ))

        story.append(Paragraph("<b>Table 2: Machine Learning Model Performance Metrics</b>", self.styles['BodyCustom']))
        story.append(self._csv_to_table("model_comparison.csv", col_widths=[130, 80, 80, 80, 80], align_left_cols=[0]))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "<b>Model Insights:</b> The tuned <b>Random Forest Model (RF2)</b> was selected as the optimal champion model, achieving an F1-score of 0.89 and an AUC-ROC of 0.97, with key drivers identified as satisfaction level, project count, tenure, and average monthly hours. The full analysis and model performance metrics are available in the provided report.",
            self.styles['BodyCustom']
        ))
        story.append(Spacer(1, 8))

        # Chart 3: Model Evaluation Visuals
        img_feat = os.path.join(self.charts_dir, "random_forest2_feature_importance.png")
        img_roc = os.path.join(self.charts_dir, "roc_curve_comparison.png")
        if os.path.exists(img_feat) and os.path.exists(img_roc):
            img_table3 = Table([
                [Image(img_feat, width=245, height=160), Image(img_roc, width=245, height=160)]
            ], colWidths=[252, 252])
            img_table3.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(img_table3)
            story.append(PageBreak())

        # ==========================================
        # 5. ACTIONABLE HR RECOMMENDATIONS
        # ==========================================
        story.append(Paragraph("5. Strategic HR Recommendations & Action Plan", self.styles['SectionHeader']))
        story.append(Paragraph(
            "Based on empirical findings and predictive modeling, Salifort Motors leadership should implement the following strategic measures:",
            self.styles['BodyCustom']
        ))

        recs = [
            ("1. Cap Workload & Restructure Project Allocation", 
             "Institute a hard cap of 5 projects per employee. Distribute tasks more evenly so no staff member exceeds 215 monthly hours. Re-engage underutilized employees (2 projects) with mentorship and clearer assignments."),
            
            ("2. Establish Clear Career Growth & Promotion Pathways", 
             "Address the severe promotion stagnation (<2.1% in 5 years). Introduce structured tenure-based reviews at year 3 and 4 to proactively retain mid-level talent before satisfaction drops."),
            
            ("3. Re-evaluate Compensation Structure for High-Performers", 
             "Align compensation with workload and performance evaluation scores. Ensure high-performing employees logging significant hours are rewarded with competitive salary adjustments rather than extra work alone."),
            
            ("4. Deploy Early Warning Attrition Risk Tracking", 
             "Integrate the Random Forest predictive model into quarterly HR reviews to identify 'at-risk' employees (e.g., 5+ projects, high hours, no promotion) and execute stay-interviews before resignation.")
        ]

        for title, desc in recs:
            rec_content = [
                Paragraph(f"<b>{title}</b>", self.styles['SubSectionHeader']),
                Paragraph(desc, self.styles['BodyCustom'])
            ]
            story.append(KeepTogether(rec_content))
            story.append(Spacer(1, 4))

        # Build Document
        doc.build(story, canvasmaker=NumberedCanvas)
        print(f"Report successfully generated at: {self.pdf_path}")


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # Resolve current project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    
    generator = HRReportGenerator(project_root)
    generator.build_pdf()