# Meeting Transcript - 27 Oct 2026


# Meeting Transcript


Hello.

Hello?

Yeah, I cannot hear your...

Hi.

Okay. Can you hear me?

Can hear me?

Yes, I can.

I cannot... say something ah, I can't hear.

Hello?

Hello, can you hear me?

Oh no, I cannot hear. Oh no. Why ah?

Hello.

Yes, I can hear. Oh no, I cannot hear you.

I turn on my mic already. Wait ah, I rejoin, I rejoin. I try again.

Hello?

Oh no. Hello, cannot hear.

Hello?

Hey, I can hear. Can you hear from this laptop?

Yes. Ah, it's my laptop, it's not your laptop.

Okay, I'm good, I'm good. We can start.

Okay, so uh, today our developer team will present to you the process of the whole system, and after that we'll have some questions to clarify the requirements, is that okay?

Okay.

Okay, so let's go first. Nito.

Okay. So can you hear me, short?

Yes, I can.

Okay, so, hi Shelly, uh, thank you for joining us today. I'm Nito and I'm from the development team and I will be the first presenter today. Uh, over the past 2 spring... review sessions... to gather feedback... system... And so far we have covered most of the core functionalities. Uh, however, there are still a few crucial challenges we need to - our team wasn't able to deliver in the last Friday's meeting. Uh, so the main purpose of today's meeting is to quickly walk you through the two functions: the fee management and FAS applications.

Okay. So, can you see the screen right now?

Okay. Let me share my screen.

Yep, I can see.

Okay, so this is the admin portal. And uh, first take a look at uh... First take a look at uh our fee management. Uh, this function can be managed by MOE and school users. And um, before we get started, there are a few key entities I would like to introduce. The first one is the fee type, which one you see on my screen right now. Fee types are used to categorize different kinds of fees, and they can be created by both MOE and school users. Uh, creating a fee type is pretty straightforward. You can see right here, you just need uh to input a name and a description, and that's it. So I'm going to quickly create a fee type for you.

Okay, so right here, I just created it. And the next one is, gonna talk about the fee component. Uh, fee component represents a specific fee uh that can be charged to students, and it's also reusable, uh which means we only need to create it once and we can use it again whenever we want to charge students for the same fee. Uh, so like here, I'm gonna create a new fee component. A fee component is belonging to one specific fee type, and to configure a fee component, there are a few steps we need to follow. First, we need to define its title, like here: examination administration fee. The next one is the scope of the uh... fee component. Uh, so based on our research, uh in Singapore, students may be charged different amounts for the same fee depending on uh certain criteria. So to support it, we have introduced the rate rules for each component. So, uh you can imagine that uh each rule has its own set of conditions and specific price. Uh, when a student matches a particular rule, they will be charged for the amount defined by that rule. And currently we are supporting two types of criteria. The first one is the student citizenship, like Singapore citizen, permanent resident, international student but uh from ASEAN, and the one that from non-ASEAN. So, yeah let me just take all of them and we'll explain later. And the next criteria is the education stage. And our system offers three types of education stage: is primary, secondary, and pre-university. Uh, so, uh, so why do I need to configure those scope? Uh, these scopes also uh... help us to ensure that the rate rules are properly defined to cover all the eligible students. Like um... like you want to have the fee component for the two Singapore citizen students, uh and uh they are from primary, they will have a different price from the one that in the secondary stage. And here, we also have the tax applied. Uh, this is um, we heard from Yao that we in Singapore we do have the fee, uh the the the text for the fee is GST. Um, and uh when the fee component is being enabled for the tax applied, uh currently we gonna be charged uh 9% for students from international students from ASEAN and non-ASEAN.

Okay, so continue.

Can I ask a question?

Okay.

So, uh you returned to your step 1...

Uh, okay right here?

Fee component. Yes. So, uh what is the difference between a fee component and a fee type? Why do I have to have one fee type, then I have a fee component?

Uh, just uh, like uh in our system, fee type is just a single entity to gather fee components with uh similar uh characteristics together. It's just used for categorization, and it's nothing else.

Okay. If it's... if it is nothing else, why why can't I just keep it just fee type?

