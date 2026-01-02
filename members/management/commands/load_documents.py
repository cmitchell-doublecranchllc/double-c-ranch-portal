"""
Management command to load initial documents
"""
from django.core.management.base import BaseCommand
from members.models import Document


class Command(BaseCommand):
    help = 'Load initial required documents'

    def handle(self, *args, **options):
        # Liability Waiver
        liability_waiver_content = """
WAIVER AND RELEASE OF LIABILITY, ASSUMPTION OF RISK AND INDEMNITY AGREEMENT

For and in consideration of Double C Ranch LLC allowing me, the undersigned, to participate as a riding student or worker at Double C Ranch LLC, located at 2626 Yule Farm, Charlottesville, VA 22901, and to engage in equine-related activities including but not limited to riding, handling, grooming, training, exercising, feeding, or working around horses (collectively referred to as "Equine Activities"), I, for myself, and on behalf of my heirs, next of kin, legal and personal representatives, executors, administrators, successors, and assigns, hereby agree to and make the following contractual representations pursuant to this Agreement (the "Agreement"):

A. RULES AND REGULATIONS:
I hereby agree that I have read, understand, and agree to be bound by all applicable Double C Ranch LLC rules, policies, and safety measures as amended from time to time.

B. ACKNOWLEDGMENT OF RISK:
I knowingly, willingly, and voluntarily acknowledge the inherent risks associated with equine activities and understand that working with, handling, and riding horses is inherently dangerous, and that participation in any equine activity at Double C Ranch LLC involves risks and dangers including, without limitation:

(i) the propensity of an equine to behave in dangerous ways which may result in injury; (ii) the inability to predict an equine's reaction to sound, movements, objects, persons, or animals; (iii) hazards of surface or subsurface conditions; (iv) the potential for serious bodily injury (including broken bones, head or neck injuries), sickness and disease (including communicable diseases), trauma, pain & suffering, permanent disability, paralysis, and death; (v) loss of or damage to personal property (including my mount, tack, and equipment) arising out of the unpredictable behavior of horses; (vi) exposure to extreme conditions and circumstances; (vii) accidents involving other participants, staff, volunteers, or spectators; contact or collision with other participants, horses, natural or manmade objects; adverse weather conditions; (viii) facilities issues and premises conditions; failure of protective equipment (including helmets); (ix) inadequate safety measures; participants of varying skill levels; (x) situations beyond the immediate control of Double C Ranch LLC and its management; (xi) other undefined, not readily foreseeable, and presently unknown risks and dangers ("Risks").

CAUTION: HORSEBACK RIDING AND EQUINE ACTIVITIES CAN BE DANGEROUS. PARTICIPATE AT YOUR OWN RISK.

Under VA Code Ann. Sec 3.2-6200-6203, an equine activity sponsor or equine professional is not liable for any injury to, or the death of, a participant in equine activities resulting from the inherent risks of equine activities.

C. ASSUMPTION OF RISK:
I understand that the aforementioned Risks may be caused in whole or in part or result directly or indirectly from my own actions or inactions, the actions or inactions of others at Double C Ranch LLC, or the negligent acts or omissions of the Released Parties defined below, and I hereby voluntarily and knowingly assume all such Risks and responsibility for any damages, liabilities, losses, or expenses that I incur as a result of my participation in equine activities at Double C Ranch LLC. I also agree to be responsible for any injury or damage caused by me, my horse, or my actions at Double C Ranch LLC.

D. WAIVER AND RELEASE OF LIABILITY, HOLD HARMLESS, AND INDEMNITY:
In conjunction with my participation in equine activities at Double C Ranch LLC, I hereby release, waive, and covenant not to sue, and further agree to indemnify, defend, and hold harmless the following parties: Double C Ranch LLC, its owners, employees, agents, contractors, volunteers, other participants, and visitors (Individually and Collectively, the "Released Parties"), with respect to any liability, claim(s), demand(s), cause(s) of action, damage(s), loss, or expense (including court costs and reasonable attorney fees) of any kind or nature ("Liability") which may arise out of, result from, or relate in any way to my participation in equine activities at Double C Ranch LLC, including claims for Liability caused in whole or in part by the negligent acts or omissions of the Released Parties.

E. COMPLETE AGREEMENT AND SEVERABILITY CLAUSE:
This Agreement represents the complete understanding between the parties regarding these issues and no oral representations, statements, or inducements have been made apart from this Agreement. If any provision of this Agreement is held to be unlawful, void, or for any reason unenforceable, then that provision shall be deemed severable from this Agreement and shall not affect the validity and enforceability of any remaining provisions.

I HAVE CAREFULLY READ THIS DOCUMENT IN ITS ENTIRETY, UNDERSTAND ALL OF ITS TERMS AND CONDITIONS, AND KNOW IT CONTAINS AN ASSUMPTION OF RISK, RELEASE AND WAIVER FROM LIABILITY, AS WELL AS A HOLD HARMLESS AND INDEMNIFICATION OBLIGATIONS. By signing below, I confirm that I have read, understand, and agree to be bound by all applicable Double C Ranch LLC policies, as well as all terms and provisions of this Agreement. If, despite this Agreement, I, or anyone on my behalf, makes a claim for Liability against any of the Released Parties, I will indemnify, defend, and hold harmless each of the Released Parties from any such Liabilities as the result of such claim.

The parties agree that this agreement may be electronically signed. The parties agree that the electronic signatures appearing on this agreement are the same as handwritten signatures for the purposes of validity, enforceability, and admissibility.

Address: 2626 Yule Farm, Charlottesville, VA 22901
"""

        # Riding Lesson Agreement
        lesson_agreement_content = """
Double C Ranch LLC Riding Lesson Agreement

Thank you for choosing Double C Ranch LLC to help you learn how to ride horses. We are excited to work with you! Please take a moment to provide your information and complete our rider release form and training agreement.

1. The Services
• Riding Lessons: Clients receive one riding lesson per week (45-min private or 60-min group lesson).
• Unmounted Horsemanship Classes: weekly (Sunday, 12 PM - 1 PM).
• Equipment Provided: Lesson horse, saddle, bridle, and all necessary riding gear.
• Lesson Grouping: Riders will be grouped based on ability as soon as they are ready.
• Pony Club Membership: All riders must sign up for Pony Club membership, as lessons are structured around Pony Club disciplines and certifications. The Pony Club membership is $155 per year and the Regional membership for Pony Club is $50 per year. Please do not hesitate to ask any questions you might have in regards to Pony Club memberships.

2. Client Requirements
• Clients must arrive on time for their lessons.
• Proper riding attire is required: boots with heels, breeches, or jeans.
• Riders must maintain a coachable and positive attitude.

3. Scheduling & Lesson Policies
• Clients will receive a dedicated lesson time each week, which will include an appropriate school horse and group of riders with similar abilities.
• Make-up Policy: One make-up lesson per month is allowed. One unused lesson may roll over to the next month, but it must be used within the following month or it will expire.
• Weather Cancellations: If a lesson is canceled due to weather, a rescheduled lesson will be offered.
• Long-term scheduling changes: Clients must request changes via call or text at (434) 996-1245.
• Rescheduling Policy: Lessons must be rescheduled at least 24 hours in advance of the scheduled time.

4. Compensation & Payment
• Clients must create an account at https://app.acuityscheduling.com/catalog.php?owner=36970923&action=addCart&clear=1&id=2073271
• Monthly payments are due on the 1st of each month based on the selected program.

5. Cancellation Policy
This agreement may be canceled by either party with at least 30 days' notice before the termination date.
To cancel payments, text or leave a voicemail at (434) 996-1245

6. No Guarantee
Double C Ranch LLC does not guarantee specific performance results. The success of the program depends on the effort and dedication of the rider.

7. Communications & Text Message Consent (Opt-In)
By signing below, I consent to receive text messages from Double C Ranch LLC regarding:
• Lesson reminders, scheduling updates, and cancellations
• Important barn announcements and events
• Pony Club updates and opportunities

I understand that:
• Standard message and data rates may apply.
• I may opt out at any time by texting STOP.
• My number will only be used for communication related to Double C Ranch LLC activities and will not be shared.

8. Release of Liability
I acknowledge the risks and potential for risks of horseback riding and activities in and around a facility where horses are kept and farm machinery operated. However, I feel that the possible benefits to me/my son/my daughter/my ward are greater than the risk assumed. Intending legally to bind myself, my heirs, and assigns, executors or administrators, I hereby waive and release forever all claims for loss or damages of any kind against Double C Ranch LLC for any and all injuries and losses that I/my son/my daughter/my ward may sustain while participating. This release includes without limitation the risk of negligent instruction and supervision. I engage in activities at Double C Ranch LLC, 2626 Yule Farm, Charlottesville, VA 22901 voluntarily with knowledge of the risks and I assume all risks of injury, death, and property damage that may result. I agree to bear any loss myself. I acknowledge that Double C Ranch LLC are materially relying on this waiver and assumption of risk in allowing me/my son/my daughter/my ward to participate in activities at Double C Ranch LLC, 2626 Yule Farm, Charlottesville, VA 22901 By their signatures below, the parties hereby understand and agree to all terms and conditions of this Agreement.

Company Representative: Christine Mitchell
Company: Double C Ranch LLC
"""

        # Create or update documents
        doc1, created = Document.objects.get_or_create(
            code='LIABILITY_WAIVER',
            defaults={
                'name': 'Waiver and Release of Liability',
                'version': 1,
                'content': liability_waiver_content,
                'is_active': True,
                'is_required': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Liability Waiver document'))
        else:
            self.stdout.write(self.style.WARNING('Liability Waiver document already exists'))

        doc2, created = Document.objects.get_or_create(
            code='LESSON_AGREEMENT',
            defaults={
                'name': 'Riding Lesson Agreement',
                'version': 1,
                'content': lesson_agreement_content,
                'is_active': True,
                'is_required': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Lesson Agreement document'))
        else:
            self.stdout.write(self.style.WARNING('Lesson Agreement document already exists'))

        self.stdout.write(self.style.SUCCESS('Documents loaded successfully!'))
