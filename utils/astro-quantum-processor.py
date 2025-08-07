import csv
from datetime import datetime
from collections import defaultdict
import os
from pathlib import Path
import logging

class AstroNarrativeProcessor:
    def __init__(self):
        # Setup paths and logging as before...
        self.project_dir = Path(os.path.join(Path.home(), 'Documents', 'AstroQuantum2025'))
        self.data_dir = self.project_dir / 'data'
        self.output_dir = self.project_dir / 'output'
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'astro_narrative.log'),
                logging.StreamHandler()
            ]
        )

        # Planet and aspect qualities remain the same...
        self.planet_qualities = {
            # ...
        }
        
        self.aspect_qualities = {
            # ...
        }

    def parse_date(self, date_str):
        """Parse date string in format 'MMM d, YYYY'"""
        try:
            return datetime.strptime(date_str.strip(), '%b %d, %Y').date()
        except ValueError as e:
            logging.warning(f"Failed to parse date: {date_str} - {str(e)}")
            return None

    def generate_interpretation(self, aspect):
        """
        Generate descriptive interpretation of an aspect with proper grammar
        """
        planet1 = self.planet_qualities.get(aspect['planet1'], 
                                           {'themes': ['Unknown', 'mystery'], 'musical': 'undefined tones'})
        planet2 = self.planet_qualities.get(aspect['planet2'], 
                                           {'themes': ['Unknown', 'mystery'], 'musical': 'undefined tones'})
        aspect_quality = self.aspect_qualities.get(aspect['aspect'].lower(), 
                                                  {'meaning': 'creating an undefined relationship', 
                                                   'musical': 'creates undefined harmonies'})

        interpretation = (
            f"{aspect['planet1']} in {aspect['sign1']} {aspect['aspect']} "
            f"{aspect['planet2']} in {aspect['sign2']} at {aspect['time']}\n\n"
            f"This aspect brings together the {', '.join(planet1['themes'][:2])} qualities of {aspect['planet1']} "
            f"with the {', '.join(planet2['themes'][:2])} qualities of {aspect['planet2']}, resulting in {aspect_quality['meaning']}. "
            f"Musically, this manifests as {planet1['musical']} interweaving with {planet2['musical']}."
        )

        return interpretation

    def read_aspects_csv(self, filename):
        """Read and parse the aspects CSV file"""
        # Rest of the code remains the same...

    def generate_ics_content(self, daily_aspects):
        """Generate the ICS calendar content"""
        ics_lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//AstroNarrativeCalendar//2025//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH'
        ]

        days_processed = 0
        for date, aspects in sorted(daily_aspects.items()):
            date_str = date.strftime("%Y%m%d")
            
            daily_interpretation = "Daily Astrological Symphony:\n\n"
            for aspect in aspects:
                daily_interpretation += self.generate_interpretation(aspect) + "\n\n"
            
            clean_interpretation = daily_interpretation.replace('\n', '\\n').replace(',', '\\,')
            
            ics_lines.extend([
                'BEGIN:VEVENT',
                f'DTSTART;VALUE=DATE:{date_str}',
                f'DTEND;VALUE=DATE:{date_str}',
                f'SUMMARY:Astrological Symphony for {date.strftime("%B %d, %Y")}',
                f'DESCRIPTION:{clean_interpretation}',
                'END:VEVENT'
            ])
            days_processed += 1

        ics_lines.append('END:VCALENDAR')
        logging.info(f"Generated ICS events for {days_processed} days")
        return '\n'.join(ics_lines)

    def process_and_save(self, input_file, output_file):
        """Process the input CSV and save as ICS"""
        # Rest of the code remains the same...

def main():
    """Main execution function"""
    try:
        processor = AstroNarrativeProcessor()
        input_file = "astrological_aspects_2025.csv"
        output_file = "astrological_symphony_2025.ics"
        
        logging.info("Starting Astrological Narrative processing")
        processor.process_and_save(input_file, output_file)
        logging.info("Processing complete")
        
    except Exception as e:
        logging.error(f"Program execution failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()