# Meeting Transcript - 23 Oct 2026


# Meeting Transcript - 23 Oct 2026


## Part 1 – School and school user setup (00:01–09:50)


Speaker 1 (00:01): Hey, so let me share my screen. Here is the dashboard page.

Speaker 2 (00:32): Oh, that's the dashboard.

Speaker 1 (00:34): Yeah, this is the dashboard. We haven't really designed the details yet; I'm just showing it to you. First, before going into detail, we need to set up some master data. We need to create a school in the system so that we can upload school users. The school users we upload will be automatically assigned by the system to the school that has been created. Let's say we have different schools here, and we are going to assign different school users to them.

Speaker 1 (01:33): By the way, you can create a new school by clicking this button and filling in the school code, which is unique, then the school name and the school type. We have different types: government, [unclear], autonomous, independent and specialised schools. And here are the academic levels. This is an optional field; a school can offer different levels, depending on the education system. Then I'll move on to school user management, where we have some school users already created. We have two options: manually input the information of one school user at a time, or upload a CSV file so that we can input many school users at the same time.

Speaker 1 (02:50): If you don't know what the CSV file should look like, the system can generate a template. You can download it and see how to input the information. The school user file should look like this. Wait a second, let me show it here.

Speaker 1 (03:32): This is the school user template. It has the school user's email, which they will use to log in to the system via Microsoft, then the first name, the last name and the school code. The school code is optional: in this demo, the school has already been created in the system, so the system will know which school the users belong to and will automatically assign them to it.

Speaker 1 (04:14): If the school code is left blank, the school user will not be assigned to any school. Now let me upload this file into the system. We have 5 school users that should be assigned to the school. Okay, so one [record failed – reason unclear]. So we can see the school user list; we have just imported the new users.

Speaker 2 (05:04): Okay, I have a question on this. Yeah.

Speaker 1 (05:09): Regarding school users: in our last session we agreed that the admin cannot create school users with passwords, because a password is sensitive information. So school users sign in with Microsoft using their own emails.

Speaker 2 (05:52): Yeah, that's right. It should be integrated with their AAD account.

Speaker 1 (06:10): Yes. And the second part is school configuration, where we have the school structure. We have different academic levels here; for now it only has Primary 1 to Primary 6, and we can add more academic levels that the school offers in this academic year.

Speaker 1 (07:17): [Unclear – something about a pop-up showing the reason when an academic level cannot be removed.] A school can offer three stages: primary, secondary and pre-university, each with different levels. Primary has 6 levels, secondary has [unclear] levels and pre-university has 2 levels. We have created one class already, and you can add more: a second class, a third class, whatever you like. You set the class code and the class name.

Speaker 1 (08:02): We can also add classes in bulk by importing a CSV file, like with school users. We also have a template: click "Get template", download it, then upload the CSV file once you have prepared it. The system will generate all the classes in bulk, and you can see the list of classes created here.

Speaker 1 (09:06): Next, we can create students [unclear].

Speaker 2 (09:11): Sorry, before you proceed, what else are we going to demo today other than classes and students?

Speaker 1 (09:17): We are going to demo the top-up management feature and SBFAS, as well as MOE FAS.

Speaker 2 (09:29): Oh, can we start with SBFAS? Does it include the application process as well?

Speaker 1 (09:38): Yes, the FAS function includes the application process.

Speaker 2 (09:45): I want to focus on the FAS, not so much on class and school management.

Speaker 1 (09:50): Okay. Can we hand over to [name unclear] to present the FAS demo?

## Part 2 – SBFAS scheme creation (10:01–14:36)


Speaker 3 (10:01): Sorry, can you hear me now?

Speaker 2 (10:04): Yes, [name unclear].

Speaker 3 (10:05): Okay, give me a minute to turn on my screen.

Speaker 3 (10:20): Okay, do you see the screen now? Yes. Okay, so let's start with SBFAS first. Here we have some UI problems, but the new scheme process still works well. Let's create a new one. Here is the list of the schemes we have created. The UI is quite confusing, but we'll fix it later.

Speaker 3 (10:45): For the scheme creation process we have four phases. The first is the scheme name, and there are two timelines. The first is the application timeline, which is when parents or school users submit applications. After that is the effective timeline, which is when the fee subsidy applies to the students; we cannot change any fee in this scheme anymore.

Speaker 3 (11:27): For example, applications open from today and close on 25 October, and the scheme is effective from 27 October to the end of the month. We also have the budget for the scheme. We haven't clarified Function 6 yet, which is about the budget, so we just put it here and we can refine it next week.

Speaker 3 (12:00): Here we also have a section for information about the scheme [unclear]. Next, we set up the eligibility. We have predefined criteria; the first one is nationality. Here you can select which nationalities can apply to the scheme. Then there is gross household income (GHI), where you can set a range, and per capita income (PCI), where you can also set a range. The current condition is that the applicant meets either the GHI or the PCI condition: if either one of the two is met, the application passes.

Speaker 3 (12:52): Next is the subsidy, where we add the fee components. This school has two levels, so for primary and secondary here we just add the fees available at the school.