Mhm. Yeah, uh so uh yeah, actually I told you that the fee type can be used to like apply the tax for it. Like uh... currently we only charge tax uh for the student from Singapore uh student from East ASEAN and non-ASEAN, but uh as uh Yao suggested, um we can uh set the tax amount for different fee types, but we haven't managed to deliver it in this sprint.

Okay. Can. Yep, we'll move forward. Continue.

Okay, so after I create a fee component, the next step is to configure the rate rules based on the combinations of student citizenship and education stage. Uh, as you saw earlier, I selected four student citizenship categories and three education stages. This means that we now have to configure for 12 combinations. Uh, however, this can take a lot of time. And if you want to set 12... 12 rate rules for the same amount, you can use the fix amount mode, and uh you're gonna all of... 12 of the combinations will receive one price at once. Uh, so uh, another option is you can configure each single of them, but to quickly demonstration, I'm gonna use the fix amount. So they all have the same price. The effective is the range of the... the the range that this rule will be effective, so I'm gonna set the effective to a bit longer in the future. And then I save.

Can I don't... Can I don't set... set effective to? So as long as I don't set it, we will be using it forever?

Yeah. It's uh, we currently are required to be set, but uh a non... non... a non period can be used forever is uh we can consider that.

Because I saw it's a mandatory field, so you can don't let me fill up uh and keep keep using the same fee for the next year because usually school fees will not be changing so much.

Okay. So uh, as you can see right here is the details of the fee component that I just created. And right here is the rule of it, like everyone primary and for international student ASEAN it will be 1000. And right here I can edit the amount of it right here.

Okay, so uh, the next important step to publish is uh publish a batch from this fee component. So what does it do?

But just now I added one lump sum for different uh citizen type, correct? Because you say I I can select one by one, or I can just change one type, or I can create one amount for all. So when I need to come here to edit right, I have to come here to edit one by one, is it? I cannot based on... whoever I want to choose and edit at one go?

Yeah, you have to come into the detail of the fee component and edit the rules that you want to change in the amount single... single one by one by one.

Okay. I would prefer just now the way where I can, you know, choose whether I want to do one by one or uh separately.

Okay. Because one by one is very tedious.

Okay. We will consider that, and bring back and see how.

Okay. Thank you. Uh, so what is... does this function mean? This is where the MOE and school user can create a fee publication batch to start charging students for a particular fee like this fee. Uh, so uh look, let let me explain what is the fee batch is. A fee batch represents a specific fee collection. Uh, currently our system only allows one fee component per batch. So if a user want to charge students for multiple fee components, they will need to create separate batches for each one. So like for example, I'm collecting the uh administration fee right here in this batch, and I also want to collect the learning material fees. I need to - I will need to create another batch for the learning material fees. So now let me create a batch, and we do have to uh provide some information. The first one is the title. Uh, it's pretty straightforward, huh? Okay, so the next is the period start and period end. So the period... the these two fields are quite important uh because they used to prevent overlapping fee collections. For example, if I set the period start to 27 today, and I set the uh period end to 30 October. And in this time, other users cannot set uh publish any batch that use this fee component again. So like uh, the user won't be able to publish another batch for the same uh administration fee during that period. And we do allow them to uh set this one to none, which means that it will not cannot be published again. This fee component again.

And the schedule uh is uh optional, and this allow user to schedule a batch to be published uh automatically at a specific date and time, like right now I'm gonna set it to 2:50 PM. And after 2:50 PM, it will be published. Uh, you don't have to set it. If you don't have to set it, you want to go into the batch detail and click the publish button later.

Okay, so the due date is pretty simple, is the deadline of the date uh the charge date. And it has to be greater than the schedule.

And then, um, let's move to the publication target. Uh, as I mentioned earlier, each fee component already had its own scope. Uh, however, when creating a batch, user can further customize the publication target uh to decide exactly which school and student should be charged. Uh, for example, let's say I want to charge the student from School A and School B right here. I can choose School A and School B. And then inside of those schools, I want to choose some students that will be inside of this school. And our database doesn't have student in that school, so I'm going to choose again. Uh, let me see which which one. Okay, so we have some students right here, 30 students. I want to charge them specifically. I'm going to confirm my selection. And then uh, 30... this 30 student will be charged.

