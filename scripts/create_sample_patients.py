import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import django
from datetime import date, datetime
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imhotep_smart_clinic.settings')
django.setup()

from django.utils import timezone
from accounts.models import User
from doctor.models import DoctorProfile, Clinic, Patients, MedicalRecord

def main():
    doctor_user = User.objects.get(username='imani')
    doctor_profile = DoctorProfile.get_or_create_for_user(doctor_user)
    clinic = doctor_profile.clinic

    print(f"Assigning patients to Doctor: {doctor_profile} (User: {doctor_user.username}) at Clinic: {clinic}")

    patients_data = [
        {
            "name": "Amina Hassan",
            "gender": "Female",
            "phone_number": "+254711234567",
            "date_of_birth": date(1991, 3, 15),
            "username": "amina_hassan",
            "email": "amina.hassan@example.com",
            "records": [
                {
                    "date": timezone.make_aware(datetime(2026, 8, 10, 10, 30)),
                    "details": "Patient presents with persistent morning occipital headaches and mild lightheadedness over the past 3 weeks. Vitals: BP 148/94 mmHg, Pulse 76 bpm, BMI 27.2. Systemic examination unremarkable. Fundoscopy shows no papilledema. Diagnosis: Stage 1 Essential Hypertension with tension headache.",
                    "remarks": "Follow low-sodium diet (<2g/day), engage in 30 mins moderate aerobic exercise 4x weekly. Monitor BP at home twice daily.",
                    "prescription": "1. Amlodipine 5mg PO OD (morning)\n2. Paracetamol 1000mg PO PRN for headache\n3. Lifestyle and dietary modification plan",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 9, 18, 14, 15)),
                    "details": "Follow-up visit for hypertension review. Home BP log shows average 132/84 mmHg. Headache frequency decreased significantly from daily to once weekly. Tolerating Amlodipine well without pedal edema. Repeat BP today: 130/82 mmHg.",
                    "remarks": "Good blood pressure control. Continue current medications and healthy dietary habits.",
                    "prescription": "1. Amlodipine 5mg PO OD (continue 60 days)\n2. Sumatriptan 50mg PO PRN for acute migraine attack",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 11, 2, 9, 45)),
                    "details": "Routine 2-month hypertensive follow-up. Patient is asymptomatic. BP in clinic: 122/78 mmHg, HR 72 bpm. Fasting lipid profile and renal function tests within normal limits (Creatinine 72 umol/L, eGFR >90).",
                    "remarks": "Excellent response to therapy. Next comprehensive follow-up scheduled in 3 months.",
                    "prescription": "1. Amlodipine 5mg PO OD (90-day refill)\n2. Routine health maintenance",
                    "is_shareable": True
                }
            ]
        },
        {
            "name": "David Ochieng",
            "gender": "Male",
            "phone_number": "+254722345678",
            "date_of_birth": date(1984, 11, 20),
            "username": "david_ochieng",
            "email": "david.ochieng@example.com",
            "records": [
                {
                    "date": timezone.make_aware(datetime(2026, 7, 15, 11, 0)),
                    "details": "Patient presents for annual physical examination. Reports mild fatigue and polyuria. Labs: Fasting Blood Sugar 9.1 mmol/L, HbA1c 8.4%, Total Cholesterol 5.8 mmol/L, LDL 3.7 mmol/L. BP 136/86 mmHg. Diagnosis: Newly diagnosed Type 2 Diabetes Mellitus with Mixed Dyslipidemia.",
                    "remarks": "Referred to clinic nutritionist for diabetic meal planning. Recommended 150 minutes of weekly aerobic exercise. Advised daily foot inspection.",
                    "prescription": "1. Metformin HCl 500mg PO BD with meals\n2. Atorvastatin 20mg PO OD at night\n3. Blood glucose monitoring kit (log FBS and 2hr post-prandial)",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 9, 5, 15, 30)),
                    "details": "Diabetic follow-up visit. Patient adjusted well to dietary modifications. Glucose log indicates fasting readings averaging 7.0 mmol/L. Mild gastrointestinal discomfort initially with Metformin, now resolved. BP 128/80 mmHg.",
                    "remarks": "Positive lifestyle adaptation. Titrating Metformin dose to achieve target glycemic control (HbA1c < 7.0%).",
                    "prescription": "1. Metformin HCl 850mg PO BD with meals\n2. Atorvastatin 20mg PO OD at night",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 10, 28, 10, 15)),
                    "details": "3-month diabetes follow-up. Repeat HbA1c improved to 7.1%. Fasting glucose 6.4 mmol/L. Urine microalbumin negative. Comprehensive bilateral lower extremity foot exam: sensation intact to 10g monofilament, pulses palpable bilaterally.",
                    "remarks": "Impressive HbA1c reduction. Continue current medication regimen and quarterly monitoring.",
                    "prescription": "1. Metformin HCl 850mg PO BD (90-day refill)\n2. Atorvastatin 20mg PO OD at night (90-day refill)\n3. Annual dilated retinal eye exam referral",
                    "is_shareable": True
                }
            ]
        },
        {
            "name": "Sarah Wanjiku",
            "gender": "Female",
            "phone_number": "+254733456789",
            "date_of_birth": date(2001, 7, 8),
            "username": "sarah_wanjiku",
            "email": "sarah.wanjiku@example.com",
            "records": [
                {
                    "date": timezone.make_aware(datetime(2026, 6, 20, 16, 0)),
                    "details": "Patient presents with acute shortness of breath, bilateral expiratory wheezing, and nocturnal cough triggered by cold weather and dust exposure. O2 saturation 95% on room air, RR 22/min. Peak Expiratory Flow (PEF) 310 L/min (62% of predicted). Diagnosis: Acute moderate bronchial asthma exacerbation.",
                    "remarks": "Administered nebulized Salbutamol in clinic with prompt relief. Provided written asthma action plan. Avoid known allergen triggers.",
                    "prescription": "1. Salbutamol Inhaler 100mcg: 2 puffs Q4-6H PRN wheeze\n2. Fluticasone/Salmeterol 250/50mcg Accuhaler: 1 inhalation BD\n3. Prednisolone 30mg PO OD for 5 days",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 8, 14, 11, 45)),
                    "details": "Asthma control review. Patient completed steroid taper with full symptom resolution. Reports zero nighttime awakenings over the last 4 weeks. Daytime rescue inhaler used only once prior to vigorous exercise. Repeat PEF 440 L/min (88% predicted).",
                    "remarks": "Asthma is well controlled. Continue daily maintenance ICS/LABA therapy.",
                    "prescription": "1. Fluticasone/Salmeterol 250/50mcg Accuhaler: 1 inhalation BD (refill)\n2. Salbutamol Inhaler 100mcg: 2 puffs 15 mins prior to exercise PRN",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 10, 12, 14, 0)),
                    "details": "Routine asthma check-up and management of seasonal allergic rhinitis. Clear breath sounds throughout lung fields. Nasal mucosal edema noted on rhinoscopy. No respiratory distress.",
                    "remarks": "Continue maintenance inhaler. Use nasal spray and antihistamine during high pollen counts.",
                    "prescription": "1. Fluticasone/Salmeterol 250/50mcg: 1 inhalation BD\n2. Fluticasone Furoate nasal spray 27.5mcg: 2 sprays per nostril OD\n3. Cetirizine 10mg PO OD PRN allergies",
                    "is_shareable": True
                }
            ]
        },
        {
            "name": "Peter Kiprop",
            "gender": "Male",
            "phone_number": "+254744567890",
            "date_of_birth": date(1972, 4, 12),
            "username": "peter_kiprop",
            "email": "peter.kiprop@example.com",
            "records": [
                {
                    "date": timezone.make_aware(datetime(2026, 7, 2, 9, 15)),
                    "details": "Patient presents with progressive right knee pain for 6 months, worse after walking and stair climbing. Morning stiffness lasting 15 minutes. Physical exam: Mild right knee effusion, joint line tenderness, crepitus on flexion. X-ray confirms Grade II Osteoarthritis (medial compartment joint space narrowing).",
                    "remarks": "Referred to physical therapy for quadriceps strengthening and low-impact conditioning. Apply ice packs 15 mins after activity.",
                    "prescription": "1. Celecoxib 200mg PO OD with food (for 14 days during flare)\n2. Omeprazole 20mg PO OD before breakfast (gastric protection)\n3. Glucosamine/Chondroitin 1500/1200mg PO OD",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 8, 25, 12, 30)),
                    "details": "Post-physiotherapy evaluation. Patient attended 6 PT sessions. Reports 50% improvement in right knee mobility and functional endurance. Joint effusion resolved. Mild occasional epigastric burning noted if taking medication on empty stomach.",
                    "remarks": "Reinforced taking NSAIDs strictly after meals. Maintain daily home physical therapy regimen.",
                    "prescription": "1. Paracetamol 1000mg PO TDS PRN for mild pain\n2. Celecoxib 200mg PO OD PRN only for severe joint flares\n3. Omeprazole 20mg PO OD (continue 30 days)",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 10, 30, 16, 20)),
                    "details": "Follow-up visit. Knee symptoms stably managed with low-impact cycling and home exercises. Pain score 2/10. GERD symptoms resolved under Omeprazole. Full range of motion preserved in right knee.",
                    "remarks": "Excellent functional status. Recommended continued weight management and joint-sparing exercises.",
                    "prescription": "1. Paracetamol 500mg-1000mg PRN\n2. Topical Diclofenac 1% gel: apply to right knee TDS PRN\n3. Routine follow-up in 6 months or SOS",
                    "is_shareable": True
                }
            ]
        },
        {
            "name": "Fatuma Mohamed",
            "gender": "Female",
            "phone_number": "+254755678901",
            "date_of_birth": date(1996, 9, 24),
            "username": "fatuma_mohamed",
            "email": "fatuma.mohamed@example.com",
            "records": [
                {
                    "date": timezone.make_aware(datetime(2026, 8, 1, 10, 0)),
                    "details": "Patient presents with persistent generalized fatigue, cold intolerance, dizziness on standing, and brittle nails over 2 months. Menorrhagia noted. Exam: Pallor of conjunctiva and palmar creases. Vitals: BP 110/70 mmHg, HR 88 bpm. Lab results: Hemoglobin 8.8 g/dL (Low), MCV 68 fL (Microcytic), Ferritin 7 ng/mL (Severe iron deficiency). Diagnosis: Moderate Microcytic Hypochromic Anemia secondary to iron deficiency.",
                    "remarks": "Dietary education on iron-rich foods (red meat, leafy greens, legumes) paired with Vitamin C. Avoid tea/coffee with meals.",
                    "prescription": "1. Ferrous Fumarate 210mg PO BD (with orange juice or water)\n2. Ascorbic Acid (Vitamin C) 500mg PO BD\n3. Tranexamic Acid 500mg PO TDS during heavy menstrual flow days",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 9, 10, 11, 15)),
                    "details": "Iron therapy tolerance and progress check. Patient reports substantial reduction in fatigue and improved daily energy. No nausea or severe constipation; stools dark as expected. Menstrual flow significantly reduced with Tranexamic acid.",
                    "remarks": "Good clinical tolerance. Advised adequate dietary fiber and hydration. Repeat full hemogram scheduled in 8 weeks.",
                    "prescription": "1. Ferrous Fumarate 210mg PO BD (continue 60 days)\n2. Vitamin C 500mg PO BD",
                    "is_shareable": True
                },
                {
                    "date": timezone.make_aware(datetime(2026, 11, 5, 15, 0)),
                    "details": "Follow-up hematological evaluation. Patient feels energetic, dizziness resolved. Conjunctiva pink, capillary refill < 2 sec. Repeat CBC: Hemoglobin 12.1 g/dL (normalized from 8.8), Ferritin 32 ng/mL (improving). Red cell indices normalized.",
                    "remarks": "Anemia successfully corrected. Continue oral iron for an additional 8 weeks to fully saturate bone marrow iron reserves.",
                    "prescription": "1. Ferrous Fumarate 210mg PO OD (maintenance dose for 60 days)\n2. Vitamin C 500mg PO OD\n3. Routine check in 3 months",
                    "is_shareable": True
                }
            ]
        }
    ]

    created_patients = []
    created_records_count = 0

    for p_data in patients_data:
        patient_user, _ = User.objects.get_or_create(
            username=p_data["username"],
            defaults={
                "email": p_data["email"],
                "first_name": p_data["name"].split()[0],
                "last_name": " ".join(p_data["name"].split()[1:]) if " " in p_data["name"] else "",
                "user_type": "patient",
                "email_verify": True
            }
        )

        patient, p_created = Patients.objects.get_or_create(
            name=p_data["name"],
            doctor=doctor_profile,
            defaults={
                "user": patient_user,
                "clinic": clinic,
                "phone_number": p_data["phone_number"],
                "gender": p_data["gender"],
                "date_of_birth": p_data["date_of_birth"],
            }
        )
        if not p_created:
            patient.user = patient_user
            patient.clinic = clinic
            patient.phone_number = p_data["phone_number"]
            patient.gender = p_data["gender"]
            patient.date_of_birth = p_data["date_of_birth"]
            patient.save()

        created_patients.append(patient)
        print(f"Patient {'created' if p_created else 'updated'}: {patient.name} (ID: {patient.id})")

        for r_data in p_data["records"]:
            record, r_created = MedicalRecord.objects.get_or_create(
                doctor=doctor_profile,
                patient=patient,
                date=r_data["date"],
                defaults={
                    "clinic": clinic,
                    "details": r_data["details"],
                    "remarks": r_data["remarks"],
                    "prescription": r_data["prescription"],
                    "is_shareable": r_data.get("is_shareable", False),
                }
            )
            if not r_created:
                record.clinic = clinic
                record.details = r_data["details"]
                record.remarks = r_data["remarks"]
                record.prescription = r_data["prescription"]
                record.is_shareable = r_data.get("is_shareable", False)
                record.save()
            created_records_count += 1
            print(f"  - Record: {record.date.strftime('%Y-%m-%d')} for {patient.name}")

    print(f"\nDone! Successfully processed {len(created_patients)} patients and {created_records_count} medical records for doctor '{doctor_user.username}'.")

if __name__ == '__main__':
    main()