Speaker 2 (13:19): For example, I just need to add three fee components here, and you can type the percentage you want, like this. Then you go to Review to see what you set up in the previous phases: here you have the name, the timelines, the eligibility and the subsidy matrix. You can save it as a draft and continue later if you want, or you can just publish. So the scheme has just been created by me.

Speaker 2 (13:48): We can continue to the parent phase, where parents can apply for FAS by themselves. We have built the FAS application for parents in the e-Service Portal. At this step the parent has to type in the data manually. We want to retrieve the information from MyInfo.

Speaker 2 (14:36): We considered it an AI feature, but we haven't implemented it yet, so maybe we'll complete it next week.

## Part 3 – SBFAS parent application and client feedback (14:47–19:22)


Speaker 3 (14:47): But that's not an AI feature. Information retrieval from MyInfo is not an AI feature. [Unclear] We'll fix it. Okay.

Speaker 1 (15:07): So basically you want the number of input fields to be minimal, with the system retrieving the details from MyInfo. [Partly unclear] Yeah, okay.

Speaker 3 (15:23): And what's the purpose of having gender, race and phone number on this page?

Speaker 2 (15:30): Yeah, those should be retrieved by the system, right?

Speaker 3 (15:33): No, I mean, how does it help with the FAS application? Why do you need to capture gender or even race?

Speaker 2 (15:43): [Unclear] We need this to check against government data whether this is the real parent of the student, so we need a verification step before checking the application.

Speaker 3 (16:02): But we are going to retrieve the data from the government database.

Speaker 2 (16:06): Yes, for the permanent information. Yeah.

Speaker 3 (16:12): So do you still need those fields?

Speaker 2 (16:16): I think we just need the NRIC, and we will retrieve all the information from the government database. Okay, so fine. Here we have to type in the student information.

Speaker 3 (16:33): I think this one you can also retrieve from the government database.

Speaker 2 (16:38): Okay, got it. Let me wait a second. The school name is [unclear]. Secondary 2 [unclear].

Speaker 1 (16:59): The school name is [unclear].

Speaker 2 (17:07): Okay, and you can add the family members here. We can demo the family details later. Right now we just need to add the application details and the child's details.

Speaker 3 (17:28): Where do you state the income information?

Speaker 2 (17:32): From the third party, as mentioned in the requirement. The parent income and the household income are retrieved from the third-party API.

Speaker 3 (17:43): Yeah, I think we also need a place for the parent to indicate whether they have additional income. If they have other income that is not reported to the government database, we need that kind of declaration.

Speaker 2 (17:58): Yes, and they also need to indicate how much additional income they have. So we must have a field where the parent provides the income themselves. Okay, got it.

Speaker 1 (18:15): But how do we know that the extra income information provided by the parent is accurate?

Speaker 2 (18:24): Based on our discussions, a supporting document can be required.

Speaker 1 (18:28): And how do we want it to be checked?

Speaker 3 (18:32): Based on their declaration, we basically have to trust them, and they have to provide a supporting document.

Speaker 2 (18:51): Yeah. Then there is the rest of the submission process [unclear], and of course we'll fix it later. As for MOE FAS, it's just like SBFAS, but we have some problems, and we might present it to you next week.

Speaker 3 (19:11): I cannot see the submitted FAS application. You mean you just submitted a FAS application just now, right? Yeah.

## Part 4 – Submitted application, MOE FAS and sprint readiness (19:22–22:34)


Speaker 2 (19:22): Yes, and here is the application I just submitted, shown right here. And it has the [unclear].

Speaker 3 (19:30): How do I view the details?

Speaker 2 (19:36): We have a button here for the details, [unclear].

Speaker 3 (19:41): Okay, you haven't finished development for this.

Speaker 2 (19:45): Yeah, we have some UI problems. [Unclear] Basically, the FAS applications from parents and their details are shown right here. We'll fix it for next sprint. Yeah? So far, that is the SBFAS flow, including where they submit the application. MOE FAS has quite some trouble, so we won't present it today; maybe next sprint.

Speaker 3 (20:20): Do you think you are able to finish everything by the next sprint?

Speaker 2 (20:23): Yes, yes, yes. For MOE FAS, I'm sure; it is about 80% done and we'll fix the rest later.

Speaker 1 (20:34): Are you asking whether we can finish all the requirements you provided initially in the next sprint? I think we'll just refine everything we have built so far.

Speaker 3 (20:45): I think you do need to refine everything you've built so far. But the FAS application process flow is only halfway done, you have a few more AI features to develop, and I haven't seen the simulation function and some of the other minor features. And you only have one sprint left.

Speaker 1 (21:07): I think we need time to refine the things we have been doing so far. As for minor requirements such as the simulation, I don't think it's possible for us to finish everything, but we will try. Don't worry, I'm not trying to overstate [partly unclear].

Speaker 3 (21:32): Was it properly communicated to the customer that you may not be able to finish everything?

Speaker 1 (21:50): I think it hasn't been. I shouldn't just say that I'll try my best; I should tell [unclear] so that we have something for [unclear].

Speaker 3 (22:10): Okay.

Speaker 2 (22:11): Yeah, thank you. So let's move to the top-up function. Okay. [Unclear – handing over to the next presenter.]