Okay, so uh, I'm gonna create it. And here is the warning for the create an open-ended fee period. So because I set the period end to none, so it doesn't mean a one time uh fee component. So...

Nito, I ask a question here huh.

Yes.

So uh, just now that page, right? Can I base on the school students' schooling status? That as long as I'm active, I'm supposed to build it.

Yeah, can you say it again? I cannot hear quite clearly.

Okay. So as long as the student is active in the school, the system should build this student. Yes, so can I have an option to choose that as long as I'm active, I will build the student?

Because just now at your selection, right, um I didn't know whether can I build students that is inactive, or can I build students that is active.

Uh, currently we choosing that uh the student that uh enrolled inside of that school and the status is enrolled, is which means they are studying in that school.

If they are un-enrolled, not enrolled right, you won't - we will not build them correct?

Yeah.

Okay, okay.

Okay, so right now, as you can see on 2:50, the the publish will be automatically published. Uh, but uh if you don't want to wait for another minute, I will click the publish button right away. Oh, you want to wait?

Uh, so I just want to ask one more question. So in the event, do I - can I - can I take a look at the bill first before it get published? Because I'm scared something is wrong, I can go and amend.

Because now when we publish, I don't know whether is it correct or not.

Yeah, it's right here. So you can see all the the uh student charge, which mean the the charge that I have created for that specific student, and the status of it. And we also have the fail charge after the publish. Uh, it will resolve the the result. And uh if it success, it will be created. And if it fail, it will be fail. And the pending is uh on the process.

Those pending ones, can I - can I view the bill first? Can I take a look how it looks like?

Uh, because I scare when I publish it's wrong. So I - before I already publish, I can take a look first. Make sure it's correct before I publish.

Oh, so like you want to click on the student to view his uh education history, right?

Yeah, uh to to view the bill that is going out.

Ah.

Because now pending, correct? Now pending right?

Yeah.

Yeah, so I scared the bill is wrong. So I can stop it, correct? Assuming I can stop it. But I want - I need to know whether did I uh build correctly or not. Can I have a look at how it looks like before I really publish?

Okay, so I'm gonna - it's gonna take a while, and I'm create a fee with the draft status. If it's draft, it will show that uh which student will be charged and how much money they gonna be charged. Okay, so let me just quickly create a new fee component for you. It's meant charlie fee. And I'm gonna click all the uh criteria again. Okay. Okay, so this time I will not be uh schedule the the fee, so it's going to be in a draft.

Mm.

Uh, oh. Actually I think I just close it in the draft status, it should show that which student and how much they gonna be charged, but I think that I have changed it so uh I can I can show the money to you, but not right now because I have...

Yeah, it's a demo. Okay, can can.

So the main objective is I just want to make sure what I created is correct before I publish.

Okay. Okay.

So uh, let me just publish this uh fee component. Uh but first, let me log in into the parent uh website. Is this our parent website? And I can log in with a Singpass, as the requirement. So, here's my children, they are Lucas Lim and Nathan Lim. And as you can see right here, I uh I have charged Lucas Lim for it. So if I click the publish button right now, the the parent will see the student to be charged.

Okay, so here's here's the current billing payment right now. And I gonna click publish. Okay, it's in the processing process. And you can refresh to check the status. So I have created successfully 30 statuses, which mean all the students have been charged. So in the par-

In the parent...

I just reloaded it. And right here, you can see your fee, Charlie Fee, right here.

Mm.

Okay, so uh I can continue to uh pay the uh fee with my online payment. Okay, so this is payment has been successfully. Uh, and uh let me get back to the uh detail. And if there are some transactions about the fee batch. And I can see the analytics of the fee for the last 7 days right here. So I have just uh... the a parent has just uh paid the fee for $1,000 SGD. Yeah.

Okay.

Okay. And uh I think that's I have covered all the main features for the fee management function. So uh, before we move on to the next function, we want to really want to hear your feedback and what were we demonstrated so far. Yeah.

Um. So uh, you want to give us some feedback or later?

For this page is it?

Yeah, yeah. If no, a Christian will be demo the FAS application feature right now, and you can give us some feedback later.

