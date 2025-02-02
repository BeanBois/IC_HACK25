import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class PlayerSheet:
    def __init__(self, blank_sheet_path):
        self.player_sheet = pd.read_csv(blank_sheet_path)
        self.questions = list(self.player_sheet['Question'])
        self.score = list(self.player_sheet['Score'])

        self.personality_result_dict = {
            'Agreeableness': 0,
            'Openness': 0,
            'Neuroticism': 0,
            'Conscientiousness': 0,
            'Extraversion': 0
        }

    def update_player_sheet(self, model_val_array):
        if len(model_val_array) != len(self.player_sheet['Score']):
            raise ValueError(f"Length mismatch: Expected {len(self.player_sheet['Score'])}, but got {len(model_val_array)}")

        self.player_sheet.loc[:, 'Score'] = model_val_array
        self.score = list(self.player_sheet['Score'])

    def calculate_traits(self):
        for key in self.personality_result_dict.keys():
            indices = self.player_sheet[self.player_sheet['Trait'] == key].index
            scores = self.player_sheet.loc[indices, 'Score'].tolist()
            reverse_flags = self.player_sheet.loc[indices, 'Reverse?'].tolist()

            adjusted_scores = [
                6 - score if reverse == "Y" else score
                for score, reverse in zip(scores, reverse_flags)
            ]

            self.personality_result_dict[key] = sum(adjusted_scores) / len(adjusted_scores) if adjusted_scores else 0

class PersonalityReport:
    def __init__(self, personality_result_dict):
        self.personality_result_dict = personality_result_dict
        self.personality_descriptions = {
            "Openness": "Openness reflects a person’s degree of intellectual curiosity, creativity, and preference for novelty",
            "Conscientiousness": "Conscientiousness describes a person’s level of organization, dependability, and work ethic",
            "Extraversion": "Extraversion is associated with sociability, enthusiasm, and the tendency to seek stimulation in social settings",
            "Agreeableness": "Agreeableness refers to a person’s tendency to be compassionate and cooperative towards others",
            "Neuroticism": "Neuroticism measures emotional stability and the tendency to experience negative emotions"
        }

    def plot_personality_type(self):
        labels = list(self.personality_result_dict.keys())
        values = list(self.personality_result_dict.values())

        values.append(values[0])  # Close the radar chart
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        angles = np.append(angles, angles[0])

        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(polar=True))

        ax.fill(angles, values, color='blue', alpha=0.25)
        ax.plot(angles, values, color='blue', linewidth=2)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=12)
        ax.set_ylim(1, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.tick_params(axis='x', pad=35)

        plt.savefig("personality_chart.png", bbox_inches='tight', pad_inches=0.1)  # Adjusted saving settings
        plt.close()

    def generate_report(self):
        sorted_traits = sorted(self.personality_result_dict.items(), key=lambda x: x[1], reverse=True)
        top_3_traits = sorted_traits[:3]

        # Create a ReportLab canvas to generate the PDF
        pdf_path = "personality_report.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Title Section
        c.setFont("Helvetica-Bold", 24)
        c.drawString(200, 750, "Personality Report")
        
        c.setFont("Helvetica", 10)
        c.drawString(200, 720, f"Date: {self.get_current_date()}")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 680, "Personality Chart:")
        
        y_position = 375  # Set the image's vertical position lower to avoid overlap
        c.drawImage("personality_chart.png", 125, y_position, width=400, height=300)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_position - 20, "Your Top Personality Traits:")

        y_position -= 40  # Adjust y_position to give space after the image
        for trait, _ in top_3_traits:
            description = self.personality_descriptions.get(trait, "No description available.")
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_position, f"{trait}:")
            y_position -= 15
            c.setFont("Helvetica", 10)
            # Ensure description fits within the page
            for line in description.split(". "):
                c.drawString(50, y_position, line + ".")
                y_position -= 15
                if y_position < 100:  # If we're too close to the bottom, add a new page
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y_position = 750  # Reset y position for new page
            y_position -= 25  # Add extra space between traits

        # Save the PDF
        c.showPage()  # End current page
        c.save()

        print(f"Report saved as {pdf_path}")

        # Automatically open the PDF (for macOS and Windows)
        self.open_pdf(pdf_path)

    def get_current_date(self):
        from datetime import datetime
        return datetime.today().strftime('%Y-%m-%d')

    def open_pdf(self, pdf_path):
        import os
        if os.name == 'posix':
            os.system(f"open {pdf_path}")
        else:
            os.system(f"start {pdf_path}")

# Example Usage
p1 = PlayerSheet('csv/BFI_44.csv')

# Generating random scores for testing
model_val_array = [random.randint(1, 5) for _ in range(44)]
p1.update_player_sheet(model_val_array)
p1.calculate_traits()

# Create a PersonalityReport instance and generate results
report = PersonalityReport(p1.personality_result_dict)
report.plot_personality_type()
report.generate_report()