## Part 5 – Bulk top-up (22:40–27:21)


Speaker 4 (22:40): Okay, can you see the screen? I will start with the bulk campaign. A bulk campaign is where you give top-ups to many students at one time. So first I will create a campaign. Let me say, give every [student]... Sorry, I can't really hear you. Please say that again.

Speaker 3 (23:44): I'm saying the terminology is not "campaign". It's just "top-up".

Speaker 4 (23:49): Okay, then we will change the terminology from "campaign".

Speaker 3 (23:57): It's not a campaign, it's a top-up. Just call it bulk top-up.

Speaker 4 (24:02): Okay, I will change the terminology to top-up. Then I will create a top-up. First, let's say: give every secondary student 300. I enter the amount of 300; the description is optional. I have to set the criteria here: secondary is ages 12 to 15, so I enter 15 here, because it's less than or equal to 15 years old. We also have a balance threshold; let's say 100 to 500. Then we can preview the list of eligible accounts that will be topped up and see the total amount we will spend. Okay, let's confirm and run. You can see the top-up is running here, and it has run successfully. In the History you can see that it was successful with no failures, and the total distribution is 60 million. Here you can see this data, where we have the status, active or inactive. We can change it to inactive.

Speaker 3 (25:34): What do active and inactive mean?

Speaker 4 (25:35): Okay, I think active means you can run it again, and inactive means you cannot run. We also set the budget right here.

Speaker 3 (25:48): You mean I can just press the run button and it will run?

Speaker 4 (25:53): Yes, I mean, you can rerun it if it is active.

Speaker 3 (25:59): That's actually very risky. What if I accidentally press the button?

Speaker 4 (26:05): You will see a confirmation here, Cancel or Run. It will ask you to confirm before it runs.

Speaker 2 (26:17): Do you have a better way to do this? Can I configure a future date and time to run the top-up, instead of manually clicking run on an ad hoc basis?

Speaker 4 (26:33): You mean a schedule, so that it runs automatically? Yes, we will consider it. If it takes a lot of effort, we will discuss it and give you feedback in the MoM. I'll give you an answer in the MoM.

Speaker 3 (26:57): Okay, but I would rather have a timer, a schedule, instead of this kind of ad hoc run. That's usually not how we do it. Usually, once we have the budget each year, we set it up and wait until the proper time to run. We won't just configure it today and [run it right away].

Speaker 4 (27:21): Okay, we have to think about that, but we haven't implemented it yet, which is why we didn't bring it up here. So that's the bulk top-up.

## Part 6 – Individual top-up, failed records and closing (27:21–32:00)


Speaker 4 (27:21): Next I will show the individual top-up. As you can see in the History, if any account fails, we can top up by individual. So you can see this is the top-up for active accounts. For inactive accounts, we also show the information, but you cannot top up that account.

Speaker 4 (28:08): Okay, I will top up this one. I give a reason here. Let's say it failed in the bulk top-up, so we have to top up manually for this account. We can review and see the new balance after the top-up, along with the current balance, and then run. It's successful, so we can view the history; the status is success.

Speaker 3 (28:41): If the bulk top-up fails, you don't really expect us to create 20 individual top-ups, do you? Is that how you expect us to do it?

Speaker 4 (28:51): I'm just saying this is for special cases. I'm not limiting you to only failed bulk top-ups and then going to individual. As I said, this is one case. Okay?

Speaker 2 (29:06): We're going to use the bulk top-up. Let's say I run 3,000 students and 20 actually fail. How do you deal with the 20 failed records?

Speaker 4 (29:14): Oh, um. Maybe we would set up another top-up and see why it failed. But normally when we run a top-up, there are not many failures. If there are, we would need to find out why there are so many failures.

Speaker 2 (29:45): Okay, wait. There will be failed top-ups, that's for sure. You don't know the complexity of the production database; there will be a few. I think the question is still how you intend to deal with the failed top-ups. You cannot just expect us to set up another rule and run it again, because your system is not able to tell which ones actually failed. Your condition is purely based on the student profile.

Speaker 4 (30:12): The profile.

Speaker 2 (30:13): It's not really based on the past job result or anything.

Speaker 4 (30:20): Oh, we can show you a failure for this one. We don't have a failure here, but a failure comes with a reason.

Speaker 3 (30:29): Yeah, but the question is how do you deal with it? How do you deal with the failed records?

Speaker 4 (30:35): I think the team has thought about it, yes. But when there are failures, we normally see just one or two

Speaker 3 (30:47): Don't tell me "normally". You can't know how many failed records there will be in production. It could be the case that more than half of the records fail.

Speaker 4 (31:01): We will think about the scenario, and we might consider adding a retry function here to retry all the failed accounts.

Speaker 3 (31:15): Okay, think of a solution and update us next time.

Speaker 4 (31:19): Yeah, thank you. So that's all about the top-up. Do you have any other questions or feedback about the top-up?

Speaker 3 (31:28): No further questions. And I think time is up.

Speaker 5 (31:30): Okay, thank you for spending your time today. We will try to deliver our best for the next sprint. Thank you.