Uh, maybe you can screenshot. Okay, to me ah, most important thing is uh the main thing I need to see whether the job runs successfully, it should always be on top. Then all the uh analytics information, bar chart, whatever, can be at the bottom.

Ah okay, thank you.

So uh Christian will be the one who demo for you the function four, is the FAS application. So uh okay. Thank you.

So hi Shelly, hope you have a good day. So I will have a quick demonstration about the...

Oh, who are you?

Ah, I am Christian, I'm sorry. So we will have a quick demonstration for... for the FAS function. So now we will begin our journey at the MOE portal. So, in MOE FAS, we will have be able to create a scheme. Uh, first we will name it. So in a scheme we have the two definitions of the date. The first one is open, that means the parents can submit their application for financial assistance. So...

And the second is effective from. Uh, effective from, that means when we uh at this time, the the system will take responsibility to allow the parents to use the uh... uh the money we uh provide them in the scheme.

Sorry.

So.

So in a scheme we will have to identify the nationality. However, uh in MOE we only allow Singapore citizen, but the UI also provide another option, this will be strictly forbidden in in a deeper layer. So we can choose the household income for the condition. And the per capita income for the second condition to pass this scheme. So... next.

So when we want um... with a MOE FAS, we only allow them to make uh assistance for education stage. And in our system we have three education stages: include primary, secondary, and pre-u. And we will type in the percentage where of subsidy we will allow them, and we will add them.

So.

Can I ask... can I enter a flat rate instead of percentage? Can I choose? Like it might be a flat rate of $100 or a 50% of the thing? Whichever is lower.

So in this scenario we only allow them to put in percentage uh... put in percentage to have them in a specific fee component in their single education stage.

And can I next to publish this scheme?

Oh. Sorry.

Something wrong with this.

So now we have a new MOE FAS, and I will move to the parent side to... make uh an application for their child. First I have to log out to... log in again to begin a new session. So choose a random user.

So in their uh screen, we will click on FAS application. We uh... we allow them to automatically fill information which uh which are managed in our system, and they only fill in some unmanaged uh data field. And in an application they will confirm for their commitment, and they will have to agree to move this application to school in case they fail the MOE FAS scheme.

Mhm.

Okay.

So in an application we have three, three main fields of data. The first one is the application whose owns this account. The next is their child, we call them uh beneficiary detail, which is uh managed in student school service. And on the other hand, we also have the family member which is managed by government data. And we can submit this application.

Okay.

So in this case, uh this application cannot pass the MOE scheme condition, so we'll it will have - it will be moved to the school, the school of their child, to check for the active, the current active scheme. So...

Can I check ah? So why is it straight away forward to school? Is it because you all checked that they do not pass the MOE FAS, that's why it was forwarded to the school, or...

Uh, in an application we have a checkbox to know that they if the parent want to move their application to the school scheme, school financial assistance, in case they fail the MOE FAS. It's another option if they fail the MOE. Right?

Okay. Um, I I will prefer huh, I just share, I would prefer if the student fill out everything, it will go through FAS - MOE FAS first, then by automatically it will go to the school. We don't need to ask the parents to declare whether do I need to forward to the school if I fail. So the system should just auto pick up that uh if MOE FAS doesn't pass, it will go to school FAS. Yeah. And if school FAS uh...

I'm not sure ah, let me think ah. If school FAS is still did not pass, right, because we can set the scheme, we can set uh MOE FAS scheme, we can set school-based FAS scheme. So if they don't pass MOE FAS, it will goes to school-based FAS. And if school-based FAS still fail, the mother or the father can go to the school and say, "Hey, I am really very poor. Can you give me the school-based FAS?" So at this moment, when the school-based FAS is rejected, the school user can override because the children come, the parents come and look for the school admin and tell them that they are very poor, they need help.

Oh. So as you mention that the application, in case they fail both MOE and the school based, in another hand, they can move directly to the school office and raise their help. So in this case, we will always allow them to receive?

Uh, not always. So case by case basis, the school admins will uh evaluate and say, "Okay, uh, I understood you give me all your necessary supporting documents offline. I can agree to give you." But some of them if cannot provide any supporting documents, no, I will not give you. So they can override based on additional information provided by the parents offline.

