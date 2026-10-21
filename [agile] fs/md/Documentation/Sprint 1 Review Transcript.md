# Sprint 1 Review Transcript


# Sprint 1 Review – Refined Meeting Script


Education Account (EA) · Sprint 1 review & demo · 16 Oct 2026 (per audio file metadata) · Duration 30:48. Source: AI-generated transcript (.docx) cross-checked line by line against the audio (.m4a). Timestamps follow the audio.

## How to read this script

- Wording is cleaned up (ASR errors fixed, filler removed) but the meaning of each turn is kept as spoken.
- Speaker labels are by role. The .docx diarization is unreliable (e.g. Hayden's intro is tagged Speaker 2), so roles were re-assigned from context: Reviewer (Speaker 1, asks questions and gives feedback), Dory (Speaker 2, overview), Hayden (Speaker 3, demo), Team member (Speaker 4, answers on business logic).
- [unclear] = could not be confirmed from the audio. [inferred] = reconstructed from context. All of these are collected in the checklist at the end.
- MOE = Ministry of Education, EA = Education Account, HQ = MOE Headquarters.

## 1. Opening and overview (00:00 – 01:25)


[00:00] Reviewer: Hi Dory.

[00:01] Dory: Okay. Today Team 5 and 8 [unclear] will introduce Sprint 1. I'm Dory [name unclear] and I will cover the overview; after that we will move to the demo with Hayden. First, the user types. We have divided the system into two portals: the Admin Portal and the e-Service Portal. The Admin Portal is for MOE HQ as well as the school users. The e-Service Portal is for parents [inferred].

[00:39] Dory: Authentication for the Admin Portal is by username and password for both user groups. Their primary responsibilities differ. MOE HQ can manage school, level, class and student. School users can configure the classes the school offers, register students and handle enrolment.

[01:04] Dory: Parents can view their children's Education Account details and check fees. They can update their profile and make payments. For the flow, Hayden will give you the demo.

## 2. Demo – MOE HQ view (01:25 – 12:20)


[01:25] Hayden: Hello. I'm Hayden, and I'm responsible for the demo this sprint. Please wait a moment while I share my screen. Can you see the screen now? We haven't completed the homepage yet, but this is the login page for MOE and school users.

[02:03] Hayden: This is the login page for MOE and school users, and here we have the mock data for MOE. This is the account of MOE headquarters, and this is the MOE homepage. There are many functions, but this sprint we focus on Functions 1, 3, 8 and 9 [function numbering to be confirmed].

### 2.1 Education Account sync (Function 1)


[02:42] Hayden: Under Education Account, as described in Function 1, the system automatically syncs the data of Singaporean students aged 7 to 16. We also added a new feature: manual sync. When I press this button, the system pulls the data from the government immediately. Let me run a test. (Sync completes.) Confirmed.

[03:21] Reviewer: Is there any difference between your first manual sync and the subsequent automatic syncs?

[03:27] Hayden: It is essentially the same. The manual sync is for when MOE needs the newest data. Otherwise the system updates automatically every night at 12 [AM/PM unclear – transcripts say "12 PM" but "every night" suggests midnight].

[03:50] Reviewer: Do you do a full sync or an incremental sync?

[03:54] Hayden: It's a full sync [unclear].

[03:57] Reviewer: So you will override the existing data even if there are no delta changes?

[04:08] Team member: [inferred from the .docx, audio very faint] The initial sync (bootstrap) takes the information of citizens aged 7 to 16; if they are eligible, the system creates an Education Account for them. For the following days we run incremental sync. A daily job runs at the start of the day (around 12 midnight [unclear]) to sync citizens who have just turned 7. If the government database updates some information that the daily job was not able to extract, MOE can trigger the manual sync again, running the bootstrap sync over for those aged between 7 and 16.

### 2.2 School user management


[05:32] Hayden: Next, the school user function. This is where MOE HQ creates school users. When I press this button, it creates a school user based on three main criteria [unclear], and saves it as a single school user. When creating school users there are two options: add a single user, or bulk create by uploading a CSV file with the list of school users. Here is the list of school users I have just created.

[06:38] Reviewer: Why do you have a password here?

[06:41] Hayden: For sign-in purposes for the school user.

[06:48] Reviewer: School users are supposed to sign in with their MOE account, their AD account. You shouldn't store passwords in your system; that is very sensitive.

[07:01] Hayden: I know. This part comes from the MOE side, so MOE will provide the credentials to the school users.

[07:10] Reviewer: No. It is integrated with their AD account. There is no separate username and password.

[07:20] Hayden: Okay, we will note it and provide it in the next demo. For now this sprint is based on username and password for school users. They can export the file and send it to the school user, based on our current flow.

### 2.3 Academic levels and academic years


[07:46] Hayden: The next step is the academic levels. This is mock data for the education stage, which MOE creates when configuring a school. Here we are only creating mock data; we will describe it in detail later. Besides academic levels, we also provide a function to create academic years, to distinguish classes between years. For example, Class 10 in 2026 is clearly different from Class 10 in 2027.

[08:45] Hayden: So the main functions we built this week are creating schools and school users.

### 2.4 School creation


[09:00] Hayden: As I demonstrated, when I create a school it has these details: school code, school name and school type. You can also assign the school users created earlier to the school. The school type has five values: Government, Government-aided, Autonomous, Independent and Specialised.

[09:48] Reviewer: Here is a list of users. Do you have a better way to manage school users? This is not very effective; there are hundreds of users in a school.

[10:03] Hayden: Right now we just list them like this.

[10:07] Reviewer: I cannot accept this solution. Go back and think of a new solution for this.

[10:12] Hayden: Okay, we will take it as a note and fix it soon. Here you can assign the school user and choose the academic level.

[10:36] Reviewer: What do you display under school users? Do you display all the users in the system for selection?

[10:50] Hayden: It is based on which school users we assigned to that school.

[10:57] Reviewer: You are assigning the school user to the school on this page, right?

[11:01] Hayden: Yes.

[11:03] Reviewer: Then how do you scope it down? Can one school user belong to multiple schools?

[11:28] Team member: For now we decided that a school user belongs to one school only, but one school can have many school users.

[11:38] Reviewer: Okay.

[11:42] Hayden: Let me continue. When creating the school, we get the list of schools that MOE manages. Here I created "UAT1"; it has 0 active classes and 0 active students. This is the overview of the MOE headquarters view. Now I will switch to the school user view. Let me check a little bit; can you wait while I create a new school for a better demo?

[12:46] Reviewer: Next time, please prepare your demo data in advance, okay?

[12:50] Hayden: Yes, okay.

## 3. Demo – School user view (13:45 – 19:30)


[13:45] Hayden: This is the school user side. The school user first has to configure classes, and after that can put students into the classes. Their first duty is to create the class. Class details include the code, the name, and the school level offering configured earlier. I have just created a class. Now I will assign a student to this class. You have to create the student first and then assign the student to the class.

[14:50] Hayden: We need to set the date of birth and the student category. The student category is what we need to consider FAS and fee management on the parent side.

[15:13] Reviewer: Can you call it "citizenship" instead of "student category"?

[15:23] Team member: Not really. Some students are Singaporean, but some are international students and we don't define which country they belong to, so I don't think "citizenship" is appropriate.

[15:46] Reviewer: No, just use it. That's how we use it.

[15:52] Team member: Okay, we will take note and change the term [last sentence partly unclear].

[16:06] Hayden: We set the enrolment start date, then create the student. Here is the student; I created a student named Hu Fang Wan [mock name]. The current class is "not assigned", so now I assign the class I just created, based on Function 3. This is the class I created earlier, with the enrolment start date set to tomorrow.

[17:07] Hayden: So basically the school user assigns students into classes, and the school user maintains many classes and many students.

[17:30] Reviewer: What does the enrolment status "Enrolled" mean?

[17:38] Hayden: It means the student is attending this school. If the student transfers to another school, the status changes to "Transferred to another school", and if the student graduates, the status changes to "Closed".

[18:03] Reviewer: In the enrolment table there are "Enrolled from" and "Enrolled to". Where do you get the dates from?

[18:14] Hayden: It is based on the assumption that "Enrolled from" is the date the student starts studying at the school, and "Enrolled to" is the graduation date.

[18:32] Reviewer: How do you know their graduation date? Is it 23 December 2027?

[18:40] Hayden: That is just the expected date, but our system can accept it as a null value and the school user can add it later.

[18:57] Reviewer: I think you still need to find a way to indicate an accurate enrolment date. Don't just put in a date anyhow.

[19:07] Hayden: Okay, we will note that. Thank you. That is the school user view; now we move to the parent view.

## 4. Demo – Parent view / e-Service Portal (19:30 – 28:40)


### 4.1 Homepage and student cards


[19:35] Hayden: This is the e-Service Portal. The parent signs in with Singpass. Here I use some mock data and log in. When the parent logs in successfully, the first thing they see is their children's cards. Here you can see three cards, which means this parent has three children. Each card shows the child's information and EA balance.

[20:10] Reviewer: This is the parent view, right? Do you think a parent doesn't know their child's date of birth, citizenship, race and address?

[20:21] Hayden: Our purpose is to show more than this on the card, such as the fees, the outstanding charges and the fees the parent has not paid. This is just the basic information; we will revise it later.

[20:44] Reviewer: So you will still show the basic information?

[20:48] Hayden: Yes. We will combine the fee information into this card later.

[20:54] Reviewer: You only have this much space. This is the homepage that parents see when they first log in, but a lot of space is used to display date of birth, gender, race and citizenship, which parents already know. No parent would not know their child's basic information. What I'm saying is you can reserve the space for better use.

[21:23] Team member: Okay. If you think this is not necessary, we will display other information that is necessary for the parent on the page, and move this information into the Student Profile section for details.

[21:48] Reviewer: Yeah.

### 4.2 Parent profile


[21:51] Hayden: Next is the parent profile. This is the parent's information integrated from Singpass: full name, NRIC, residential address and contact information. Here is the mailing address. This is basic information that the parent can adjust in the system, for example the phone number and the email address [remaining words unclear], and then save to update our system.

### 4.3 Transaction history


[22:40] Hayden: Now the transactions. Parents can see their transaction history here.

[22:59] Reviewer: Can you go back to the transaction page? In what circumstances would the status be "not successful"?

[23:12] Hayden: Currently we only cover the happy case. For unsuccessful statuses, for example system or network failure, we will review them for QA testing and provide them to you later.

[23:29] Reviewer: Okay, but if a transaction failed, should we still display it to parents? Shouldn't we recover those transactions and display only the successful ones? Has the team thought about that?

[23:49] Hayden: We did discuss it. Our idea right now is to keep the status, and maybe we will change it or remove it for a better parent experience.

### 4.4 Fee and payment


[24:02] Hayden: Last part: fee and payment. The parent can see the fees for each of their children. They can see the child's EA balance, and also the outstanding fees. Here are the fees the parent still has to pay. For example, I will pay the stationery fee and the field trip fee. There are two payment methods: use the EA balance, or use the online gateway.

[24:42] Hayden: First I use the EA balance: authorise and pay. The receipt is shown, and when we go back, you can see the account balance has been deducted.

[25:08] Hayden: The second method is the online gateway. I authorise and pay; the gateway flow does not yet provide the "QA" [unclear – possibly QR] for the parent to pay, so it is only simple basic information for now, and we will provide it to you next week. Payment succeeds and the system issues the receipt. That is the flow when paying a fee for a child.

[25:46] Reviewer: So the flow is you choose a child first, and then you see the outstanding fees and education account balance for that particular child?

[25:51] Hayden: Yes.

[25:58] Reviewer: Okay. Can you display the child's name somewhere else, rather than only as a card, for example in the corner?

[26:03] Hayden: Right, we can do that later. We will note it.

[26:11] Reviewer: And your outstanding fees are not updated yet, right? After you pay a fee, the outstanding fees and the education account balance should be updated in real time.

[26:24] Hayden: They do update in real time.

[26:29] Reviewer: Okay, maybe I didn't see it.

[26:34] Hayden: For example, if I select all three fees the total is 840 [amount to confirm]. That is basically our parent flow, and we have also shown you the MOE and school user views earlier. That is our presentation for the demo.

[27:07] Reviewer: Is that all? Can you scroll down a bit?

[27:09] Hayden: Sorry, we also have the split payment situation. For example, the total fee is about 1,100 but the EA balance is only 1,000 [amounts to confirm]. When we go to payment, we combine both methods: it uses the current Education Account balance and adds the online gateway so the parent can finish paying the total.

[28:09] Reviewer: Can you allow me to choose how much to use from the education account? I may not want to use up the whole $1,000 at once.

[28:16] Hayden: Right now we haven't built that, but we can modify it for you later. Then we authorise and pay, same as the previous flow.

### 4.5 UI feedback on the Outstanding Fees page


[28:39] Reviewer: Can you go back to the outstanding fee page? I want the team to look into the UI. Maybe find another child with data.

[28:55] Hayden: Like this.

[28:57] Reviewer: The first column is very narrow and the second column is very wide, although the description is not that long. If you scroll down further, the education account balance is displayed again; why do you display it here again? Also, the date format here is year-month-day, while some of your other pages use a different format. Please keep it consistent, including the due date format.

[29:39] Hayden: Okay, I'll fix it.

## 5. Closing feedback (29:42 – 30:48)


[29:42] Hayden: That is the overall flow of our system. Do you have any feedback right now?

[29:53] Reviewer: You may still want to drill down into some of the details. At a high level it looks okay, but there are certain scenarios [transcripts say "happy scenarios"; likely "unhappy scenarios / edge cases"] that the team hasn't really considered yet. From a user experience perspective, also think about what is really useful from a parent's perspective. The team can take this back and propose a better solution in next week's demo.

[30:26] Hayden: Yes, we will note it and enhance it later. Thank you for today. See you next week.

[30:36] Reviewer: Thanks, team. Bye.

[30:39] Team member / Hayden: Thank you. Bye.

## Quick index for the MoM: feedback and follow-ups

- Auth for school users: do not store passwords; school users must sign in with their MOE AD account (integration). Team to provide in next demo. Interim: username/password with export file.
- School user selection: current list is not workable for hundreds of users per school; the Reviewer rejected it and asked for a new solution.
- School user scope: confirmed one school user belongs to one school; one school has many school users.
- Demo prep: prepare demo data in advance.
- Student category: Reviewer asked to rename it to "Citizenship"; the team pushed back (international students), Reviewer insisted; team to take note and change the term.
- Enrolment dates: "Enrolled from / to" must be accurate; do not default an arbitrary graduation date. The team allows null and the school user can fill it in later.
- Parent homepage cards: remove DOB, gender, race, citizenship and address from the cards; use the space for fee and balance; move basic details to Student Profile.
- Transaction status: unsuccessful statuses to be reviewed for QA; open question whether to show failed transactions to parents.
- Online gateway: flow still basic; more detail to be provided next week.
- Fee page: show the child's name more clearly (e.g. in the corner); fix column widths; avoid showing the EA balance twice; use one consistent date format.
- Split payment: parent should be able to choose how much of the EA balance to use; team to modify later.
- Overall: team to detail the scenarios not yet covered, think about what is useful for parents, and propose a better solution in next week's demo.

## Items to verify before finalising the MoM

- Names and roles: Dory (overview), Hayden (demo), the Reviewer, and "Team 5 and 8".
- Auto-sync time: transcripts say "12 PM"; context suggests midnight.
- The Team member's explanation at 04:08 – 05:27 (initial full/bootstrap sync, then incremental; daily job) is reconstructed from the .docx because the audio is very faint.
- "Three main criteria" when creating a school user (05:32).
- Function numbering ("Functions 1, 3, 8 and 9") and which function each demo step maps to.
- "QA" vs "QR" for the online gateway (25:12).
- "Happy scenarios" at 29:53, probably "unhappy scenarios".
- Amounts in the split payment demo (840; 1,100 vs 1,000).
- Parent profile editable fields at 22:23 and the term the Team member used at 15:52.