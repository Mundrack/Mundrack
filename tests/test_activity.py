import importlib.util,unittest,json,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import date,timedelta
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('activity',ROOT/'scripts/refresh-activity.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ActivityTests(unittest.TestCase):
    def markup(self):
        start=date(2025,9,27)
        return ''.join(f'<td id="d{i}" data-date="{start+timedelta(days=i)}" data-level="{1 if i==10 else 0}"></td><tool-tip for="d{i}">{"3 contributions" if i==10 else "No contributions"} on a day.</tool-tip>' for i in range(365))
    def test_counts_and_dates(self):
        days=m.parse_calendar(self.markup(),date(2026,9,26))
        self.assertEqual(sum(d['count'] for d in days),3)
        self.assertEqual(days[-1]['date'],'2026-09-26')
    def test_changed_markup_fails(self):
        with self.assertRaises(ValueError): m.parse_calendar(self.markup().replace('No contributions','Unknown data'),date(2026,9,26))
    def test_duplicate_or_partial_data_fails(self):
        with self.assertRaises(ValueError): m.parse_calendar(self.markup()+'<td id="d0" data-date="2025-09-27" data-level="0"></td>',date(2026,9,26))
        with self.assertRaises(ValueError): m.parse_calendar('',date(2026,9,26))
    def test_shipped_snapshot_draws_every_day_on_both_layouts(self):
        data=json.loads((ROOT/'data/activity.json').read_text())
        for mobile in [False,True]:
            root=ET.fromstring(m.render(data,mobile)); ns={'s':'http://www.w3.org/2000/svg'}
            cells=root.findall('.//s:rect[s:title]',ns)
            self.assertEqual(len(cells),len(data['days']))
            for cell in cells:
                self.assertLess(float(cell.attrib['x'])+float(cell.attrib['width']),float(root.attrib['width']))
                self.assertLess(float(cell.attrib['y'])+float(cell.attrib['height']),float(root.attrib['height']))
if __name__=='__main__':unittest.main()