Yeah. Thank you very much, and I will back to the admin. So we have to log out and sign in their child school account.

Sorry, sorry, I have uh one question.

Sure.

Um, you talked to uh to parents when they fail the school-based FAS, and uh they if they want to reapply, uh they talk, they have... to school user or they have to uh provide any required documents. Can you uh tell us uh some of the examples of the required documents? What are they?

It can be their uh additional income that they have, or other people that is staying with them. So if there are more people staying with them, the PCI will decrease. So depending on whether they earn more money, which is additional income, or I have more people staying in my household. Because all this will result the PCI uh calculation.

Ah, all of the the things that you mentioned, they are all the criteria that we um set in the scheme for the school user to to to set up, to configure their their scheme already?

Correct.

So uh, I would like to know if there are any issues, uh any extra documents rather than those that you have just mentioned that uh the school user can reconsider their application?

Uh, you mean the documents to be submitted is it?

Yeah, yeah. Because school user already, when they configure their scheme, they have already set the criteria based on the PCI uh or their extra income of the parents and other members of the parent.

Well, this information comes from homes, you know, right? Like I have to call the homes API to retrieve all this information.

Yeah, yeah.

So in the event if homes retrieve doesn't have it, nobody tells them, correct? Understand. So for example, I can have a my my family can have a baby that is born today, but the homes interface do not have this information. So as a school admin, I can then go and override certain things as well. Or maybe I um my my my grandfather is very old, decided to stay with me this week, but homes interface do not have this information. So homes interface really takes time to update their information. But because the grandfather is already staying with me, I can go to the school admin and prove them and showing them the the IC, our identification card, saying that this this grandfather is really staying with me. So I have an evidence that I say that more people is staying within my household. That's why my PCI should be actually be lower than what is retrieved from the homes. This is the our real-life scenario lah.

Yeah.

By the way can we ask for like uh 5, 10 more minutes so that we can finish...

Can, can, can, can. Yeah.

So, to finish the journey, we will back to school admin screen, and in this school screen, we have two scheme right now. One for... one in status of application open, that means they will receive the parents application before, and effective, that means they will proceed with the student charge to uh to have them in the scheme percentage as I mentioned previously. So in they in this screen, uh we can see a new application we have just sent to the school management. And it's in status forwarded to school, that means we will wait for the effective time for the school admin to process the confirmation. So...

In this uh, we prepare a... an application that is in effective and pass all the scheme conditions, and we will prove for them. So, unfortunately, there are some conflicts in our UI status. So, so when we approve this application, we will have a handshake with our billing payment to allow a subsidy charge to decrease their... their student charge when we pay for the billing. So, this is the end of our journey in FAS uh function. So back to Hayden, he - can you give us some... requirement...

Can you enter the hardcopy form right now? Because in the requirement, hardcopy form is also mentioned.

Oh, there... the hard copy... to right... so that up there... can we have finish it...

Uh, we haven't finished the uh OCR, but we are processing. We might show you in the uh in Friday afternoon.

Do you all need any uh requirement or you all understand the requirements?

Uh, I already asked Yao for it, and we are working on it.

Okay, can. Yeah, so next we'll demo the F7... uh the function 7 because we have two different approach for the function 7, and we want to ask for like um your decision which is your which uh you would prefer. So Christian, can you show the function 7?

So...

In the first...

So, in requirement 7, we would assume that we will have the user to use our system or UI. So we recommend that we will have a guided tour, as you can see on the screen. When they want to have in a specific function, like full tour or display only or help them to uh submit an FA FAS application, they can choose this. And in this scenario, the UI will allow them to next uh step by step to learn and to read the screen information and help them to finish their purpose.

Um, on the other hand, another function, they will uh the... the admin, MOE admin, will have...

We'll have the ability to to see the the parent screen, and this will be demonstrated by Nito. So, Nito, can you help me to demonstrate the view function of the MOE admin?

So, uh, you might want to take your time a little longer, just to show the demo for the function uh 7. So currently we have two ways to implement this function. uh, just open the... okay, the first one is the using the guide tour. Okay, so the next one is the View As function. Let me just log in for the MOE...

Okay, so right here I have to View As. Uh, I can search for the school user or the parents. So these are the lim right?

Is it Lim?

Okay, so uh I'm gonna search - search for his account, and I'm gonna create...

I'm gonna search for his account, and I create some reasons to be in, and I'm gonna request a live view. So after I request a live view, this parent will receive an information that you want to share your screen with the MOE. And if you decide to share your screen, the the admin will see your screen and uh, each uh action you do will be respond uh stringlessly to the user like here. When I scroll up, and when I go to the uh page, the page will reflect correctly to the uh admin screen right here.

And I can go to there, and I can perform my actions. And uh why I encou- encounter some error, I can uh immediately ask my - ask for the MOE what uh what is wrong with it, and the MOE can see the the situation and explain it to the customer.

Okay. So this one I can give some feedback. Um, for the simulation right, I don't - I can see whatever the parents can see. But the action buttons has to be disabled. I cannot tell the parents to pay money.

Ah, okay.

Okay, so uh right here I can choose another actions like the View As, uh which means I will automatically uh be navigate to the parent account, like here. And I'm currently the admin. And uh I can go and I can select whatever I want. Like I can even select and try to pay for them. But when I want to authorize and pay, I cannot do it.

Okay, that's good.

Okay. So this is our final solution. Are you okay with it?

Yeah, okay. I'm okay with that one.

Okay, thank you.

Okay, thank you. So uh Hayden, you would like to ask anything, Hayden?

Yes.

Yes. Okay, so uh I have some question to ask you uh mainly about the function six, seven. So uh previously uh Nito has presented to you about the simulation function. So are you taking that question, or do you have some feedback about it?

Yeah, so I need to simulate two things. One is parents, the other one is school user. So just now you only show me parents, so I also need to see how school user uh it looks like, so you can demo to me.

I mean no need now lah, I mean uh uh because not enough time so we can do the demo, it's fine.

Okay, understand.

Okay, so uh I will have a small question uh relevant to the function 6. So uh in our system right now, uh created by logic that um for example, in a school, in a school, a school user will manage like uh a check... buckets...

But there are multiple scheme, instead of that, do you have a single manage the whole scheme? So make sure the current flow is uh we manage uh a lot of bucket, and each bucket manage one scheme. Instead of one budget manage the whole scheme in one school run.

So... HQ will HQ manage their own budget, school will manage their own budget. So if the school user budget got uh over budget, you need to display what is the over budget that they set. But for HQ there is no budget.

Yeah, so for example the MOE admin are they allowed to like uh manage uh many buckets for just one?

One is fine, just it cannot be over budget for school. School cannot be over. Once I set a budget for a school right, if I hit the budget up, system need to alert me. But MOE HQ budget also can set, setting one budget, but because they have limited budget.

Uh. So uh. Uh but you want to see if we can limit all limit that the MOE users manage their own, like for instances, student... school...

Uh, what I mean - what I want to ask is, for example, there's a scheme, uh scheme in a school, and uh school user want to uh want to know that uh in that scheme which student earn that scheme? Uh, do you want to to - that the...

What you mean what what you mean which shouldn't earn that scheme?

Uh, I mean, uh currently, maybe the school have many schemes that are currently running, and the school user want to manage uh which student earn that scheme. Are they want to print the the information?

So I got you one more time. The front end you surround and put it in and test the API properly. So after every point...

Okay. You also you you check everything properly and you have some tests about the AI chatbot, um want to do the full...

Show them it's nothing to pay a student payment or something, or the AI can do anything else, or it can I mean the AI just limits it, nothing to interact and perform actions for the payment.

What... I think...

So user guide is for them when they can self-help.

Ah so you want us to pop - what pop up the the guy tool like the the video one?

Okay, yeah. But you prioritize the uh simulation first. That one is more important, because if they have any issue, we can simulate. The guy is more for them to, you know, first time when I log in I don't know where to click, that that guy is good to have.

Okay, got it.

Thank you.

Okay, uh I have another meeting already. So sorry. uh if you all got any questions, you can just drop me via Teams, I can help to reply from there.

Okay, got it. Okay, so thank you for today, and we'll see you on Friday. Thank you.

Thank you. Bye bye.

Okay, bye.

Ok bye bye.